from Functions import *

# hypothesis 2 
def abortion_sex():
    """
    The function displays the results for the second Hypothesis: Is there a relation between the response to abortion and sex?
    
    Args:
        None
        
    Results:
        None
        
    Prints:
        Grouped dataframe
        Summary dataframe
        Scatterplot 
        Point Biserial hypothesis test results
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
    
    # scatter plot with connections between points for response to abortion of males and females in percentage 
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
    
    # add buttons to decide/ switch between graphs being displayed (options: both, male response, female response)
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
    
    # Point Biserial hypothesis test
    sex_arr = abse_df["sex"].to_numpy()
    sex_bool = sex_arr == "male"
    response_arr = abse_df["response to abortion"].to_numpy()
    
    correlation, pvalue = stats.pointbiserialr(sex_bool, response_arr)
    
    print('\n\033[4m' + "Point-Biserial Correlation Test:\n\n" + '\033[0m'+"Correlation: ", correlation, "\nP-value: ", pvalue)
    
    return

abortion_sex()