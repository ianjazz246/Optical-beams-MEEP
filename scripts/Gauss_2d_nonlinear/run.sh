#!/bin/sh
n1=1.00
n2=1.54

MEEP_SCRIPT=Gauss2d.py
# logk = -2
for amp in 1.0 5.0 10.0; do
        out_dir="amp=$amp logk=-2"
        python3 "$MEEP_SCRIPT" -logk -2 -amp "$amp" -n1 "$n1" -n2 "$n2" -outdir "$out_dir"
done

python3 "$MEEP_SCRIPT" -logk -3 -amp 1.0 -n1 "$n1" -n2 "$n2" -outdir "amp=1.0 logk=-3"
python3 "$MEEP_SCRIPT" -logk -1 -amp 1.0 -n1 "$n1" -n2 "$n2" -outdir "amp=1.0 logk=-1"
