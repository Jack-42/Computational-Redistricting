# Computational-Redistricting
## Authors
Anthony Sharma and Jack Ringer

## About
Final project for CS506 - Computational Geometry

## Usage
```
(env) Computational-Redistricting/src$ python main.py -h
usage: main [-h] --points_per_color POINTS_PER_COLOR [--algorithm ALGORITHM]
            [--sample_method SAMPLE_METHOD] [--color_method COLOR_METHOD]
            [--seed SEED] [--fig_save_path FIG_SAVE_PATH]

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
```

## TODO:
* Algorithm for ham sandwich and weighted ham sandwich cuts