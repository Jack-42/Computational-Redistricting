#!/bin/bash
# example script for running program
points_per_color="10,12"
prog="iterative_ham_sandwich"
color_method="random"
seed=42
k=2

python3 src/main.py --points_per_color $points_per_color \
--program $prog \
--color_method $color_method \
--seed $seed \
--k $k \
--show_fig