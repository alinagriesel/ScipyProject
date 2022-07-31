import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import scipy.stats as stats

pd.options.mode.chained_assignment = None

# helper function, used for abortion_sex() and abortion_rel()
def percentage_mean_max(df, quantity):
    """
    Adds a percentage column to the given dataframe and calculates a mean and max response
    
    Args:
        df (dataframe): A dataframe with 3 columns (one type of binary variable, response, counts)
        quantity (integer): Number of participants in that dataframe 
    
    Returns:
        df (dataframe): the input data frame with an added column for percentage 
        percentage_arr (numpy array): the percentage column as numpy array
        mean (float): mean response for given variable
        maxval (integer): maximum response for given variable
    """
    # add percenatge column to given df
    df["percentage"] = df["counts"]/quantity
    # get percentage array
    percentage_arr = df["percentage"].to_numpy()
    mean = df["counts"].to_numpy()@df["response to abortion"].to_numpy()/quantity
    maxval = df["response to abortion"].to_numpy()[df["counts"].to_numpy().argmax()]
    
    return df,percentage_arr, mean, maxval


def normal_shapiro(data, column, bins):
    """
    Check whether some data column is likely normally distributed using the Shapiro Wilk test and by displaying a histogram for the given data column for visualization
    
    Args:
        data (dataframe): -
        column (string): the column of the dataframe for which normality should be tested
        bins (integer): number of bins for the histogram 
    
    Returns:
        None
        
    Prints:
        Histogram
        Results of the Shapiro Wilk test
    """
    # histogram for given sample
    fig = px.histogram(data, x = column, nbins = bins, title = "Histogram for '"+ column + "'")
    fig.update_layout(bargap=0.2)
    fig.show()
    
    # shapiro wilk test 
    statistic, pvalue = stats.shapiro(data[column])
    print('\n\033[4m' + "Shapiro-Wilk Test:\n\n" + '\033[0m'+"Statistic: ", statistic, "\nP-value: ", pvalue)
    
    return

def tidy_abortion_df():
    """
    Create tidy dataframe with variables relevant for all 3 hypotheses concerning abortion
    
    Args:
        None
        
    Returns:
        abortion_df (dataframe): the dataframe that can be used to create an overview of the used data and for all hypotheses functions
        
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

def ind_histograms():
    """
    Displays a figure containing 5 histogram plots for each of the 5 variables used in the 3 hypotheses for visualization of the used data
    
    Args:
        None
    
    Returns:
        None
        
    Prints: 
        Figure containing 5 plots
    """
    # get relevant arrays fo reach variable
    df2 = tidy_abortion_df()
    x1 = df2["response to abortion"].to_numpy()
    x2 = df2["sex"].to_numpy()
    x3 = df2["age"].to_numpy()
    x4 = df2["denomination"].dropna().to_numpy()
    x5 = df2["religious assessment"].dropna().to_numpy()
    
    # set figure and add each histogram
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
    Displays a table containing the number of all participants that were used per hypothesis after excluding unfit participants/ rows
    
    Args:
        None
        
    Returns:
        None
        
    Prints: 
        dataframe with 2 columns, one for hypothesis and one for counts of participnats
    """
    # get row number of each in the end used dataframe 
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
    
    # put numbers together into pandas df
    data = {"Hypothesis": [1,2,3],
           "Participant counts": [len(abse_df), len(abag_df), len(abre_df)]
           }
    
    data_frame = pd.DataFrame(data)
    print("\n\033[4m" + "Number of participants used for each hypothesis:" + "\033[0m\n\n", data_frame)
    
    return


# Test for outlier deetction and removal, used in Hypothesis 1 for mean response as the graph for mean response indicates some outliers
def rosner_test(arrayy, arrayx):
    """
    Execute Rosner Test using the z value of values in data array to determine outliers and remove them. Z values over 3 are considered outliers.
    
    Args:
        arrayy (numpy array): Array of y values from which we want to determine outliers and remove them
        arrayx (numpy array): Array containing the x values where we also need to delete the values at index where arrayy has outliers 
        
    Returns:
        arrayy (numpy array): with removed outliers
        arrayx (numyp array): with removed x values for outlier y values
    """
    z_max = 4
    
    while z_max > 3:
        
        std = np.std(arrayy)
        mean = np.mean(arrayy)
        
        z_values = abs(arrayy-mean)/std
        z_max = max(z_values)
        z_max_index = z_values.argmax()
        
        if z_max > 3:
            arrayy = np.delete(arrayy, z_max_index)
            arrayx = np.delete(arrayx, z_max_index)
            
    return arrayy, arrayx