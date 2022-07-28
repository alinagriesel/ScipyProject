from Functions import *

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

abortion_age()