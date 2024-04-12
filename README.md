# Computational-Redistricting
## Authors
Anthony Sharma and Jack Ringer

## About
Final project for CS506 - Computational Geometry

## Usage
```
(env) Computational-Redistricting/src$ python main.py -h
usage: main [-h] --points_per_color POINTS_PER_COLOR [--algorithm ALGORITHM]
            [--sample_method SAMPLE_METHOD] [--color_method COLOR_METHOD] [--seed SEED]
            [--fig_save_path FIG_SAVE_PATH] [--show_fig] [--k K]

Visualize points/lines with given params

options:
  -h, --help            show this help message and exit
  --points_per_color POINTS_PER_COLOR
                        number of points to use for each color
  --algorithm ALGORITHM
                        algorithm to visualize
  --sample_method SAMPLE_METHOD
                        method for sampling spatial points
  --color_method COLOR_METHOD
                        method for sampling color points
  --seed SEED           random seed
  --fig_save_path FIG_SAVE_PATH
                        path to save figure to (optional)
  --show_fig            show figure if set
  --k K                 number of iterations to perform with iterative ham-sandwich algorithm
```

## TODO:
* Measure/plot timings for iterative hs-cuts for different values of n_points_per_color, k
* (Option 1) Sampling points from (maybe weighted?) Voronoi diagrams
* (Option 2) Try to simulate weighted ham-sandwich cuts by sampling additional points around existing points (integer weights >0)