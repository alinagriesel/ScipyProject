# ScipyProject

## Overview:

- Section I: 	Project idea and structure
- Section II: 	Requirements
- Section III: 	General information on dataset
- Section IV: 	Explanation of relevant variables and corresponding hypotheses
- Section V: 	Instructions for the use of our code 
- Section VI: 	Interpretation of Outputs / Hypotheses testings
- Reference


## Section I: Project idea and structure

This project is a data analysis mainly comprising 3 different hypotheses, all of which however revolve around the topic of abortion. In preparation for the project, we were looking for an interesting dataset to work with after settling on the idea to conduct a data analysis. We came across an open source dataset corresponding to a general public survey, conducted by the GESIS Leibniz Institute for the Social Sciences (Diekmann et al., 2019). The variable report was published in 2019 and contains a number of survey questions from various fields such as politics, economy, social injustices or religion. The latter one especially caught our interest as it also addresses questions regarding ones stance on abortion. Recent public and political debates in the United States give rise to the question as to what opinion the German population advocates in general and depending on different factors as will be outlined in Section III.
Our analysis can roughly be structured into preprocessing of data through data-wrangling, plotting for data visualisation, and applying appropriate statistical correlation testings to prepared data. Overall, we have decided on three hypotheses for which we finally present and interpret the results.


## Section II: General information on dataset

As briefly touched upon above, the dataset represents the participant’s responses to a large number of different questions. Each question functions as a variable, thus occupying one column respectively, and represented by a short reference code within the dataset. The responses also follow a specific schemata which uses numeric values to refer to response possibilities which are further clarified in the ALLBUS Variable Report published alongside the dataset. This report provides a thorough and extensive explanation for every single variable/question and their respective response possibilities. After each explanation, a short summary statistics provides some general information on e.g. count and percentage corresponding to each response possibility.
In total, 3477 people participated in the study. However, not all participants gave responses to every question. Since we focus on the particular topic of abortion, the participant count for each variable varies between 1259 and 1570.


## Section III: Explanation of relevant variables and corresponding hypotheses

### Variables
`J005 – abortion at low income`

The main question we want to raise seeks for an overall picture on how bad Germans regard an abortion, given that the family only possesses a low income which would not suffice to raise a child. This question corresponds to the variable J005 – abortion at low income. The response possibilities that are of interest to us are ‘always bad’, ‘nearly always bad’, ‘only sometimes bad’ and ‘never bad’, with the numeric references from 1 to 4 respectively within the dataset, adding up to 1575 relevant responses. Negative response numbers represent answers such as ‘not specified’ or ‘no participation’ which we therefore exclude during data wrangling
The hypotheses test this variable against 3 other variables, namely age, sex and religiousness (conditioned on denomination (rd01) prior to hypothesis testing). Age and sex are two of only a few variable names which are used as they are within the dataset.

`age`

The data points for age have been generated using the year of birth as indicated by the participants. Negative response numbers refer to cases in which the age could not be generated and which we therefore exclude during data wrangling. There is a total of 3472 data points for age.

`sex`

The variable sex only differentiates between the responses ‘male’ and ‘female’, 1 and 2 respectively in the dataset. It is important to mention here, that the interviewer themselves were responsible to fill out this point for each participant without asking them. No other sex category was included and thus all 3477 participants were assigned either male or female. We believe this to be critical and suggest that one should look at correlation tests with caution. Nevertheless, we believe it is sufficient to provide some indication for possible sex differences. Altogether, 1777 participants were assigned to be male and 1700 participants were assigned to be female. The proportion between the two sexes is therefore quite even.

`religiousness`

The variable J029 in the dataset, which we changed to religiousness, denotes the participant’s personal assessment of how religious they are. The response possibilities are (1)‘deeply religious’, (2)‘very religious’, (3)‘rather religious’, (5)‘rather not religious’, (6)‘not religious’ and (7)‘not religious at all’. The numbers in parentheses refer to the numeric reference within the dataset.
Since we are only interested in whether religion plays a role, we have merged the response possibilities to two binary responses wherein 1-3 represent ‘religious’ (616 participants) and 5-7 represent ‘not religious’ (845 participants). Furthermore, we have excluded response possibility 4, as it denotes ‘neither religious nor not religious which would not be suitable for either aspect of our binary category. We have also excluded all negative response numbers as they refer to e.g. ‘not specified’ or ‘no participation’.
In addition to this, we are only interested in people who are most likely Christian in order to not confuse different religious and their possibly opposing ideologies. We therefore used another variable, namely rd01 – denomination, in order to further exclude all people who are religious but do not have Christianity as their denomination. Thus, our final religiousness variable comprises two response possibilities, either (Christian) religious or not religious.

### Hypotheses
`Hypothesis 1`

First of all, we want to know whether there are significant differences in the response to abortion among different age groups. Since the response to abortion is an ordinal variable and age a metric one, we can either use the Pearson Correlation test (parametric) or the Kendall Tau Correlation test (non-parametric). The former should only be applied if we know that the relevant variables follow a normal distribution as this is pre-assumed by the test. We therefore checked the distribution of the age data points using the Shapiro-Wilk test. Although age usually follows a normal distribution, it does not do so in our case (further explained in Section VI), perhaps due to the low amount of participants or other biases influencing which people end up as participants. We therefore choose the Kendall Tau Correlation test.

`Hypothesis 2`

Secondly, we want to know whether the responses to abortion vary between the two sexes. Since response to abortion is an ordinal variable and the sex is a binary nominal one, we cannot use the Kendall Tau Correlation test, nor the Pearson Correlation test. In order to account for a binary nominal variable, we make use of the Point Biseral Correlation test.

