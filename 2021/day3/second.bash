#!/bin/bash

set -euo pipefail

INPUT="input.txt"
FIRST_LINE=$(cat ${INPUT} | head -n 1)
LEN=${#FIRST_LINE}
((LEN=LEN-1))

o2_nums=($(cat ${INPUT} |tr "\n" " "))
co2_nums=($(cat ${INPUT} |tr "\n" " "))
o2=""
co2=""

# for index in 0; do
for index in $(seq 0 ${LEN}); do
    zeros_o=0
    ones_o=0
    zeros_co=0
    ones_co=0
    echo N-th digit: $index
    # o2 levels
    for value in ${o2_nums[@]}; do
        ELEM=${value:index:1}
        if [[ ${ELEM} -eq 1 ]]; then
            ((ones_o=ones_o+1))
        else
            ((zeros_o=zeros_o+1))
        fi
    done
    # co2 levels
    for value in ${co2_nums[@]}; do
        ELEM=${value:index:1}
        if [[ ${ELEM} -eq 1 ]]; then
            ((ones_co=ones_co+1))
        else
            ((zeros_co=zeros_co+1))
        fi
    done

    # o2 next values
    if [[ ${#o2_nums[@]} -gt 1 ]]; then
        most_common_o2=""
        if [[ ${ones_o} -ge ${zeros_o} ]]; then
            most_common_o2=1
        else
            most_common_o2=0
        fi
        new_o2_nums=()
        for value in ${o2_nums[@]}; do
            ELEM=${value:index:1}
            if [[ ${ELEM} -eq ${most_common_o2} ]]; then
                new_o2_nums+=(${value})
            fi
        done
        o2_nums=("${new_o2_nums[@]}")
    fi

    # co2 next values
    if [[ ${#co2_nums[@]} -gt 1 ]]; then
        least_common_co2=""
        if [[ ${zeros_co} -le ${ones_co} ]]; then
            least_common_co2=0
        else
            least_common_co2=1
        fi
        new_co2_nums=()
        for value in ${co2_nums[@]}; do
            ELEM=${value:index:1}
            if [[ ${ELEM} -eq ${least_common_co2} ]]; then
                new_co2_nums+=(${value})
            fi
        done
        co2_nums=("${new_co2_nums[@]}")
    fi
done

echo "02: "${o2_nums[@]}
echo "co2: "${co2_nums[@]}


o2=$((2#${o2_nums[0]}))
co2=$((2#${co2_nums[0]}))

echo O2: "${o2}"
echo CO2: "${co2}"
echo $(( o2 * co2 ))