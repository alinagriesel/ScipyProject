import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None


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

def tidy_abortion_summary():
    
    print('\033[1m' + 'Summary:' + '\033[0m')
    print("\nFull Dataframe: \n\n", tidy_abortion_df())
    # summary statistic
    print("\nSummary statistic: \n\n", tidy_abortion_df().describe(include='all'))   
    
    return 


# could still add mean and max response of males and females to summarizing df 
# test still missing
def abortion_sex():
    """
    Check for correlation between sex and response to abortion by counting responses
    of males and females and plotting the percentage
    """
    
    print("\n" + '\033[1m' + 'Hypothesis 1: Is there any relation between the response concerning abortion and sex?' + '\033[0m')
    
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
    
    # get percentage of male and female counts on response to abortion
    males_df["percentage"] = males_df["counts"]/quantity_males
    females_df["percentage"] = females_df["counts"]/quantity_females
    
    males_percentage = males_df["percentage"].to_numpy()
    females_percentage = females_df["percentage"].to_numpy()
    
    values = males_df["response to abortion"].to_numpy()
    
    # add percentage to grouped df
    abse_group_df = pd.concat([females_df, males_df])
    print("\n Grouped Dataframe: \n\n",abse_group_df, "\n")
    
    # line plot for response to abortion of males and females in percentage 
    plt.plot(values, males_percentage, 'o-g')
    plt.plot(values, females_percentage, 'o-b')
    plt.legend(['males', 'females'])
    plt.title("Response to abortion depending on sex in percentage\n")
    plt.xlabel("Response to abortion in numeric values")
    plt.ylabel("percentage")
    plt.xticks(ticks=values, labels=values)
    plt.show()
    
    return   


# Fehlt: test
# Fehlt: plot beschriftung
# Idee: plot mit shared x axis anstat zwei plots komplett individuell 
# könnte man noch machen: die dfs zusammen führen als eins 
# könnte man noch machen: age bins und nochmal alles 
def abortion_age():
    """
    doc:
    """
    
    print("\n" + '\033[1m' + 'Hypothesis 2: Is there a any relation between the response to abortion and the age?' + '\033[0m')
    
    # choose relevant columns and remove rows containing nans
    abortion_df = tidy_abortion_df()
    abag_df = abortion_df[["age", "response to abortion"]]
    abag_df = abag_df.dropna()
    
    # grouped df
    abag_group_df = abag_df.groupby(["age","response to abortion"]).value_counts().reset_index()
    abag_group_df = abag_group_df.rename(columns = {0:"counts"})
    print("\nGrouped Dataframe:\n\n",abag_group_df)
    
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
    print("\nSummary:\n\n",summary_df)    
    
    # scatterplots for mean and max response
    plt.scatter(list(individual_ages), mean_values)
    plt.title("Mean response to abortion of every age")
    plt.xlabel("ages")
    plt.ylabel("numeric response to abortion")
    plt.show()
    plt.scatter(list(individual_ages), max_values)
    plt.title("Max response to abortion of every age")
    plt.xlabel("ages")
    plt.ylabel("numeric response to abortion")
    plt.yticks(list(set(max_values)), list(set(max_values)) )
    plt.show()
    
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
    
    # get percentage of response 
    nr_df["percentage"] = nr_df["counts"]/quantity_nr
    r_df["percentage"] = r_df["counts"]/quantity_r
    
    nr_percentage = nr_df["percentage"].to_numpy()
    r_percentage = r_df["percentage"].to_numpy()
    
    values = nr_df["response to abortion"].to_numpy()
    
    # add percentage to grouped df
    abre_group_df = pd.concat([nr_df, r_df])
    print("\nGrouped Dataframe:\n\n",abre_group_df)
    
    # line plot 
    plt.plot(values, nr_percentage, 'o-g')
    plt.plot(values, r_percentage, 'o-b')
    plt.legend(['not religious', 'religious'])
    plt.title("Response to abortion depending on religious self assessemnt in percentage\n")
    plt.xlabel("Response to abortion in numeric values")
    plt.ylabel("percentage")
    plt.xticks(ticks=values, labels=values)
    plt.show()
    
    return 
     
    