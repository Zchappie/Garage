cat static.txt 

# We strongly believe Emden is Oldenburg
cat edges.txt \
    | sed "s/Emden-Hamm/+1 x1/g" \
    | sed "s/Emden-Bremen/+1 x2/g" \
    | sed "s/Bremen-Hamm/+1 x3/g" \
    | sed "s/Bremen-Hannover/+1 x4/g" \
    | sed "s/Hannover-Hamm/+1 x5/g" \
    | sed "s/Kassel-Hamm/+1 x6/g" \
    | sed "s/Hannover-Kassel/+1 x7/g" \
    | sed "s/Hannover-Erfurt/+1 x8/g" \
    | sed "s/Erfurt-Kassel/+1 x9/g" \
    | sed "s/Hamm-Frankfurt/+1 x10/g" \
    | sed "s/Kassel-Frankfurt/+1 x11/g" \
    | sed "s/Nuremberg-Kassel/+1 x12/g" \
    | sed "s/Erfurt-Nuremberg/+1 x13/g" \
    | sed "s/Frankfurt-Nuremberg/+1 x14/g" \
    | sed "s/Freiburg-Frankfurt/+1 x15/g" \
    | sed "s/Frankfurt-Stuttgart/+1 x16/g" \
    | sed "s/Stuttgart-Nuremberg/+1 x17/g" \
    | sed "s/Nuremberg-Munich/+1 x18/g" \
    | sed "s/Freiburg-Stuttgart/+1 x19/g" \
    | sed "s/Munich-Stuttgart/+1 x20/g" \
    | sed "s/Freiburg-Munich/+1 x21/g" \
    | sed "s/CUT //g" \
    | sed "s/AND //g" \
    | sed "s/ ENDCUT/ >= 1;/g"


