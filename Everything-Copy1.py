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
    print('\033[4m' + "Shapiro-Wilk Test:\n\n" + '\033[0m'+"Statistic: ", statistic, "\nP-value: ", pvalue)
    
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
    fig.show()
    
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

def tidy_abortion_summary():
    
    print('\033[1m' + 'Summary:' + '\033[0m')
    print("\n\033[4mFull Dataframe:\033[0m\n\n", tidy_abortion_df())
    # summary statistic
    print("\n\033[4m" + "Summary statistic:" + "\033[0m\n\n", tidy_abortion_df().describe(include='all')) 
    
    ind_histograms()
    participants_counts()
    
    return
  


def abortion_age():
    """
    doc:
    """
    
    print("\n" + '\033[1m' + 'Hypothesis 1: Is there a any relation between the response to abortion and the age?' + '\033[0m')
    
    # choose relevant columns and remove rows containing nans
    abortion_df = tidy_abortion_df()
    abag_df = abortion_df[["age", "response to abortion"]]
    abag_df = abag_df.dropna()
    
    # grouped df
    abag_group_df = abag_df.groupby(["age","response to abortion"]).value_counts().reset_index()
    abag_group_df = abag_group_df.rename(columns = {0:"counts"})
    print("\n\033[4mGrouped Dataframe:\033[0m\n\n",abag_group_df)
    
    # get mean and max response to abortion from each age group
    counts = abag_group_df['counts'].to_numpy()
    ages = abag_group_df['age'].to_numpy()
    values = abag_group_df['response to abortion'].to_numpy()
    
    individual_ages = set(ages)
    mean_values = []
    max_values = []
    
    for element in individual_ages:
        inter = 0
        counter = 0
        mval = 0
        m = 0
        for i,val in enumerate(ages):
            if val == element:
                inter += values[i]*counts[i]
                counter += counts[i]
                
                if counts[i] > mval:
                    mval = counts[i]
                    m = values[i]
                
        mean_values.append(inter/counter)
        max_values.append(m)
    
    # summary df containing each age group and the mean and max response to abortion
    zipped = list(zip(individual_ages, mean_values, max_values))
    summary_df = pd.DataFrame(zipped, columns = ["Age", "Mean Response", "Max Response"])
    print("\n\033[4mSummary:\033[0m\n\n",summary_df)    
    
    # scatterplots for mean and max response
    fig1 = px.scatter(x = list(individual_ages), y = mean_values, 
                      labels = {
                                "x": "age",
                                "y": "Mean response to abortion of every age"   
                            },
                      title = "Mean response to abortion of every age")
    fig1.show()
    
    fig2 = px.scatter(x = list(individual_ages), y = max_values, 
                      labels = {
                                "x": "age",
                                "y": "Max response to abortion of every age"   
                            },
                      title = "Max response to abortion of every age",)
    fig2.update_yaxes(dtick=list(set(max_values)))
    fig2.show()
    
    
    # check whether the age column is normally distributed
    normal_shapiro(abag_df, "age", 40)
    
    # Hypothesis Test
    age_arr = abag_df["age"].to_numpy()
    response_arr = abag_df["response to abortion"].to_numpy()
    
    correlation, pvalue = stats.kendalltau(age_arr, response_arr)
    print('\n\033[4m' + "Kendall's Tau Correlation Test:\n\n" + '\033[0m'+"Correlation: ", correlation, "\nP-value: ", pvalue)

    
    return 

def abortion_sex():
    """
    Check for correlation between sex and response to abortion by counting responses
    of males and females and plotting the percentage
    """
    
    print("\n" + '\033[1m' + 'Hypothesis 2: Is there any relation between the response concerning abortion and sex?' + '\033[0m')
    
    # choosing relevant columns
    abortion_df = tidy_abortion_df()
    abse_df = abortion_df[["sex", "response to abortion"]]
        
    # group_by
    abse_group_df = abse_df.groupby(["sex","response to abortion"]).value_counts().reset_index()
    abse_group_df = abse_group_df.rename(columns = {0:"counts"})
    
    # get counts of how many males and how many females 
    quantity = abse_df["sex"].value_counts()
    quantity_males = np.asarray(quantity)[0]
    quantity_females = np.asarray(quantity)[1]
    
    # split df for males and females 
    females_df = abse_group_df[:4]
    males_df = abse_group_df[4:]
    
    values = males_df["response to abortion"].to_numpy()
    
    # use function to get percentage, mean and max values respectively 
    females_df, females_percentage, mean_female_response, max_female_response = percentage_mean_max(females_df, quantity_females)
    males_df, males_percentage, mean_male_response, max_male_response = percentage_mean_max(males_df, quantity_males)

    # add percentage to grouped df
    abse_group_df = pd.concat([females_df, males_df])
    print("\n\033[4mGrouped Dataframe:\033[0m\n\n",abse_group_df, "\n")
    
    # summary df with mean and max response
    zipped = list(zip(set(abse_df["sex"].to_numpy()), [mean_male_response, mean_female_response], [max_male_response, max_female_response]))
    summary_df = pd.DataFrame(zipped, columns = ["Age", "Mean Response", "Max Response"])
    print("\n\033[4mSummary:\033[0m\n\n",summary_df)
    
    # line plot for response to abortion of males and females in percentage 
    
    plot = go.Figure(data=[go.Scatter(
        name='Males',
        x=values,
        y=males_percentage, 
    ),
        go.Scatter(
        name='Females',
        x=values,
        y=females_percentage,
        line_color = "red"
    )
    ])
    
    plot.update_xaxes(dtick=values)
    plot.update_xaxes(title="Response to abortion in numeric values")
    plot.update_yaxes(title="Percentage")
    
        # Add dropdown
    plot.update_layout(
        updatemenus=[
            
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Both"},
                              ]),
                               
                    
                    dict(label="Males",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Male response to abortion",
                                }]),
                    
                    dict(label="Females",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Female response to abortion",
                                }]),
                ]),
            )
        ])
      
    plot.show()
    
    # Hypothesis test
    sex_arr = abse_df["sex"].to_numpy()
    sex_bool = sex_arr == "male"
    response_arr = abse_df["response to abortion"].to_numpy()
    
    correlation, pvalue = stats.pointbiserialr(sex_bool, response_arr)
    
    print('\033[4m' + "Point-Biserial Correlation Test:\n\n" + '\033[0m'+"Correlation: ", correlation, "\nP-value: ", pvalue)
    
    return       
   

