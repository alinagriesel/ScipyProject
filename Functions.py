import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import scipy.stats as stats

pd.options.mode.chained_assignment = None

""" FEHLT: Kommentare und DOCSTRINGS!!! """


# helper function, used for abortion_sex() and abortion_rel()
def percentage_mean_max(df, quantity):
    """
    doc:
    """
    
    df["percentage"] = df["counts"]/quantity
    percentage_arr = df["percentage"].to_numpy()
    mean = df["counts"].to_numpy()@df["response to abortion"].to_numpy()/quantity
    maxval = df["response to abortion"].to_numpy()[df["counts"].to_numpy().argmax()]
    
    return df,percentage_arr, mean, maxval

# helper function to check whether a sample is likely coming from a normal distribution
def normal_shapiro(data, column, bins):
    """
    Check whether some data column is likely normally distributed 
    """
    fig = px.histogram(data, x = column, nbins = bins, title = "Histogram for '"+ column + "'")
    fig.update_layout(bargap=0.2)
    fig.show()

    statistic, pvalue = stats.shapiro(data[column])
    print('\n\033[4m' + "Shapiro-Wilk Test:\n\n" + '\033[0m'+"Statistic: ", statistic, "\nP-value: ", pvalue)
    
    return

def tidy_abortion_df():
    """
    Create dataframe with variables relevant for all hypotheses concerning abortion
    """
    
    # load data
    df = pd.read_stata('data/data.dta', convert_categoricals = False)
    # choose relevant columns / variables  
    abortion_df = df[["sex", "age", "J005", "rd01", "J029"]]
    # remove all values below 0 of abortion response, as negative values indicate not apllicable
    abortion_df = abortion_df[(abortion_df.J005 > 0)]
    # rename columns
    abortion_df = abortion_df. rename(columns = {"J005": "response to abortion", "rd01": "denomination", "J029": "religious assessment"})
    # rename values 
    abortion_df = abortion_df.replace({"sex": {1: "male", 2: "female"},
                                      "denomination": {1: "protestant church (w.o. free church)", 2: "protestant church", 3: "roman catholic church", 4: "other christian religious group", 5: "other non christian religious group", 6: "no religious group", -9: np.nan, -7: np.nan},
                                      "religious assessment": {1: "deeply religious", 2: "very religious", 3: "rather religious", 4: "neither nor", 5: "rather not religious", 6: "not religious", 7: "not religious at all", -13: np.nan, -12: np.nan, -9: np.nan, -8: np.nan}})  
    
    return abortion_df

# kommentare+doc !!
def ind_histograms():
    """
    doc:
    """
    
    df2 = tidy_abortion_df()
    x1 = df2["response to abortion"].to_numpy()
    x2 = df2["sex"].to_numpy()
    x3 = df2["age"].to_numpy()
    x4 = df2["denomination"].dropna().to_numpy()
    x5 = df2["religious assessment"].dropna().to_numpy()
    
    fig, ax = plt.subplots(2, 3, figsize=(10,7))
    fig.suptitle("Histogram for each individual variable", fontsize=20)
    
    ax[0,0].hist(x1)
    ax[0,0].set_title("Response to Abortion")
    ax[0,0].set_ylabel("counts")
    
    ax[0,1].hist(x2)
    ax[0,1].set_title("Sex")
    ax[0,1].set_ylabel("counts")
    
    ax[0,2].hist(x3, bins = 30, rwidth=0.7)
    ax[0,2].set_title("Age")
    ax[0,2].set_ylabel("counts")
    
    ax[1,0].hist(x4, rwidth=0.7)
    ax[1,0].set_title("Denomination")
    ax[1,0].tick_params(axis='x', labelrotation = 90)
    ax[1,0].set_ylabel("counts")
    
    ax[1,1].hist(x5, rwidth=0.7)
    ax[1,1].set_title("Religious Assessment")
    ax[1,1].tick_params(axis='x', labelrotation = 90)
    ax[1,1].set_ylabel("counts")
    
    fig.delaxes(ax[1][2])
    fig.tight_layout()
    plt.show()
    
    return 

def participants_counts():
    """
    doc:
    """
    df = tidy_abortion_df()
    abse_df = df[["sex", "response to abortion"]]
    
    abag_df = df[["age", "response to abortion"]]
    abag_df = abag_df.dropna()
    
    abre_df = df[["response to abortion", "denomination", "religious assessment"]]
    abre_df = abre_df.dropna()
    abre_df = abre_df[(abre_df["denomination"] != "other non christian religious group") & (abre_df["religious assessment"] != "neither nor" )]
    abre_df["religious assessment"] = abre_df["religious assessment"].replace(["deeply religious", "very religious", "rather religious"],"religious").replace(["rather not religious", "not religious", "not religious at all"], "not religious")
    abre_df["denomination"] = abre_df["denomination"].replace(["protestant church (w.o. free church)", "protestant church", "roman catholic church", "other christian religious group"],"christian")
    index_names = abre_df[(abre_df["religious assessment"] == "religious") & (abre_df["denomination"] == "no religious group")].index
    abre_df.drop(index_names, inplace = True)
    
    data = {"Hypothesis": [1,2,3],
           "Participant counts": [len(abse_df), len(abag_df), len(abre_df)]
           }
    
    data_frame = pd.DataFrame(data)
    print("\n\033[4m" + "Number of participants used for each hypothesis:" + "\033[0m\n\n", data_frame)
    
    return