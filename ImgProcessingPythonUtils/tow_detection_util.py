from medpy.filter.smoothing import anisotropic_diffusion
from tow_inspection_util import *

def write_tow_in_csv(file_name, edges, target_folder):
    f = open(os.path.join(target_folder, file_name[:-4]+'.csv'), 'w')
    
    with f:
        writer = csv.writer(f)
        writer.writerows(edges)

# STRAIGHT TOWS UTILS---------------------------------------------------------------------------------------------------
def fit_edge(gradients):
    # define a function to be fitted
    def func(x, a, b, c):
        return np.square(x)*a + x*b + c 
    
    popt, pcov = curve_fit(func, range(len(gradients)), gradients)
    return popt

def tow_detection(img, num_tow=8, rigidity=8):
    """
    1. Need to differentiate the curved ones and straight ones.
    2. Separate the cases for different tows
    Inputs:
        num_tow: the number of tows should be detected from the image.
        rigidity: how straight the fitted curve along edges.
    Return:
        edges: [(num_tow+1) x 2 x height]
    """
    # filtering the images
    medianed = cv2.medianBlur(img, 13)
    # plotImage(medianed) 
    _, median_gradient = np.gradient(img) # only the horizontal gradient is needed, on medianed/original image

    # create a mean vertically and find gradient on it
    means = np.mean(medianed, axis=0)

    # find course edges
    gradientArr = np.gradient(means)
    sortInds = np.argsort(np.absolute(gradientArr))
    maxGrdInd = sortInds[-1]
    sortIndsWithoutMax = sortInds[np.where(np.logical_or(sortInds>(maxGrdInd+10), sortInds<(maxGrdInd-10)))]
    secMaxGrdInd = sortIndsWithoutMax[-1]
    print("The course edges are at ", maxGrdInd, secMaxGrdInd)
    
    y = np.arange(len(img), dtype=int) 
    edges = np.empty([num_tow + 1, 2, len(img)])
    
    # finding local maximal gradients
    tow_width = int((max(maxGrdInd, secMaxGrdInd) - min(maxGrdInd, secMaxGrdInd))/num_tow)
    edge_list = [min(maxGrdInd, secMaxGrdInd) + i*tow_width for i in range(num_tow + 1)]
    for i in range(len(edge_list)):
        mid = edge_list[i]
        left = mid - int(tow_width/rigidity)
        right = mid + int(tow_width/rigidity)
        search_range = median_gradient[:, left:right]
        max_gradient = np.argmax(search_range, axis=1) + left
        # print("Max gradient of edge", i, ", its shape is", max_gradient.shape)
        
        [a, b, c] = fit_edge(max_gradient)
        x = range(len(max_gradient))
        fitted_curve = np.square(x)*a + x*b + c
        # print("Fitted curve shape is", fitted_curve.shape)
        
        edges[i] = np.concatenate((fitted_curve[:, None], y[:, None]), axis=0).reshape((2, -1)) 
    return edges

# SQUIGGLY TOWS UTILS---------------------------------------------------------------------------------------------------
def fit_edge_high_order(gradients):
    # Defined a third order function to be fitted, as curvature of steered tow
    def func(x, a, b, c):
        return np.power(x, 3)*a + np.power(x, 2)*b + x*c + d 
    
    popt, pcov = curve_fit(func, range(len(gradients)), gradients)
    return popt

def tow_detection_steer(img, num_tow=4, rigidity=4):
    # steered case
    if num_tow == 4:
        left_bound = 1300
        right_bound = 1930
        
    # filtering the images
    medianed = cv2.medianBlur(img, 7)
    diffused = anisotropic_diffusion(img=medianed, niter=30, kappa=20, gamma=0.1, option=2)
    # plotImage(diffused) 
    diff_top = np.mean(diffused[:10,:], axis=0)
    
    # find course edges
    gradient_arr = np.gradient(diff_top)
    sort_inds = np.argsort(np.absolute(gradient_arr[left_bound: left_bound+40])) + left_bound
    left_grad_ind = sort_inds[-1]
    sort_inds = np.argsort(np.absolute(gradient_arr[right_bound-30: right_bound])) + right_bound - 30
    right_grad_ind = sort_inds[-1]
    print("The course edges are at ", left_grad_ind, right_grad_ind)
    
    _, median_gradient = np.gradient(diffused) # only the horizontal gradient is needed, on medianed/original image
    median_gradient = np.abs(median_gradient)
    
    y = np.arange(len(img), dtype=int) 
    edges = np.empty([num_tow + 1, 2, len(img)])
    
    # finding local maximal gradients
    tow_width = int((right_grad_ind - left_grad_ind)/num_tow)
    edge_list = [left_grad_ind + i*tow_width for i in range(num_tow + 1)]
    for i in range(len(edge_list[1:-1])):
        mid = edge_list[i+1]
        left = mid - int(tow_width/rigidity)
        right = mid + int(tow_width/rigidity)
        search_range = diff_top[left:right]
        max_gradient = np.argmax(search_range) + left
        edge_list[i+1] = max_gradient
    
    edge_list = np.transpose(np.array([[0]*len(edge_list), edge_list]))
    edges[:, :, 0] = edge_list.astype('int')
    # print('edges', edges[:, :, 0])
    # now try row by row, afterwards, 5-20 rows; vertorize later
    for i in range(len(img)-1):
        middles = edges[:, 1, i]
        lefts = middles - 5 # emperical
        rights = middles + 5
        # print(middles, lefts, rights)
        for j in range(len(middles)):
            search_range = median_gradient[i+1, int(lefts[j]):int(rights[j])]
            max_gradient = np.argmax(search_range) + int(lefts[j])
            # print(max_gradient)
            gradient_row = np.transpose(np.array([i+1, max_gradient]))
            edges[j, :, i+1] = gradient_row
    return edges