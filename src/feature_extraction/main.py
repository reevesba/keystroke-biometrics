''' Extract features from raw data

Author: Bradley Reeves
Date: May 23, 2021

'''

import pandas as pd
from feature_extractor import FeatureExtractor


def main():
    # Load dataset
    dataset = pd.read_csv('../../dat/keylog_clean.csv')

    # Extract features
    extractor = FeatureExtractor(dataset)
    df = extractor.generate_features()

    # Save new dataset
    df.to_csv('../../dat/keystroke_biometrics.csv', index=False)


if __name__ == "__main__":
    main()
