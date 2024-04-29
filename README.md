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
  * In particular need to repeat experiments using different seeds - 10 repetitions for each experiment seems reasonable
* Add code to calculate district majorities after RHSC
  * Fairly straightforward for unweighted case
  * For weighted case probably need some kind of flag saying if a point is an actual point or just part of weighting scheme
  * Then can run experiments to measure how well weighting scheme actually works (rather than having to eyeball everything)
* (Optional) Adapt cluster method to (very roughly) simulate population regions
  * Basically each point is a population site - give small points_per_color
  * Could say the site color is the majority - randomly sample between [0.51, 1.0] by how much they're a majority
  * Can adapt _cluster() method in `point_set.py` to achieve this
  * Could probably sample spreads and population counts (ie weights) from a gaussian
  * See how this impacts cuts/methods compared to uniform random?