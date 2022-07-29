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

This project is a data analysis mainly comprising 3 different hypotheses, all of which however revolve around the topic of abortion. In preparation for the project, we were looking for an interesting dataset to work with after settling on the idea to conduct a data analysis. We came across an open source dataset corresponding to a general public survey, conducted by the GESIS Leibniz Institute for the Social Sciences (Diekmann et al., 2019). The variable report was published in 2019 and contains a number of survey questions from various fields such as politics, economy, social injustices or religion. The latter one especially caught our interest as it also addresses questions regarding ones stance on abortion. Recent public and political debates in the United States give rise to the question as to what opinion the German population advocates in general and depending on different factors as will be outlined in Section IV.
Our analysis can roughly be structured into preprocessing of data through data-wrangling, plotting for data visualisation, and applying appropriate statistical correlation testings to prepared data. Overall, we have decided on three hypotheses for which we finally present and interpret the results.


## Section II: General information on dataset

As briefly touched upon above, the dataset represents the participant’s responses to a large number of different questions. Each question functions as a variable, thus occupying one column respectively, and represented by a short reference code within the dataset. The responses also follow a specific schemata which uses numeric values to refer to response possibilities which are further clarified in the ALLBUS Variable Report published alongside the dataset. This report provides a thorough and extensive explanation for every single variable/question and their respective response possibilities. After each explanation, a short summary statistics provides some general information on e.g. count and percentage corresponding to each response possibility.
In total, 3477 people participated in the study. However, not all participants gave responses to every question. Since we focus on the particular topic of abortion, the participant count for each variable varies between 1259 and 1570.


## Section III: Explanation of relevant variables and corresponding hypotheses

### Variables
    J005 – abortion at low income
The main question we want to raise seeks for an overall picture on how bad Germans regard an abortion, given that the family only possesses a low income which would not suffice to raise a child. This question corresponds to the variable J005 – abortion at low income. The response possibilities that are of interest to us are ‘always bad’, ‘nearly always bad’, ‘only sometimes bad’ and ‘never bad’, with the numeric references from 1 to 4 respectively within the dataset, adding up to 1575 relevant responses. Negative response numbers represent answers such as ‘not specified’ or ‘no participation’ which we therefore exclude during data wrangling
The hypotheses test this variable against 3 other variables, namely age, sex and religiousness (conditioned on denomination (rd01) prior to hypothesis testing). Age and sex are two of only a few variable names which are used as they are within the dataset.

    age
The data points for age have been generated using the year of birth as indicated by the participants. Negative response numbers refer to cases in which the age could not be generated and which we therefore exclude during data wrangling. There is a total of 3472 data points for age.

    sex
The variable sex only differentiates between the responses ‘male’ and ‘female’, 1 and 2 respectively in the dataset. It is important to mention here, that the interviewer themselves were responsible to fill out this point for each participant without asking them. No other sex category was included and thus all 3477 participants were assigned either male or female. We believe this to be critical and suggest that one should look at correlation tests with caution. Nevertheless, we believe it is sufficient to provide some indication for possible sex differences. Altogether, 1777 participants were assigned to be male and 1700 participants were assigned to be female. The proportion between the two sexes is therefore quite even.

    religiousness
The variable J029 in the dataset, which we changed to religiousness, denotes the participant’s personal assessment of how religious they are. The response possibilities are (1)‘deeply religious’, (2)‘very religious’, (3)‘rather religious’, (5)‘rather not religious’, (6)‘not religious’ and (7)‘not religious at all’. The numbers in parentheses refer to the numeric reference within the dataset.
Since we are only interested in whether religion plays a role, we have merged the response possibilities to two binary responses wherein 1-3 represent ‘religious’ (616 participants) and 5-7 represent ‘not religious’ (845 participants). Furthermore, we have excluded response possibility 4, as it denotes ‘neither religious nor not religious which would not be suitable for either aspect of our binary category. We have also excluded all negative response numbers as they refer to e.g. ‘not specified’ or ‘no participation’.
In addition to this, we are only interested in people who are most likely Christian in order to not confuse different religious and their possibly opposing ideologies. We therefore used another variable, namely rd01 – denomination, in order to further exclude all people who are religious but do not have Christianity as their denomination. Thus, our final religiousness variable comprises two response possibilities, either (Christian) religious or not religious.

### Hypotheses
    Hypothesis 1
First of all, we want to know whether there are significant differences in the response to abortion among different age groups. Since the response to abortion is an ordinal variable and age a metric one, we can either use the Pearson Correlation test (parametric) or the Kendall Rank Correlation test (non-parametric). The former should only be applied if we know that the relevant variables follow a normal distribution as this is pre-assumed by the test. We therefore checked the distribution of the age data points using the Shapiro-Wilk test. Although age usually follows a normal distribution, it does not do so in our case, perhaps due to the low amount of participants or other biases influencing which people end up as participants. We therefore choose the Kendall Rank Correlation test.

    Hypothesis 2
Secondly, we want to know whether the responses to abortion vary between the two sexes. Since response to abortion is an ordinal variable and the sex is a binary nominal one, we cannot use the Kendall Rank Correlation test, nor the Pearson Correlation test. In order to account for a binary nominal variable, we make use of the Point Biseral Correlation test.

    Hypothesis 3
Finally, we are interested in the role of religiousness when it comes to stances on abortion, whether (Christian) religious people tend to give different responses to abortion than non religious people. After the changes to the response possibilities which we have made earlier, depending on the participant’s denomination, we are left with a binary nominal variable. Therefore, as in H2, we will use the Point Biseral Correlation test again.


## Section IV: Requirements and table of files

### Requirements
In order to execute our code, there are a few things you need to have installed and prepared. First of all, we have worked with Python 3.10.4 so this version should definitely work. Next, there are a few librarys required. You can install all at once with the use of the provided "requirements.txt" file and a command like #pip install -r requirements.txt#.


### Table of files


    • libraries
    • python version
    • jupyter notebook

## Section V: Instructions for the use of our code 


## Section VI: Interpretation of Outputs / Hypotheses testings
    • since age does not matter, we excluded the alternative explanation of religious people are usually older.
    
    
    
    
    
## Reference
Diekmann, A., Hadjar, A., Kurz, K., Rosar, U., Wagner, U., Westle, B., & Kantar Public, M. (2019). Allgemeine Bevölkerungsumfrage der Sozialwissenschaften ALLBUS 2018. GESIS - Leibniz-Institut für Sozialwissenschaften. Retrieved from https://search.gesis.org/research_data/ZA5270?doi=10.4232/1.13250

