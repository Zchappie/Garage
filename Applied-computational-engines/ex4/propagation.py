import itertools


def unit_propagation(variables, cnf):
    # negate variables
    neg_variables = set(var * -1 for var in variables)
    # remove the negated variables from the cnf / unit propagation
    cnf_ = [set(c) - neg_variables for c in cnf]

    variables_ = set([list(c)[0] for c in cnf_ if len(c) == 1])

    if len(variables_) == 0:
        return variables
    else:
        return unit_propagation(variables | variables_, [c for c in cnf_ if len(c) > 1])

def optimal_table(cnf, num_vars, file):
    cnf = set(tuple(c) for c in cnf)

    # calculate all full valuations and solutions
    full_valuations = list(itertools.product([1, -1], repeat=num_vars))
    solutions = list()
    for v in full_valuations:
        variables = set([(var + 1) * val for var, val in enumerate(v) if val != 0])
        if all(len(c) > len(set(c) - variables) for c in cnf):
            solutions.append(variables)

    print(solutions)

    # calculate all partial valuations
    valuations = list(itertools.product([1, -1, 0], repeat=num_vars))
    partials = [x for x in valuations if 0 in x]

    with open(file, "w") as f:
        # latex table head
        f.write("\\begin{longtable}{|"+ "|".join(["c"]*(num_vars+2)) +"|}\n")
        f.write("\hline {} & unit propagation & optimal? \\\\ \\hline \n".format(" & ".join(map(str,range(1, num_vars+1)))))
        for v in partials:
            variables = set([(var + 1) * val for var, val in enumerate(v) if val != 0])
            # recursively use unit propagation and derive variables
            derived = unit_propagation(variables, cnf) - variables

            # get all superset solutions to the current partial solution
            sols = [set(solution) for solution in solutions if variables.issubset(solution)]

            # check if the solution is optimal
            # it is optimal if the superset solutions do not imply a valuation to a variable 
            # that we dont get by unit propagation.
            optimal = []
            if len(sols) > 0:
                hm = sols[0]
                for sol in sols:
                    hm &= sol
                for h in hm:
                    if h not in derived | variables:
                        optimal.append(h)

                derived = ",".join([str(c) for c in derived])
                optimal = ",".join([str(c) for c in optimal])

                print("{} | {:15} {:3}".format(" ".join("{:3}".format(x) for x in v), derived, optimal))

                varstrings = []
                for x in v:
                    if x == 1:
                        varstrings.append("true")
                    if x == -1:
                        varstrings.append("false")
                    if x == 0:
                        varstrings.append("-")

                f.write("{} & {:15} & {:3}\\\\ \\hline \n".format(" & ".join(varstrings), derived, optimal))
        f.write("\\end{longtable}\n")


cnf = [[3, -5], [1, -5], [-1, -3, 5], [2, -4, -5], [-2, -3, 4], [-1, -4, 5], [1, -2, -3]]
optimal_table(cnf, 5, "table1.tex")

