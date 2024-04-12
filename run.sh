#!/bin/bash
# example script for running program
points_per_color="10,12"
algo="iterative_ham_sandwich"
sample_method="uni_random"
color_method="random"
seed=42
k=2

python3 src/main.py --points_per_color $points_per_color \
--algo $algo \
--sample_method $sample_method \
--color_method $color_method \
--seed $seed \
--k $k \
--show_fig