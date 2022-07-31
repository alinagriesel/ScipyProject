from Functions import *

# Overview/summary print function
def tidy_abortion_summary():
    """
    Displays the full tidy dataframe used for all hypotheses, a summary statistic, a histogram plot for each variable and the counts of all participants per hypothesis
    
    Args:
        None
    Returns:
        None
    Prints:
        Full dataframe
        Summary statistic
        5 histograms
        Participant counts per hypothesis
    """
    
    print('\033[1m' + 'Summary:' + '\033[0m')
    print("\n\033[4mFull Dataframe:\033[0m\n\n", tidy_abortion_df())
    # summary statistic
    print("\n\033[4m" + "Summary statistic:" + "\033[0m\n\n", tidy_abortion_df().describe(include='all')) 
    
    ind_histograms()
    participants_counts()
    
    return

tidy_abortion_summary()
