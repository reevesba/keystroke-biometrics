''' Extract features from raw data

Author: Bradley Reeves
Date: May 29, 2021

Note: Raw data should be presorted by uuid,
sentence_id, then timestamp.
'''

from pandas import DataFrame
from itertools import chain
from typing import List, Dict, TypeVar

# Custom types
FeatureExtractor = TypeVar('FeatureExtractor')


class FeatureExtractor:
    def __init__(self: FeatureExtractor, df: DataFrame) -> None:
        ''' Initialize FeatureExtractor instance
            Parameters
            ----------
            self : FeatureExtractor instance
            df : Keylogger Data

            Returns
            -------
            None
        '''
        # Remove the quote characters
        self.dataset = df[df['key_code'] != 222]

    def __get_lr(self: FeatureExtractor, code: int) -> str:
        ''' Map key code to left or right hand
            Parameters
            ----------
            self : FeatureExtractor instance
            code : Key code

            Returns
            -------
            Left or right label
        '''
        lr = {
            16: 'shift', 32: 'space', 65: 'l', 66: 'l', 67: 'l',
            68: 'l', 69: 'l', 70: 'l', 71: 'l', 72: 'r', 73: 'r',
            74: 'r', 75: 'r', 76: 'r', 77: 'r', 78: 'r', 79: 'r',
            80: 'r', 81: 'l', 82: 'l', 83: 'l', 84: 'l', 85: 'r',
            86: 'l', 87: 'l', 88: 'l', 89: 'r', 90: 'l', 188: 'r',
            190: 'r', 222: 'r'
        }
        return lr[code]

    def __get_dwell_feature(self: FeatureExtractor, chars: List) -> str:
        ''' Map key code and shift value to feature label
            Parameters
            ----------
            self : FeatureExtractor instance
            chars : [key code value, shift key value]

            Returns
            -------
            Feature label
        '''
        feature = {
            ('l', 0): 'l', ('l', 1): 'L',
            ('r', 0): 'r', ('r', 1): 'R',
            ('space', 0): 'space', ('space', 1): 'space',
            ('shift', 0): 'shift', ('shift', 1): 'shift'
        }
        lr = self.__get_lr(chars[0])
        return feature[lr, chars[1]]

    def __get_flight_feature(self: FeatureExtractor, chars: List) -> str:
        ''' Map two key codes and shift values to feature label
            Parameters
            ----------
            self : FeatureExtractor instance
            chars : [key code value, shift key value]*2

            Returns
            -------
            Feature label
        '''
        feature = {
            ('l', 0, 'r', 0): 'lr', ('l', 1, 'r', 0): 'Lr',
            ('r', 0, 'l', 0): 'rl', ('r', 1, 'l', 0): 'Rl',
            ('l', 0, 'l', 0): 'll', ('l', 1, 'l', 0): 'Ll',
            ('r', 0, 'r', 0): 'rr', ('r', 1, 'r', 0): 'Rr'
        }
        lr_a = self.__get_lr(chars[0])
        lr_b = self.__get_lr(chars[2])
        return feature[lr_a, chars[1], lr_b, chars[3]]

    def __get_flights(self: FeatureExtractor, df: DataFrame) -> Dict:
        ''' Calculate flights for sentence
            Parameters
            ----------
            self : FeatureExtractor instance
            df : All keystroke events for a sentence

            Returns
            -------
            flight_values : Sentence flight features
        '''
        # Remove rows that can be entered with either hand.
        # Also, get rid of the keyup events since we are
        # concerned with keydown to keydown flight.
        shift, space = (16, 32)
        df = df[
            (~df['key_code'].isin([shift, space])) &
            (df['key_event'] == 'keydown')
        ].reset_index(drop=True)

        flight_vals = {
            'lr': 0, 'Lr': 0, 'rl': 0, 'Rl': 0,
            'll': 0, 'Ll': 0, 'rr': 0, 'Rr': 0
        }
        flight_cnts = {
            'lr': 0, 'Lr': 0, 'rl': 0, 'Rl': 0,
            'll': 0, 'Ll': 0, 'rr': 0, 'Rr': 0
        }

        for i in range(len(df) - 1):
            chars = [
                df.at[i, 'key_code'], df.at[i, 'shift_key'],
                df.at[i + 1, 'key_code'], df.at[i + 1, 'shift_key']
            ]

            # Second keystroke should not contain shift
            if chars[3] == 0:
                # Calculate flight time
                feature = self.__get_flight_feature(chars=chars)
                flight_vals[feature] += \
                    df.at[i + 1, 'timestamp'] - df.at[i, 'timestamp']
                flight_cnts[feature] += 1

        # Replace flight_vals sums with means
        for k in flight_vals:
            if flight_cnts[k] > 0:
                flight_vals[k] = flight_vals[k]/flight_cnts[k]
        return flight_vals

    def __get_dwellings(self: FeatureExtractor, df: DataFrame) -> Dict:
        ''' Calculate dwellings for sentence
            Parameters
            ----------
            self : FeatureExtractor instance
            df : All keystroke events for a sentence

            Returns
            -------
            dwell_vals : Sentence dwelling features
        '''
        dwell_vals = {'l': 0, 'r': 0, 'L': 0, 'R': 0, 'space': 0, 'shift': 0}
        dwell_cnts = {'l': 0, 'r': 0, 'L': 0, 'R': 0, 'space': 0, 'shift': 0}

        for i in range(len(df)):
            if df.at[i, 'key_event'] == 'keydown':
                # Get the next keydown event
                keydown_key = df.at[i, 'key_code']

                # Get the same character's keyup event
                j = i + 1
                keyup_key = df.at[j, 'key_code']
                while keyup_key != keydown_key:
                    j += 1
                    keyup_key = df.at[j, 'key_code']

                # Calculate dwell time
                chars = [df.at[i, 'key_code'], df.at[i, 'shift_key']]
                feature = self.__get_dwell_feature(chars=chars)
                dwell_vals[feature] += \
                    df.at[j, 'timestamp'] - df.at[i, 'timestamp']
                dwell_cnts[feature] += 1

        # Replace dwell_vals sums with means
        for k in dwell_vals:
            if dwell_cnts[k] > 0:
                dwell_vals[k] = dwell_vals[k]/dwell_cnts[k]
        return dwell_vals

    def __get_cpm(self: FeatureExtractor, df: DataFrame) -> Dict:
        ''' Calculate characters per minute
            Parameters
            ----------
            self : FeatureExtractor instance
            df : All keystroke events for a sentence

            Returns
            -------
            Characters per minute for sentence
        '''
        cpm = len(df)/(df['timestamp'].iloc[-1] - df['timestamp'].iloc[0])*1000
        return {'cpm': cpm}

    def __get_features(self: FeatureExtractor, df: DataFrame) -> DataFrame:
        ''' Extract feature vector from sentence
            Parameters
            ----------
            self : FeatureExtractor instance
            df : All keystroke events for a sentence

            Returns
            -------
            Sentence feature vector
        '''
        df.reset_index(drop=True, inplace=True)

        # Get feature vectors
        flights = self.__get_flights(df)
        dwellings = self.__get_dwellings(df)
        cpm = self.__get_cpm(df)
        is_bot = {'is_bot': df.at[0, 'is_bot']}

        # Return as single dataframe
        sample_dict = dict(chain(
            flights.items(),
            dwellings.items(),
            cpm.items(),
            is_bot.items()
        ))
        return DataFrame(sample_dict, index=[0])

    def generate_features(self: FeatureExtractor) -> DataFrame:
        ''' Extract features from original dataset
            Parameters
            ----------
            self : FeatureExtractor instance

            Returns
            -------
            ret_dataset : All extracted features and data
        '''
        sentence_dfs = self.dataset.groupby(
            ['uuid', 'sentence_id'], group_keys=False
        )
        return sentence_dfs.apply(self.__get_features)
