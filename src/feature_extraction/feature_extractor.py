''' Extract features from raw data

Author: Bradley Reeves
Date: May 23, 2021

Planned features:
Latencies
---------
lr: Transition from left hand to right hand
rl: Transition from right hand to left hand
lR: Transition from left hand to right hand + shift
Lr: Transition from left hand + shift to right hand
rL: Transition from right hand to left hand + shift
Rl: Transition from right hand + shift to left hand
lL: Transition from left hand to left hand + shift
Ll: Transition from left hand + shift to left hand
rR: Transition from right hand to right hand + shift
Rr: Transition from right hand + shift to right hand
ll: Transition from left hand to left hand
rr: Transition from right hand to right hand

Hold Times
----------
l: Hold time of left hand keys
r: Hold time of right hand keys
L: Hold time of left hand keys + shift
R: Hold time of right hand keys + shift
space: Hold time of space key
shift: Hold time of shift key

Other
-----
cpm: Characters per minute (type speed)
'''

import numpy as np
import pandas as pd

class FeatureExtractor:
    def __init__(self, dataset):
        self.dataset = dataset

    def __clean_data(self):
        # Commas need a fixin
        pass

    def __get_latencies(self):
        # Each sentence will be a single sample
        # So, each session (uuid) should have about 10 samples
        # How about creating a df with sentenceId, mean_latencies, mean_hold_times, and cpm
        
        # For this, we only care about the keydown events
        temp_df = self.dataset[(self.dataset['key_event'] == 'keydown') & (self.dataset['key_char'] != 'Shift')]

        for index, row in temp_df.iterrows():
            print(temp_df['key_char'][index])

    def __get_hold_times(self):
        pass

    def __get_cpm(self):
        pass

    def generate_features(self):
        #print(self.dataset.head(5))
        #print(self.dataset.tail(5))

        new_dataset = pd.DataFrame(columns=('lr', 'Lr', 'lR', 'rl', 'Rl', 'rL', 'll', 'Ll', 'lL', 'rr', 'Rr', 'rR', 'l', 'r', 'L', 'R', 'space', 'shift', 'cpm'))

        mean_latencies = self.__get_latencies()
        #hold_times = self.__get_hold_times()
        #cpm = self.__get_cpm()

        return new_dataset
            
