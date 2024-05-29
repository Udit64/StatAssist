from scipy.stats import shapiro
import pandas as pd
from flask import session
import io
from flask import Response


questions_options = {
    
    "q1": {"question": "Is this a one sample problem?", "options": ["yes","no"]},
    "q2": {"question": "Is there only one variable of interest?", "options" : ["yes","no"]},
    "q3": {"question": "Is this a two sample problem?", "options": ["yes","no"]},
    "q5": {"question": "Inference concerning mean or variance?", "options": ["mean", "variance"]},
    "q11": {"question": "Are you assuming curve comes from a Weibull distribution:", "options": ["yes","no"]},
    "q12": {"question": "Are you interested in comparison of survival curves of two groups with limited control of covariates:", "options": ["yes", "no"]},
    "q14": {"question": "Do incidence rates remain constant over time:", "options": ["yes", "no"]},
    "q15": {"question": "How many number of ways can the categorical variable be classified into?", "options": ["1", "2", ">2"]},
    "q21": {"question": "Is this a one-sample problem -", "options": ["yes", "no"]},
    "q22": {"question": "RxC Contingency table, R>2 and C>2?", "options": ["yes", "no"]},
    "q23": {"question": "Samples are independent or not:", "options": ["Independent", "not Independent"]},
    "q25": {"question": "Is the underlying distribution binomial?", "options": ["yes", "no"]},
    "q26": {"question": "Is the data person-time type?", "options": ["yes", "no"]},
    "q27": {"question": "Samples are independent or not:", "options": ["yes","no"]},
    "q28": {"question": "Are variances of the two samples significantly different?", "options": ["yes","no"]},
    "q29": {"question": "Is the data Categorical? ", "options": ["yes","no"]},
    "q30": {"question": "Is one variable Continuous and the other one Categorical? ", "options": ["yes","no"]},
    "q31": {"question": "Interested in predicting one variable from the other? ", "options": ["yes","no"]},
    "q32": {"question": "Are both Variables normal? ", "options": ["yes","no"]},
    "q34": {"question": "Are you interested in comparison of survival curves of two groups with limited control of covariates:", "options": ["yes", "no"]},
    "q35": {"question": "Both Variables Continuous? ", "options": ["yes","no"]},
    "q37": {"question": "Interested in relationship between 2 Variables? ", "options": ["yes","no"]},
    "q38": {"question": "Interested in trends over k binomial proportions? ", "options": ["yes","no"]},
    "q39": {"question": "2 x 2 Contingency Table? ", "options": ["yes","no"]},
    "q40": {"question": "2 x k Contingency Table? ", "options": ["yes","no"]},
    "q42": {"question": "Are the expected values >=5? ","options":["yes","no"]},
    "q43": {"question": "Confounding is present?", "options": ["yes","no"]},
    "q44": {"question": "Inference concerning mean or variance?", "options": ["mean", "variance"]},
    "q45": {"question": "Underlying distribution is Binomial?", "options": ["yes", "no"]},
    "q46": {"question": "Underlying distribution is Poisson?", "options": ["yes", "no"]},
    "q47": {"question": "Inference concerning mean or variance?", "options": ["mean", "variance"]},
}


def clt(df):
    sample_size = df.size[0]
    stat, shapiro_p_value = shapiro(df)
    if shapiro_p_value > 0.05:
        return True
    else:
        return False
    


# def determine_next_question(question_id):
#     print("Question ID: ", question_id)
#     csv = session['csv_data']
#     df = pd.read_csv(io.StringIO(csv.decode('utf-8')))
#     #print(df)
    
#     if question_id == "q1":
#         if response == "yes":
#             if clt(df):
#                 return 'q44'
#             else:
#                 return "q45"
#         elif response == "no":
#             return "q3"         
#     elif question_id == 'q44':
#         if response == 'mean':
#             if df.size[0] > 30:
#                 return "Can perform z-test due to large sample size"
#             else:
#                 return "Use t-test due to small data size"    
#         elif response == 'variance':
#             return 'Statistical Test Decided: Chi Square test for variances'  
    
#     elif question_id == "q45":
#         if response == "yes":
#             return "Statistical Test Decided: One sample binomial test"
#         elif response == "no":
#             return "q46"
        
#     elif question_id == "q46":
#         if response == "yes":
#             return "Statistical Test Decided: One sample poisson test"
#         elif response == "no":
#             return "Use another underlying distribution of use nonparametric methods"
        
#     elif question_id == 'q47':
#         if response == 'mean':
#             return "q23"    
#         elif response == 'variance':
#             return 'Statistical Test Decided: Two-Sample F-test to compare variances' 
    
#     elif question_id == "q2":
#         if response == "yes":
#             return "q1"
#         elif response == "no":
#             return "q37"

