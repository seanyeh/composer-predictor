# Composer Predictor
#####EECS 349
#####Sean Yeh and Paul Juhn

### About
Our attempt to use machine learning to predict the composer of a musical piece.

### Basic Steps

1. Split each raw data file into multiple examples by running `./preprocess.py`. (this only needs to be run once, but no harm in running multiple times). The resulting data will be stored in `data/preprocessed/`
2. Evaluate features on each example by running `./generate.py`. This will store the results into two csv files: one for training and the other for testing
3. Create model and show prediction accuracy on testing data and/or show cross-validation scores by running `./model.py` with the `--test` and/or the `--cross-validation` flags.

As always, you can always run any of these files with the `--help` flag for more information.
