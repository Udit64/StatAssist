import pandas as pd
import numpy as np
from scipy.stats import shapiro
import scipy.stats as stats


import pandas as pd
from scipy.stats import shapiro, binom_test

def method0(data):
    # Ensure 'data' is a pandas Series or a single column DataFrame
    if isinstance(data, pd.DataFrame) and data.shape[1] == 1:
        data = data.iloc[:, 0]

    stat, shapiro_p_value = shapiro(data)
    sample_size = len(data)

    results = []
    
    if shapiro_p_value > 0.05:
        results.append("Data is approximately normally distributed.")
        if sample_size >= 30:
            results.append("Central Limit Theorem (CLT) likely holds true.")
            results.append("Performing z-test due to large sample size.")
        else:
            results.append("Sample size is small; use t-test.")
    else:
        test_result = binom_test(x=sum(data), n=sample_size, p=0.5)  # Assuming p=0.5 for simplicity
        if test_result < 0.05:
            results.append("Data does not follow a binomial distribution. Check any other distribution.")
        else:
            results.append("Data follows a binomial distribution.")
            results.append(f"One-sample binomial test p-value: {test_result}")

    return " ".join(results)

def method1(data):
    results = []
    sample_size = data.size[0]
    if sample_size ==2:
        stat, shapiro_p_value = shapiro(data)
        test_type=input("Inference concerning mean or variance")
        if shapiro_p_value > 0.05 and test_type == "mean":
            results.append("Data is approximately normally distributed, proceeding with mean comparison.")
            results.extend(method3(data))  # Assuming method3 is adapted to return a list of results
        else:
            results.append("For variance comparison, consider using the two-sample F test.")
        return results
    else:
        return(method2(data))

def method2(data):
    results = []
    stat, shapiro_p_value = shapiro(data)
    if shapiro_p_value > 0.05:
        results.append("Data is approximately normally distributed; ANOVA can be used.")
    else:
        iscategorical=int(input("Is the data Categorical?"))
        if iscategorical:
            results.append("For categorical data, consider using R x C Contingency Table Methods.")
        else:
            results.append("Non-parametric methods like Kruskal-Wallis Test may be more appropriate.")
    return results

def method3(data):
    results = []
    independence = input("Samples are independent or not: Type 1 for independent and 0 for not independent")
    segregator = input("Which Column segregates between the two samples (type exactly as in csv):")
    if independence == "0":
        results.append("Perform paired t test to compare means")
    elif independence == "1":
        unique_values = data[segregator].unique()
        if len(unique_values) == 2:  # Ensure there are exactly two unique values to segregate the samples
            results.append("Perform two-sample t test with equal variances to compare means if variances are equal, otherwise use unequal variances version.")
    return results
    
def method4(data):
    results = []
    is_interest_in_var = input("Interested in relationship between 2 Variables? Type 1 for yes and 0 for no:")
    if is_interest_in_var == "1":
        are_var_cont = input("Both Variables Continuous? Type 1 for yes and 0 for no:")
        if are_var_cont == "1":
            is_var_on_other = input("Interested in predicting one variable from the other? Type 1 for yes and 0 for no:")
            if is_var_on_other == "1":
                results.append("Consider Simple Linear Regression for prediction.")
            else:
                is_normal = input("Are both Variables normal? Type 1 for yes and 0 for no:")
                if is_normal == "1":
                    results.append("Consider Pearson Correlation for normally distributed data.")
                else:
                    results.append("Consider Spearman Rank Correlation for non-normally distributed data.")
        else:
            is_one_cont = input("Is one variable Continuous and the other one Categorical? Type 1 for yes and 0 for no:")
            if is_one_cont == "1":
                num_ways = input("How many number of ways can the categorical variable be classified into? Type the number:")
                if num_ways == "1":
                    results.append("Consider One-Way ANOVA for analysis.")
                elif num_ways == "2":
                    results.append("Consider Two-Way ANOVA for analysis.")
                else:
                    results.append("Consider Higher-Way ANOVA for complex classifications.")
            else:
                results.append("For two categorical variables, consider Contingency Table methods.")
    else:
        results.append("For multiple variables or outcomes, consider regression models or multivariate analysis.")
    return results



def method5():
    results = []
    samplesno = input("Is this a one-sample problem - type 1 for yes and 0 for no:")
    if samplesno == "1":
        results.append("Perform one-sample test for incidence rates")
    else:
        irc = input("Do incidence rates remain constant over time: type 1 for yes and 0 for no:")
        if irc == "1":
            results.append("Consider two-sample tests for incidence rates or trend tests")
        else:
            survival = input("Are you interested in comparison of survival curves of two groups with limited control of covariates: type 1 for yes and 0 for no:")
            if survival == "1":
                results.append("Perform log-rank test")
            else:
                assumption = input("Are you assuming curve comes from a Weibull distribution: type 1 for yes and 0 for no:")
                if assumption == "1":
                    results.append("Use parameter survival methods based on Weibull distribution")
                else:
                    results.append("Use Cox proportional hazards model")
    return results

def method6(data):
    results = []
    is_2_cross_2 = input("2 x 2 Contingency Table? Type 1 for yes and 0 for no:")
    if is_2_cross_2 == "1":
        results.extend(methodA())
    else:
        is_2_cross_k = input("2 x k Contingency Table? Type 1 for yes and 0 for no:")
        if is_2_cross_k == "1":
            results.extend(methodB())
        else:
            is_rc = input("RxC Contingency table, R>2 and C>2? Type 1 for yes and 0 for no:")
            if is_rc == "1":
                results.append("Use Chi-Squared Test for RxC Table.")
            else:
                results.append("The data may not fit well with any of the contingency table methods provided.")
    return results


def methodA():
    return ["For 2 x 2 tables without confounding, consider the Chi-Squared test. If confounding is present, the Mantel-Haenszel test might be more appropriate."]

def methodB():
    is_inter_in_k = input("Interested in trends over k binomial proportions? Type 1 for yes and 0 for no:")
    if is_inter_in_k == "1":
        return ["For trends in k binomial proportions, consider using the Chi-Squared test for trend, especially if no confounding is present. If confounding is present, the Mantel Extension might be more appropriate."]
    else:
        return ["For 2 x k tables without an interest in trends, consider the Chi-Squared test for homogeneity."]

