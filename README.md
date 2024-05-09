# Computational-Redistricting
## Authors
Anthony Sharma and Jack Ringer

## About
Final project for CS506 - Computational Geometry.

This project contains an implementation of repeated ham-sandwich cuts (RHSCs) in the plane. 

The project was developed with the goal of computational redistricting in mind (hence the repo name). However, our implementation of RHSCs could reasonably be adapated to other tasks.

## Usage
```
(env) Computational-Redistricting/src$ python main.py -h
usage: main [-h] --points_per_color POINTS_PER_COLOR [--program PROGRAM]
            [--weight_method WEIGHT_METHOD] [--color_method COLOR_METHOD]
            [--seed SEED] [--fig_save_path FIG_SAVE_PATH] [--show_fig] [--k K]
            [--calculate_final_regions] [--subsample_points]
            [--subsample_ratio SUBSAMPLE_RATIO]

Visualize points/lines with given params

options:
  -h, --help            show this help message and exit
  --points_per_color POINTS_PER_COLOR
                        number of points to use for each color
  --program PROGRAM     program to visualize, choose from: ('ham_sandwich',
                        'iterative_ham_sandwich', 'visualize_points')
  --weight_method WEIGHT_METHOD
                        how to weight points, choose from: ('uniform',
                        'majority')
  --color_method COLOR_METHOD
                        method for sampling color points
  --seed SEED           random seed
  --fig_save_path FIG_SAVE_PATH
                        path to save figure to (optional)
  --show_fig            show figure if set
  --k K                 (iterative_ham_sandwich only) number of iterations to
                        perform
  --calculate_final_regions
                        (iterative_ham_sandwich only) calculate final regions
                        formed by cuts and log their statistics
  --subsample_points    subsample the original set of points before performing
                        HSC
  --subsample_ratio SUBSAMPLE_RATIO
                        ratio of points to sample, will sample floor(n_points
                        * ratio) total points
```