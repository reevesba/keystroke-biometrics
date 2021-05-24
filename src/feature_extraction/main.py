''' Extract features from raw data

Author: Bradley Reeves
Date: May 23, 2021

'''

import pandas as pd
from feature_extractor import FeatureExtractor

def main():
    # Test the extractor with a single user first
    dataset = pd.read_csv("../../dat/keylog.csv")

    single_session_df = dataset[dataset["uuid"] == "12ae2a9e-542e-4e4b-8302-96b3fd9637cd"]

    extractor = FeatureExtractor(single_session_df)
    extractor.generate_features()

if __name__ == "__main__":
    main()