# Computational-Redistricting
## Authors
Anthony Sharma and Jack Ringer

## About
Final project for CS506 - Computational Geometry

## Usage
```
(env) Computational-Redistricting/src$ python main.py -h
usage: main [-h] --n_points N_POINTS [--sample_method SAMPLE_METHOD]
            [--color_method COLOR_METHOD] [--n_colors N_COLORS]
            [--color_probs COLOR_PROBS] [--seed SEED]
            [--fig_save_path FIG_SAVE_PATH]

Visualize points with given params

options:
  -h, --help            show this help message and exit
  --n_points N_POINTS   number of points
  --sample_method SAMPLE_METHOD
                        method for sampling spatial points
  --color_method COLOR_METHOD
                        method for sampling color points
  --n_colors N_COLORS   number of colors to use
  --color_probs COLOR_PROBS
                        probability of sampling each color
  --seed SEED           random seed
  --fig_save_path FIG_SAVE_PATH
                        path to save figure to (optional)
```

## TODO:
* Algorithm for ham sandwich and weighted ham sandwich cuts