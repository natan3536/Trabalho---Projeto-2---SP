#!/bin/bash
SIZES="5000 10000 20000 30000 40000"
RUNS=5
OUT=resultados_projeto2.csv
echo "protocolo,n,corrida,tempo_s,enviado_MB,recebido_MB" > $OUT
for p in 0 2 3; do
  for n in $SIZES; do
    for run in $(seq 1 $RUNS); do
      ./psi.exe -r 0 -p $p -b 16 -n $n > /tmp/r0.txt &
      sleep 1
      ./psi.exe -r 1 -p $p -b 16 -n $n > /tmp/r1.txt
      wait
      t=$(grep "Required time" /tmp/r0.txt | awk '{print $3}')
      s=$(grep "Data sent" /tmp/r0.txt | awk '{print $3}')
      r=$(grep "Data received" /tmp/r0.txt | awk '{print $3}')
      echo "$p,$n,$run,$t,$s,$r" | tee -a $OUT
      sleep 1
    done
  done
done
