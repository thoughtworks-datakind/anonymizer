import pandas as pd
import sys

def parse(input_path, delimiter = ',') : 
    df = pd.read_csv(input_path, delimiter=delimiter)
    df = df.applymap(lambda x: len(str(x)))
    return df