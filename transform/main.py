import pandas as pd
import numpy as np
import os
import argparse


def main(filename):
    df = pd.read_csv(filename)
    df = df.reindex(columns=[
        'city',
        'name',
        'address',
        'latitude',
        'longitude',
        ])


    filename_clean = filename[0:filename.index('_.csv')]
    df.to_csv('{}_clean.csv'.format(filename_clean),sep=',', index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                    help= 'The path to the dirty data',
                    type= str)

    arg = parser.parse_args()
    df = main(arg.filename)
