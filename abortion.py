import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None

def tidy_abortion_df():
    """ make whole given dataframe smaller and tidier for ownspecific purpose"""
    
    df = pd.read_stata('data/data.dta', convert_categoricals = False)
    
    # choose relevant columns / variables  
    abortion_df = df[["sex", "age", "J005", "rd01", "J029"]]
    # remove all values below 0, as negative values indicate not apllicable
    abortion_df = abortion_df[(abortion_df.J005 > 0) & (abortion_df.J029 > 0) & (abortion_df.rd01 > 0)]
    # rename columns
    abortion_df = abortion_df. rename(columns = {"J005": "response to abortion", "rd01": "denomination", "J029": "religious assessment"})
    # rename values 
    abortion_df = abortion_df.replace({"sex": {1: "male", 2: "female"},
                                      "denomination": {1: "protestant church (w.o. free church)", 2: "protestant church", 3: "roman catholic church", 4: "other christian religious group", 5: "other non christian religious group", 6: "no religious group"},
                                      "religious assessment": {1: "deeply religious", 2: "very religious", 3: "rather religious", 4: "neither nor", 5: "rather not religious", 6: "not religious", 7: "not religious at all"}})
    
    return abortion_df
    