#     elif question_id == "q3":
#         if response == "yes":
#             if clt(df):
#                 return "q47"
#             else:
#                 return "q25"
#         elif response == "no":
#             return "q23"            

#     elif question_id == 'q5':
#         if response == 'mean':
#             return 'q23'
#         elif response == 'variance':
#             return 'q25'


#     elif question_id == 'q11':
#         if response == 'yes':
#             return 'Statistical Test Decided: Use parameter survival methods based on Weibull distribution.'
#         elif response == 'no':
#             return 'Statistical Test Decided: Use Cox proportional hazards mode.'

#     elif question_id == 'q12':
#         if response == 'yes':
#             return 'Statistical Test Decided: Log rank test'
#         elif response == 'no':
#             return 'q11'


#     elif question_id == 'q14':
#         if response == 'yes':
#             return 'Statistical Test Decided: Two sample test for incidence rates/trend test.'
#         elif response == 'no':
#             return 'q12'

    
#     elif question_id == 'q15':
#         if response == '1':
#             return 'Statistical Test Decided: One-way ANOVA.'
#         elif response == '2':
#             return 'Statistical Test Decided: Two-way ANOVA.'
#         elif response == '>2':
#             return 'Statistical Test Decided: Higher-Way ANOVA.'
            
    
    
#     elif question_id == 'q21':
#         if response == 'yes':
#             return 'Statistical Test Decided: One sample test for incidence rates.'
#         elif response == 'no':
#             return 'q14'

#     elif question_id == 'q22':
#         if response == 'yes':
#             return 'Statistical Test Decided: Use Chi-Squared Test for RxC Table.'
#         elif response == 'no':
#             return "The data may not fit well with any of the contingency table methods provided."

#     elif question_id == 'q23':
#         if response == 'Independent':
#             return 'q28'
#         elif response == 'not Independent':
#             return 'Statistical Test Decided: Paired t-test to perform mean.'


#     elif question_id == 'q25':
#         if response == 'yes':
#             return 'q27'
#         elif response == 'no':
#             return 'q26'


#     elif question_id == 'q26':
#         if response == 'yes':
#             return 'q21'
#         elif response == 'no':
#             return "Use another underlying distribution or nonparametric methods"

#     elif question_id == 'q27':
#         if response == 'yes':
#             return 'q42'
#         elif response == 'no':
#             return  "Statistical Test Decided: McNemar's test"

#     elif question_id == 'q28':
#         if response == 'yes':
#             return "Statistical Test Decided: Two sample t-test with equal variances if variance is equal, otherwise use unequal variances version"
#         elif response == 'no':
#             return  "Ensure data is split into 2 classes"
            
#     elif question_id == 'q29':
#         if response == 'yes':
#             return "Statistical Test Decided: Use RXC Contigency table methods."
#         elif response == 'no':
#             return "Statistical Test Decided: Kruskall-Wallis Test"

#     elif question_id == 'q30':
#         if response == 'yes':
#             return  'q15'
#         elif response == 'no':
#             return 'Statistical Test Decided: Use Contigency table methods.'

#     elif question_id == 'q31':
#         if response == 'yes':
#             return  "Statistical Test Decided: Consider Simple Linear Regression for prediction."
#         elif response == 'no':
#             return 'q32'
            
            
#     elif question_id == 'q32':
#         if response == 'yes':
#             return  "Statistical Test Decided: Pearson Correlation."
#         elif response == 'no':
#             return "Statistical Test Decided: Spearman Rank Correlation."
            
            
            
#     elif question_id == 'q34':
#         if response == 'yes':
#             return "Statistical Test Decided: Perform log-rank test for comparison of survival curves."
#         elif response == 'no':
#             return 'q11'

#     elif question_id == 'q35':
#         if response == 'yes':
#             return 'q31'
#         elif response == 'no':
#             return 'q30'

            
#     elif question_id == 'q37':
#         if response == 'yes':
#             return 'q35'
#         elif response == 'no':
#             return 'For multiple variables or outcomes, consider regression models or multivariate analysis.'
            
            
#     elif question_id == 'q38':
#         if response == 'yes':
#             return 'q43'
#         elif response == 'no':
#             return 'Statistical Test Decided: Chi-Squared Test for homogenity.'
            
#     elif question_id == 'q39':
#         if response == 'yes':
#             return 'q43'
#         elif response == 'no':
#             return 'q40'
            
#     elif question_id == 'q40':
#         if response == 'yes':
#             return 'q9'
#         elif response == 'no':
#             return 'q22'

    
#     elif question_id == 'q42':
#         if response == 'yes':
#             return 'q39'
#         elif response == 'no':
#             return "Statistical Test Decided: Fisher's exact test"
            
#     elif question_id == 'q43':
#         if response == 'yes':
#             return "Statistical Test Decided: Mantel-Haenszel test."
#         elif response == 'no':
#             return "Statistical Test Decided: Chi-Squared Test."


#     return