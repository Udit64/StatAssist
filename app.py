from flask import Flask, render_template, request,redirect, url_for, session,jsonify

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from dictwnextq import *
app = Flask(__name__)
app.secret_key = 'your_secret_key'

import pandas as pd
import numpy as np
from scipy.stats import shapiro
import scipy.stats as stats


stat_test=None
@app.route('/')
def index():
    # Display the first question
    return render_template('index.html', question_id='q1', questions_options=questions_options)

@app.route('/result')
def result():
    global stat_test
    stats_info = session.get('stats_info')
    # stat_test = session.get('stat_test')
    # if stats_info is None:
    #     return "Error: No data to display"
    return render_template('result.html', stats_info=stats_info,stat_test=stat_test)

@app.route('/update_response', methods=['GET'])
def update_response():
    print(request.form)
    question_id = request.args.get('question_id')
    response = request.args.get('response')

    # Retrieve or initialize the session's responses.
    responses = session.get('responses', {})

    # Update the responses dictionary.
    responses[question_id] = response

    # Persist the updated responses in the session.
    session['responses'] = responses

    # Determine the next question based on the current response.
    print("udi2",question_id)

    next_question_id = determine_next_question(question_id, response)


    print("check",next_question_id)

    # if next_question_id is None:

    #         # If there are no more questions, redirect to the results page.
    #         return redirect(url_for('result'))
    # Print the selected option for debugging.
    print(f"Selected option for {question_id}: {response}")
    print(f"Next question ID: {next_question_id}")

    # Return the ID of the next question along with the success status.
    return jsonify(success=True, next_question_id=next_question_id)

@app.route('/process', methods=['POST'])
def process():
    # Check if the 'response' key is in the submitted form data
    if 'response' in request.form:
        # Retrieve or initialize the session's responses.
        responses = session.get('responses', {})

        # Get the current question ID and response from the form.
        question_id = request.form['question_id']
        response = request.form['response']

        # Update the responses dictionary with the current response.
        responses[question_id] = response
        session['responses'] = responses

        # Determine the next question based on the current response.

        next_question_id = determine_next_question(question_id, response)


        # Check if there are no more questions to determine.
        if next_question_id is None:
            # All questions have been answered, now check if CSV data is present.
            # if 'csv_data' in session:
                # Analyze the CSV data since it's available.
                csv_file = session.get('csv_data')
                # analyze_data(csv_file)  # Ensure 'stats_info' is set in the session within this function.

                # Redirect to the results page.
                return redirect(url_for('result'))
            # else:
            #     # The CSV data is missing, return an error message.
            #     return render_template('index.html', error="CSV file is required.",
            #                            questions_options=questions_options)
        else:
            # There are still more questions to answer, render the next question.
            return render_template('index.html', question_id=next_question_id,
                                   questions_options=questions_options)
    else:
        # The form was submitted without a valid 'response' key, this is unexpected.
        # Handle the error or redirect as appropriate.
        return render_template('index.html', error="An unexpected error occurred.",
                               questions_options=questions_options)