def abortion_rel():
    """
    doc:
    """
    
    print("\n" + '\033[1m' + 'Hypothesis 3: Is there any relation between the response to abortion and christian religious assessment?' + '\033[0m')
    
    # choose relevant columns and drop nan rows 
    abortion_df = tidy_abortion_df()
    abre_df = abortion_df[["response to abortion", "denomination", "religious assessment"]]
    abre_df = abre_df.dropna()
    # also drop rows on two other conditions
    abre_df = abre_df[(abre_df["denomination"] != "other non christian religious group") & (abre_df["religious assessment"] != "neither nor" )]
    
    # merge some values 
    abre_df["religious assessment"] = abre_df["religious assessment"].replace(["deeply religious", "very religious", "rather religious"],"religious").replace(["rather not religious", "not religious", "not religious at all"], "not religious")
    abre_df["denomination"] = abre_df["denomination"].replace(["protestant church (w.o. free church)", "protestant church", "roman catholic church", "other christian religious group"],"christian")
    
    # drop combination of religious self assessment and no religious denomination
    index_names = abre_df[(abre_df["religious assessment"] == "religious") & (abre_df["denomination"] == "no religious group")].index
    abre_df.drop(index_names, inplace = True)
    
    # groupby
    abre_group_df = abre_df[["religious assessment", "response to abortion"]].groupby(["religious assessment", "response to abortion"]).value_counts().reset_index()
    abre_group_df = abre_group_df.rename(columns = {0:"counts"})   
    
    # get amount of religious and not religious people
    quantity = abre_df["religious assessment"].value_counts()
    quantity_nr = np.asarray(quantity)[0]
    quantity_r = np.asarray(quantity)[1]
    
    # split df into two for religious and not religious respectively
    nr_df = abre_group_df[:4]
    r_df = abre_group_df[4:]
    
    # response values (1 to 4)
    values = nr_df["response to abortion"].to_numpy()
    
    # use function to get percentage, mean and max response respectively
    nr_df, nr_percentage, mean_nr_response, max_nr_response = percentage_mean_max(nr_df, quantity_nr)
    r_df, r_percentage, mean_r_response, max_r_response = percentage_mean_max(r_df, quantity_r)
    
    # add percentage to grouped df
    abre_group_df = pd.concat([nr_df, r_df])
    print("\n\033[4mGrouped Dataframe:\033[0m\n\n",abre_group_df)
    
    # summray df with mean and max repsonse
    zipped = list(zip(set(abre_df["religious assessment"].to_numpy()), [mean_r_response, mean_nr_response], [max_r_response, max_nr_response]))
    summary_df = pd.DataFrame(zipped, columns = ["Religiousness", "Mean Response", "Max Response"])
    print("\n\033[4mSummary:\033[0m\n\n",summary_df)

    # line plot for response to abortion in percentage 
    
    plot = go.Figure(data=[go.Scatter(
        name ='Religious',
        x = values,
        y = r_percentage, 
    ),
        go.Scatter(
        name='Not Religious',
        x = values,
        y = nr_percentage,
        line_color = "red"
    )
    ])
    
    plot.update_xaxes(dtick=values)
    plot.update_xaxes(title="Response to abortion in numeric values")
    plot.update_yaxes(title="Percentage")
    
    # Add dropdown
    plot.update_layout(
        updatemenus=[
            
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True]},
                               {"title": "Both Religious assessment types and their response to abortion",
                               }]),
                               
                    
                    dict(label="Religious",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Religious self assessment and response to abortion",
                                }]),
                    
                    dict(label="Not Religious",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Not Religious self assessment and response to abortion",
                                }]),
                ]),
            )
        ])
      
    plot.show()
    
    
    # Hypothesis test
    rel_arr = abre_df["religious assessment"].to_numpy()
    rel_bool = rel_arr == "religious"
    response_arr = abre_df["response to abortion"].to_numpy()
    
    correlation, pvalue = stats.pointbiserialr(rel_bool, response_arr)
    
    print('\033[4m' + "Point-Biserial Correlation Test:\n\n" + '\033[0m'+"Correlation: ", correlation, "\nP-value: ", pvalue)
    
    return 
      
tidy_abortion_summary()
abortion_age()
abortion_sex()
abortion_rel()