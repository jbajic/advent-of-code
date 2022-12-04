#!/bin/bash

set -euo pipefail

INPUT="input.txt"
FIRST_LINE=$(cat ${INPUT} | head -n 1)
LEN=${#FIRST_LINE}
((LEN=LEN-1))

gamma=""
epsilon=""
for index in $(seq 0 ${LEN}); do
    zeros=0
    ones=0
    echo N-th digit: $index
    while read p; do
        ELEM=${p:index:1}
        if [[ ${ELEM} -eq 1 ]]; then
            ((ones=ones+1))
        else
            ((zeros=zeros+1))
        fi
    done < "${INPUT}"

    # Determine the nth digit
    echo Ones: ${ones} Zeros:${zeros}
    if [[ ${ones} -ge ${zeros} ]]; then
        gamma=${gamma}1
        epsilon=${epsilon}0
    else
        gamma=${gamma}0
        epsilon=${epsilon}1
    fi
done

GAMMA=$((2#$gamma))
EPSILON=$((2#$epsilon))

echo Gamma: "${GAMMA}"
echo Epsilon: "${EPSILON}"
echo $(( EPSILON * GAMMA ))