# print(questions_options)
def determine_next_question(question_id, response):
    global stat_test
    print("Udit: ",question_id)
    csv=session.get('csv_data')
    df = pd.read_csv(io.StringIO(csv.decode('utf-8')))
    stats_info = df.describe()
    session['stats_info'] = stats_info.to_json()
    print(df)
    if question_id == 'q1':

        if response == 'One':
            return 'q2'
        elif response == 'Two':
            return 'q37'
        else:
            return 'q100'

    elif question_id == 'q100':
        if response == "continous":
            stat_test = "Multiple Regression"
            session['stat_test'] = stat_test
            return None
        else:
            return 'q101'

    elif question_id == 'q101':
        if response == "yes":
            return 'q3'

        else:
            stat_test = "Perform Multiple Logistic Regression Methods"
            session['stat_test'] = stat_test
            return None

    elif question_id == 'q2':
        if response == 'One Sample Problem':
            # print(df.iloc[:,0])
            shapiro=stats.shapiro(df.iloc[:,0])
            if shapiro[1]>0.05:
                if len(list(df.iloc[:,0])) < 30:
                    stat_test=  "Perform independent t test "

                    return None
                else:
                    stat_test=  "Perform independent z test "

                    return None
            else:
                data=df.iloc[:,0]
                num_unique=np.unique(data)
                if len(num_unique)>2:
                    sample_mean = np.mean(data)

                    if isinstance(data[0], np.float64) == False:
                        expected_counts = stats.poisson.pmf(range(max(data)+1), sample_mean) * len(data)
                        observed_counts, _ = np.histogram(data, bins=range(max(data)+2))
                    else:
                        expected_counts = stats.poisson.pmf(np.arange(int(max(data))+1), int(round(sample_mean))) * len(data)
                        observed_counts, _ = np.histogram(data, bins=np.arange(int(max(data))+2))

                    chi2_stat, p_value = stats.chisquare(observed_counts, f_exp=expected_counts)
                    if p_value>0.05:
                        stat_test="Perform one sample Poisson test"
                    else:
                        stat_test="Use another underlying distribution or use non parametric method"

                    return None
                else:
                    p=np.mean(data)
                    n=len(data)
                    if n*p>=5 and n*(1-p)>=5:
                        stat_test="Follows binomial distribution, Perform normal theory methods"
                    else:
                        stat_test="Follows binomial distribution, Perform exact methods"

                    return None
        elif response == 'Two Sample Problem':
            shapiro_test_A = stats.shapiro(df.iloc[:,0])
            shapiro_test_B = stats.shapiro(df.iloc[:,1])
            p1=shapiro_test_A[1]
            p2=shapiro_test_B[1]
            print(p1)
            print(p2)
            if p1>0.05 and p2>0.05:
                return 'q24'
            else:
                data=df.iloc[:,0]
                if len(np.unique(data))>2:
                    return 'q26'
                else:
                    return 'q27'

        else:
            pcheck=0
            for i in range(df.shape[1]):
                p=stats.shapiro(df.iloc[:,0])
                if p[1]<0.05:
                    pcheck=1
                    break
            if pcheck==1:
                return 'q29'
            else:
                stat_test="Perform One way Anova test"
                return None




    elif question_id == 'q3':
        if response == 'One Sample Problem':
            stat_test="Use one sample tests for incidence rates"
            return None
        elif response == 'Two Sample Problem':
            return 'q14'
        else:
            return 'q36'
    elif question_id == 'q4':
        if response == 'Yes':
            return 'q5'
        elif response == 'No':
            return 'q14'

    if question_id == 'q24':
        if response == 'mean':
            return 'q23'
        elif response == 'variance':
            stat_test="Perform Two sample F test to compare variances"
            return None


    elif question_id == 'q11':
        if response == 'Yes':
            stat_test=  'Statistical Test Decided: Use parameter survival methods based on Weibull distribution.'

            return None
        elif response == 'No':
            stat_test=  'Statistical Test Decided: Use Cox proportional hazards mode.'

            return None

    elif question_id == 'q12':
        if response == 'yes':
            stat_test=  'Statistical Test Decided: Log rank test'

            return None
        elif response == 'no':
            return 'q11'


    elif question_id == 'q14':
        if response == 'yes':
            stat_test='Use two sample test for comparison of incidence rates, if no confounding is present; or methods for stratified person time data, if confounding is present.'
            return None
        else:
            return 'q12'


    elif question_id == 'q15':
        if response == '1':
            outcome=df.iloc[:,-1]
            pval=stats.shapiro(outcome)
            if pval[1]>0.05:
                stat_test="Perform One way anova (Check whether you want to control the confounding variables or not)"
            else:
                stat_test="Perform Kruskal Wallis Test"

            return None

        elif response == '2':
            stat_test="Perform Two way anova (Check whether you want to control the confounding variables or not)"

        elif response == '>2':
            stat_test="Perform One way anova (Check whether you want to control the confounding variables or not)"

        return None


    elif question_id == 'q21':
        if response == 'yes':
            return 'Statistical Test Decided: One sample test for incidence rates.'
        elif response == 'no':
            return 'q36'

    elif question_id == 'q22':
        if response == 'yes':
            return 'Statistical Test Decided: Use Chi-Squared Test for RxC Table.'
        elif response == 'no':
            return "The data may not fit well with any of the contingency table methods provided."

    elif question_id == 'q23':
        if response == 'Independent':
            variance_A = df.iloc[:,0].var(ddof=1)  # ddof=1 for sample variance
            variance_B = df.iloc[:,1].var(ddof=1)
            F = variance_A / variance_B

            # Degrees of freedom
            df_A = len(df.iloc[:,0]) - 1
            df_B = len(df.iloc[:,1]) - 1

            # P-value from the F-distribution
            p_value = stats.f.cdf(F, df_A, df_B)
            print("abhinav",p_value)
            if p_value<0.05:
                stat_test=  "Normality holds for both samples, samples have statistically different variance checked using F test so we can do t test with unequal variance"

                return None
            else:

                stat_test = "Normality holds for both samples, samples have statistically similar variance checked using F test so we can t test with equal variance"

                return None

        elif response == 'Not Independent':
            stat_test= 'Statistical Test Decided: Paired t-test to perform mean.'
            return None

    elif question_id == 'q25':
        if response == 'yes':
            return 'q27'
        elif response == 'no':
            return 'q26'


    elif question_id == 'q26':
        if response == 'Yes':
            return 'q3'
        elif response == 'No':
            stat_test= "Use another underlying distribution or nonparametric methods"
            return None

    elif question_id == 'q27':
        if response == 'yes':
            return 'q105'
        elif response == 'no':
            stat_test=  "Statistical Test Decided: McNemar's test"
            return None

    elif question_id == 'q105':
        if response == 'yes':
            return 'q39'
        elif response == 'no':
            stat_test= "Statistical Test Decided: Fisher's exact test"
            return None


    elif question_id == 'q29':
        if response == 'Yes':
            stat_test= "Statistical Test Decided: Use RXC Contigency table methods."
            return None
        elif response == 'No':
            stat_test= "Statistical Test Decided: Kruskall-Wallis Test"
            return None

    elif question_id == 'q30':
        if response == 'yes':
            return  'q15'
        elif response == 'no':
            return 'q102'

    elif question_id == "q102":
        if response == "yes":
            stat_test="Perform Rank Correlation Method"
            return None
        else:
            return 'q104'

    elif question_id=="q104":
        if response == "association":
            stat_test="Use contingency Table methods"
        else:
            stat_test="Use Kappa Statistics"

        return None

    elif question_id == 'q31':

        if response == 'yes':

            stat_test="Simple Linear Regression for prediction"
            return  None
        elif response == 'no':

            var1=stats.shapiro(df.iloc[:,0])
            var2=stats.shapiro(df.iloc[:,1])
            if var1[1]>0.05 and var2[1]>0.05:
                stat_test="Perform pearson correlation methods"
            else:
                stat_test="Perform Rank correlation methods"

            return None


    elif question_id == 'q34':
        print("abhinav")
        if response == 'yes':
            # print("samanyu")
            stat_test="Perform log rank test"
            # session['stat_test']=stat_test
            return None
        elif response == 'no':
            return 'q11'

    elif question_id == 'q35':
        if response == 'yes':
            return 'q31'
        elif response == 'no':
            return 'q30'


    elif question_id == 'q37':
        if response == 'yes':
            return 'q35'
        elif response == 'no':

            outcome=df.iloc[:,-1]

            if len(np.unique(outcome))>2:
                stat_test="Outcome variable is continous. So, perform Multiple Regression Methods"
                return None
            else:
                return 'q101'


    elif question_id == 'q38':
        if response == 'yes':
            stat_test="Use chi square test for trend, if no confounding is present, or Mantel Extension test if confounding is present"
            return None
        elif response == 'no':
            return 'Use Chi-Squared Test for heterogenity for 2xk tables.'

    elif question_id == 'q39':
        if response == 'yes':
            stat_test="Use two sample test for binomial proportions or 2x2 contingency table methods if no confounding is present, or the Mentel Haenszel Test if confounding is present."
            return None
        elif response == 'no':
            return 'q40'

    elif question_id == 'q40':
        if response == 'yes':
            return 'q38'
        elif response == 'no':
            stat_test="Use chi square test for RxC tables."



    elif question_id == 'q36':
        if response == 'yes':
            stat_test="Use test of trend for incidence rates"
            return None
        elif response == 'no':
            return 'q34'



    # Add more conditions based on your questionnaire logic
    return None

def analyze_data(csv_file):
    global stat_test
    df = pd.read_csv(io.StringIO(csv_file.decode('utf-8')))
    # print(df)
    stats_info = df.describe()

    numcol = df.shape[1]
    session['stats_info'] = stats_info.to_json()
    session['stat_test'] = stat_test
  # Store stats info in session
    return stats_info, stat_test

@app.route('/analyze', methods=['POST'])
def analyze():
    # print("udit1")
    if 'csv_file' not in request.files:
        return render_template('index.html', error="No file part",
                               questions_options=questions_options)
    # print("udit2")

    file = request.files['csv_file']
    if file.filename == '':
        return render_template('index.html', error="No selected file",
                               questions_options=questions_options)
    if file:
        # print("udi/t3")

        csv_file = file.read()
        session['csv_data'] = csv_file  # Store CSV data in session
        analyze_data(csv_file)
        return redirect(url_for('process'))

if __name__ == '__main__':
    app.run(debug=True)
