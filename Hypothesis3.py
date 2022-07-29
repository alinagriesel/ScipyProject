from Functions import *

# Hypothesis 3
def abortion_rel():
    """
    The function displays the results for the third Hypothesis: Is there a relation between the response to abortion and religiousness?
    
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
    
    # add buttons to decide what graph should be displayed (both, religious response, not religious response)
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
    
    
    # Point Biserial hypothesis test
    rel_arr = abre_df["religious assessment"].to_numpy()
    rel_bool = rel_arr == "religious"
    response_arr = abre_df["response to abortion"].to_numpy()
    
    correlation, pvalue = stats.pointbiserialr(rel_bool, response_arr)
    
    print('\n\033[4m' + "Point-Biserial Correlation Test:\n\n" + '\033[0m'+"Correlation: ", correlation, "\nP-value: ", pvalue)
    
    return

abortion_rel()
