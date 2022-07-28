from Functions import *

def tidy_abortion_summary():
    
    print('\033[1m' + 'Summary:' + '\033[0m')
    print("\n\033[4mFull Dataframe:\033[0m\n\n", tidy_abortion_df())
    # summary statistic
    print("\n\033[4m" + "Summary statistic:" + "\033[0m\n\n", tidy_abortion_df().describe(include='all')) 
    
    ind_histograms()
    participants_counts()
    
    return

tidy_abortion_summary()