`Hypothesis 3`

Finally, we are interested in the role of religiousness when it comes to stances on abortion, whether (Christian) religious people tend to give different responses to abortion than non religious people. After the changes to the response possibilities which we have made earlier, depending on the participant’s denomination, we are left with a binary nominal variable. Therefore, as in H2, we will use the Point Biseral Correlation test again.


## Section IV: Requirements and table of files

### Requirements
In order to execute our code, there are a few things you need to have installed and prepared. First of all, we have worked with Python 3.10.4 so this version should definitely work. Next, there are a few packages required. You can install all at once with the use of the provided `requirements.txt` file and a command like:

    pip install -r requirements.txt


### Table of files

- folder `data` contains:
    -  ZA5272_v1-0-0.dta (data set as we have downloaded it from GESIS Website
    -  data.csv (which we do not use but which some may prefer to work with)
    -  data.dta (which we are working with in our code)
- `README.md`
- `requirements.txt`

- `Functions.py` (contains 4 functions which are used by other py files but which does not give any output to the user)
- `Overwiev.py` (tidy data frame, summary statistic, histogram for each individual variable, number of participants for each hypothesis)
- `Hypothesis1.py` (response to abortionn - age)
- `Hypothesis2.py` (response to abortionn - sex)
- `Hypothesis3.py` (response to abortionn - religiousness)

- `test_notebook` (during the development of the code, we have worked with a notebook for convenience. Feel free to check it out and run individual codes in cells as you like)


## Section V: Instructions for the use of our code 

After installing python and all necessary packages, you can choose which hypothesis you would like to look at and run e.g. the following command with the corresponding hypothesis py file:

    python Hypothesis1.py

"Hypothesis1" can therein be exchanged by any py file you would like to execute. We would recommend you run the `Overview.py` file in order to gain some feeling for the variables and responses.
The following Section includes our interpretation of the correlation tests. Feel free to read through it while having the graphs and test results open.


## Section VI: Interpretation of Outputs / Hypotheses testings

Results of Correlation Tests provide a Correlation Coefficient which is a value representing the effect size, ranging from -1 to 1 wherein -1 refers to a perfect negative correlation, i.e. as Variable1 increases, Variable2 decreases, 0 refers to no detectable correlation and 1 is a perfect positive correlation, i.e. if Variable1 increases, Variable2 does so as well. There are different ways of interpreting the values between these extremes but we will focus on a general coefficient analysis which declares 0.2-0.4, 0.4-0.6 and above 0.6 to be a weak, moderate or strong correlation respectively. (Dixon, 2021)


`Hypothesis 1 - Response to abortion vs age - Interpretation`

In order to determine which correlation test to use in this case, as mentioned above, we conducted the Shapiro-Wilk Test to check whether `age` is normally distributed. The test Statistic has a value of ~0.98 and a P-value of ~1.83e^-14. Both values indicate that we can very likely reject the null hypothesis, meaning, we cannot assume a normal distribution and should rather use a non-parametric correlation test such as the Kendall Tau Correlation test.
This test results in a correlation coefficient of ~0.008 which is very small and stands for basically no detectable correlation. The p-value of ~0.66 also does not support a significant result if one takes 0.05 as the significance threshold, as usually done.
Thus, there is no evidence for a correlation between responses to abortion and age. After creating the scatterplot, we have already expected to find no correlation as all data points are evenly, horizontally distributed.


`Hypothesis 2 - Response to abortion vs sex - Interpretation`

For the second hypothesis we used the Point-Biseral Correlation Test. Its Correlation Coeffcient results in ~-0.025 which again, does not speak in favour of a correlation. Similarly, the p-value of ~0.32 is also no indication of a significant correlation. The hypothesis that sex plays a role in responses to abortion can therefore also be rejected. This is also to no surprise after plotting the data as the plot-lines for females and males behave very similar.


`Hypothesis 3 - Response to abortion vs religiousness - Interpretation`

For the last hypothesis we also used the Point-Biseral Correlation Test. Contrary to the former hypotheses, the Coefficient ~-0.27 shows some weak correlation between religiousness and responses to abortion. Note the negative sign which speaks for a weak negative correlation. Besides this and also contrary to the former two hypothesis results, the p-value is highly significant with a value of ~2.76e^-22. Therefore, we can accept the hypothesis that there is a weak correlation between responses to abortion and whether someone is (Christian) religious or not.
Considering this result in combination with the scatter plot we have created,(Christian) Religious people seem a bit more likely to militate against abortion. Keep in mind that "response to abortion" is conditioned on the fact that the family only has low income and would not be able to provide for the child. Unfortunately, we do not have data for responses to abortion in general. Results may have been different or arguably more severe in this case.
There may be one objection one could raise which suggests that older people are more likely to be religious and conservative und thus age could be a bias distorting the correlation measurement. However, since we have checked for an age-dependency in the first hypothesis, we believe this to be relevant to the current hypothesis.

    
## Reference
Diekmann, A., Hadjar, A., Kurz, K., Rosar, U., Wagner, U., Westle, B., & Kantar Public, M. (2019). Allgemeine Bevölkerungsumfrage der Sozialwissenschaften ALLBUS 2018. GESIS - Leibniz-Institut für Sozialwissenschaften. Retrieved from https://search.gesis.org/research_data/ZA5270?doi=10.4232/1.13250

Dixon, T. (2021). How to evaluate correlational studies....PROPERLY! | IB Psychology. IB Psychology. Retrieved 29 July 2022, from https://www.themantic-education.com/ibpsych/2021/02/25/how-to-evaluate-correlational-studies-properly/.

