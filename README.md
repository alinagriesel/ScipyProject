# ScipyProject

## Brief Project Description

- Dataset from ALLBUS 2018 - Gesis Variable Report - "Allgemeine Bevölkerungsumfrage der Sozialwissenschaften"
- Abortion Hypotheses:
  - Relation between response to abortion:
    - age (ordinal vs. metric) -> Pearson correlation or Kendall rank correlation
    - sex (ordinal vs. binary nominal) -> point biseral correlation
    - religiousness with christianity as denomination (ordinal vs. binary nominal) -> point biseral correlation


## (until) 19.07.2022
- 5 functions
  - create tidy dataframe for each hypothesis
  - print dataframe and summary statistic with mean, min, max, etc.
  - first hypothesis - group dataframe with count, sex and percentage of response proportion, inlcuding plotting
  - second hypothesis - ""
  - third hypothesis - ""
- Discussion which tests to use, we are looking for correlation tests, thus we consider Kendall, Pearson or Spearman. To determine which one to use for which hypothesis, we will check for their variance and whether variables are normally distributed
- so far we have categorised the variables of the Abortion Hypotheses as follows:
  - sex: nominal (binary)
  - age: metric
  - Response to Abortion: ordinal
  - Denomination: nominal (binary after change of values to christianity vs no religion)
  - Religious Assessment: norminal (ordinal as used in Allbus but after change of values to religious vs not religious it becomes a binary nominal variable)

  
## 20.07.2022
- helper function for percentage, mean and max response
- rewrite abortion_sex() and abortion_rel() to use helper function
