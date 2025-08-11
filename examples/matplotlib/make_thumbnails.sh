#!/bin/sh
export MPLBACKEND=module://gr.matplotlib.backend_gr
for f in  *.py
do
  GKSwstype=pdf python $f
  x=`echo $f | awk -F\. '{print $1}'`
  cpdf -scale-page "0.5 0.5" gks.pdf -o ${x}.pdf
  rm -f gks.pdf
done
rm -f tex_demo.png
