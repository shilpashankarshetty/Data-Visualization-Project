from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from io import BytesIO
import seaborn as sns
import base64


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:Shilpa123@localhost/loan"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="thishello"
db = SQLAlchemy(app)

users = [{'username': 'user1', 'password': 'password1'}, {'username': 'user2', 'password': 'password2'}]



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('bank.html')


@app.route('/apply_loan')
def apply_loan():
    return render_template('apply_loan.html')

@app.route('/bank', methods=['GET','POST'])
def bank():
    if request.method == 'POST':
        return render_template('bank.html')
    
@app.route('/bank_interest1')
def bank_interest1():
    return render_template('bank_interest1.html')

@app.route('/bank_interest2')
def bank_interest2():
    return render_template('bank_interest2.html')

@app.route('/bank_interest3')
def bank_interest3():
    return render_template('bank_interest3.html')

@app.route('/bank_interest4')
def bank_interest4():
    return render_template('bank_interest4.html')

@app.route('/bank_interest5')
def bank_interest5():
    return render_template('bank_interest5.html')


@app.route('/bank_interest6')
def bank_interest6():
    return render_template('bank_interest6.html')

@app.route('/form_fill', methods=['GET', 'POST'])
def form():
    success_message = None
    error_message = None

    if request.method == 'POST':
        gender = request.form.get('gender')
        married = request.form.get('married')
        dependents = request.form.get('dependents')
        education = request.form.get('education')
        self_employed = request.form.get('self_employed')
        applicantincome = int(request.form.get('applicantincome'))
        coapplicantincome = int(request.form.get('coapplicantincome'))
        loanamount = int(request.form.get('loanamount'))
        loanamountterm = request.form.get('loanamountterm')
        credithistory = int(request.form.get('credithistory'))
        date = request.form.get('date')

        # Convert date string to a date object
        dates = datetime.strptime(date, '%Y-%m-%d').date()

        loanStatus = "not approved"  # Default loan status

        # Check conditions for loan eligibility
        if (self_employed == 'No' and applicantincome < 500000 and loanamount > 500000) or \
           (credithistory < 700 or int(dependents) > 3):
            error_message = "Loan not approved. Applicant does not meet eligibility criteria."
        else:
            # If loan is approved, set status to "approved"
            loanStatus = "approved"
            success_message = "Loan approved and uploaded."

            # Insert data into the Loan model
            db.session.execute(text("INSERT INTO loan_status(gender, married, dependents, education, self_employed, applicantincome, coapplicantincome, loanamount, loanamountterm, credithistory) VALUES (:gender, :married, :dependents, :education, :self_employed, :applicantincome, :coapplicantincome, :loanamount, :loanamountterm, :credithistory)"),{"gender":gender,"married" :married, "dependents":dependents,"education" :education,"self_employed" :self_employed,"applicantincome" :applicantincome,"coapplicantincome" :coapplicantincome, "loanamount":loanamount, "loanamountterm":loanamountterm, "credithistory":credithistory})
            db.session.execute(text("INSERT INTO loan_approved (gender, married, dependents, education, self_employed, applicantincome, coapplicantincome, loanamount, loanamountterm, credithistory,loanstatus) VALUES (:gender, :married, :dependents, :education, :self_employed, :applicantincome, :coapplicantincome, :loanamount, :loanamountterm, :credithistory, :loanstatus)"),{"gender":gender,"married" :married, "dependents":dependents,"education" :education,"self_employed" :self_employed,"applicantincome" :applicantincome,"coapplicantincome" :coapplicantincome, "loanamount":loanamount, "loanamountterm":loanamountterm, "credithistory":credithistory, "loanstatus":loanStatus})

            db.session.commit()

    return render_template('form.html', success_message=success_message, error_message=error_message)


@app.route('/submit', methods=['POST'])
def submit():
    return redirect(url_for('form')) 


# ----------------------------------------------------------------VISUALIZATION-----------------------------------------


def fetch_loan_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    df = pd.DataFrame([(loan.gender, float(loan.loanamount), float(loan.credithistory)) for loan in loan_data],
                      columns=['gender', 'loanamount', 'credithistory'])

    return df


# --------------------HEATMAP------------------------
def fetch_heatmap_scatter_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    df = pd.DataFrame([(loan.gender, float(loan.dependents), float(loan.credithistory)) for loan in loan_data],
                      columns=['gender', 'dependents', 'credithistory'])

    return df

# ---------------------SCATTERPLOT-----------------------------
def fetch_scatter_scatter_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    df = pd.DataFrame([(loan.gender, float(loan.applicantincome), float(loan.credithistory)) for loan in loan_data],
                      columns=['gender', 'dependents', 'credithistory'])

    return df

#----------------------Pie chart approved by gender-------

#----------------------Pie chart not approved by gender-------

#----------------------VIOLIN PLOT------------------------

def fetch_violin_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    df = pd.DataFrame([(loan.dependents, float(loan.applicantincome)) for loan in loan_data],
                      columns=['dependents', 'applicantincome'])

    return df


#-------------------DISTRIBUTION PLOT--------------------------

def fetch_distribution_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    applicant_income = []
    coapplicant_income = []

    for loan in loan_data:
        applicant_income.append(float(loan.applicantincome))
        coapplicant_income.append(float(loan.coapplicantincome))

    df = pd.DataFrame({'Applicant Income': applicant_income, 'Coapplicant Income': coapplicant_income})
    return df


#-------------------DENSITY PLOT-------------------

def fetch_density_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    df = pd.DataFrame([(loan.coapplicantincome, float(loan.applicantincome)) for loan in loan_data],
                      columns=['coapplicantincome', 'applicantincome'])

    # Convert 'dependents' to numeric
    df['coapplicantincome'] = pd.to_numeric(df['coapplicantincome'], errors='coerce')

    return df

#---------------------STACKED BAR CHART OF APPLICANTINCOME------------------------

def fetch_stacked_bar_data():
    loan_data = db.session.execute(text("SELECT dependents, applicantincome FROM loan_approved"))
    df = pd.DataFrame([(loan.dependents, float(loan.applicantincome)) for loan in loan_data],
                      columns=['dependents', 'applicantincome'])

    return df

#---------------------STACKED BAR CHART OF COAPPLICANTINCOME------------------------

def fetch_stacked_bar_data_coapplicant():
    loan_data = db.session.execute(text("SELECT dependents, coapplicantincome FROM loan_approved"))
    df = pd.DataFrame([(loan.dependents, float(loan.coapplicantincome)) for loan in loan_data],
                      columns=['dependents', 'coapplicantincome'])

    return df

#-------------------------Bar Chart-----------------------------------------
def fetch_bar_data():
    loan_data = db.session.execute(text("SELECT education, credithistory FROM loan_approved"))
    df = pd.DataFrame([(loan.education, float(loan.credithistory)) for loan in loan_data],
                      columns=['education', 'credithistory'])

    return df

#-----------------------Histogram--------------------------------------------

def fetch_histogram_data():
    loan_data = db.session.execute(text("SELECT gender, loanamount FROM loan_approved"))
    df = pd.DataFrame([(loan.gender, float(loan.loanamount)) for loan in loan_data],
                      columns=['gender', 'loanamount'])

    return df


#--------------------Correlogram-------------------------------------------
def fetch_correlogram_data():
    loan_data = db.session.execute(text("SELECT * FROM loan_approved"))
    df = pd.DataFrame([(float(loan.applicantincome), float(loan.loanamount)) for loan in loan_data],
                      columns=['applicantincome', 'loanamount'])

    return df





@app.route('/dashboard')
def box_plot():

    plt.style.use('dark_background')
    # Fetch and display box plot
    loan_data = fetch_loan_data()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='credithistory', y='loanamount', data=loan_data, ax=ax)
    plt.title('Box Plot of Loan Amount by Credit History')
    plt.xlabel('Credit History')
    plt.ylabel('Loan Amount')
    img_box = BytesIO()
    plt.savefig(img_box, format='png')
    img_box.seek(0)
    plt.close()

    # Fetch and display heatmap
    heatmap_data = fetch_heatmap_scatter_data()
    heatmap_data_pivot = heatmap_data.pivot_table(index='dependents', columns='credithistory', aggfunc=len, fill_value=0)
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data_pivot, annot=True, fmt='g', cmap='Blues', cbar=True, ax=ax_heatmap)
    plt.title('Heatmap of Dependents vs. Credit History')
    plt.xlabel('Credit History')
    plt.ylabel('Dependents')
    img_heatmap = BytesIO()
    plt.savefig(img_heatmap, format='png')
    img_heatmap.seek(0)
    plt.close()

    # Fetch and display scatter plot
    scatter_data = fetch_scatter_scatter_data()
    fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='dependents', y='credithistory', data=scatter_data, ax=ax_scatter)
    plt.title('Scatter Plot of Dependents vs. Credit History')
    plt.xlabel('Dependents')
    plt.ylabel('Credit History')
    img_scatter = BytesIO()
    plt.savefig(img_scatter, format='png')
    img_scatter.seek(0)
    plt.close()

# ----------------PIE CHART FOR APPROVED-----------------------
    
    approved_loan_data = db.session.execute(text("SELECT gender, COUNT(*) as count FROM loan_approved WHERE loanstatus='approved' GROUP BY gender"))
    approved_loan_df = pd.DataFrame([(loan.gender, int(loan.count)) for loan in approved_loan_data], columns=['gender', 'count'] )
    fig_pie, ax_pie = plt.subplots()
    wedges, texts, autotexts = ax_pie.pie(approved_loan_df['count'], labels=approved_loan_df['gender'], autopct='%1.1f%%', startangle=90)
    # plt.setp(autotexts, textprops=dict(color="white"))
    # wedges, texts, autotexts = ax_pie.pie(approved_loan_df['count'], labels=approved_loan_df['gender'], autopct='%1.1f%%', startangle=90)


    ax_pie.pie(approved_loan_df['count'], labels=approved_loan_df['gender'], autopct='%1.1f%%', startangle=90,textprops={'color': 'cyan'})
    ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Approved Loans by Gender')
    img_pie = BytesIO()
    plt.savefig(img_pie, format='png')
    img_pie.seek(0)
    plt.close()

    

#-------------------------PIE CHART FOR NOT APPROVED-----------------------------------------

    not_approved_loan_data = db.session.execute(text("SELECT gender, COUNT(*) as count FROM loan_approved WHERE loanstatus='not approved' GROUP BY gender"))
    not_approved_loan_df = pd.DataFrame([(loan.gender, int(loan.count)) for loan in not_approved_loan_data], columns=['gender', 'count'])
    fig_pie_not_approved, ax_pie_not_approved = plt.subplots()
    ax_pie_not_approved.pie(not_approved_loan_df['count'], labels=not_approved_loan_df['gender'], autopct='%1.1f%%', startangle=90, textprops={'color': 'green'})
    ax_pie_not_approved.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Not Approved Loans by Gender')
    img_pie_not_approved = BytesIO()
    plt.savefig(img_pie_not_approved, format='png')
    img_pie_not_approved.seek(0)
    plt.close()


#---------------------------VIOLON PLOT--------------------------------------------------------
    violin_data = fetch_violin_data()
    fig_violin, ax_violin = plt.subplots(figsize=(10, 6))
    sns.violinplot(x='dependents', y='applicantincome', data=violin_data, ax=ax_violin)
    plt.title('Violin Plot of Applicant Income by Dependents')
    plt.xlabel('Dependents')
    plt.ylabel('Applicant Income')
    img_violin = BytesIO()
    plt.savefig(img_violin, format='png')
    img_violin.seek(0)
    plt.close()

#------------------------DISTRIBUTION PLOT------------------------------------------------------
    distribution_data = fetch_distribution_data()
    fig_dist, ax_dist = plt.subplots(figsize=(10, 6))
    sns.histplot(data=distribution_data, kde=True, bins=30, ax=ax_dist, element='step', stat='density')
    plt.title('Distribution Plot of Applicant and Coapplicant Income')
    plt.xlabel('Income')
    plt.ylabel('Density')
    img_dist = BytesIO()
    plt.savefig(img_dist, format='png')
    img_dist.seek(0)
    plt.close()



#-----------------------DENSITY PLOT---------------------------------------------------------
    
    density_data = fetch_density_data()
    fig_density, ax_density = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data=density_data, x='coapplicantincome', y='applicantincome', fill=True, cmap='Blues', ax=ax_density)
    plt.title('Density Plot of coapplicantincome vs. Applicant Income')
    plt.xlabel('coapplicantincome')
    plt.ylabel('Applicant Income')
    img_density = BytesIO()
    plt.savefig(img_density, format='png')
    img_density.seek(0)
    plt.close()

#---------------------STACKED BAR CHART OF APPLICANTINCOME------------------------
    stacked_bar_data = fetch_stacked_bar_data()
    fig_stacked_bar, ax_stacked_bar = plt.subplots(figsize=(10, 6))
    sns.barplot(x='dependents', y='applicantincome', data=stacked_bar_data, estimator=np.sum, ci=None, ax=ax_stacked_bar)
    plt.title('Stacked Bar Plot of Applicant Income by Dependents')
    plt.xlabel('Dependents')
    plt.ylabel('Total Applicant Income')
    img_stacked_bar = BytesIO()
    plt.savefig(img_stacked_bar, format='png')
    img_stacked_bar.seek(0)
    plt.close()

#---------------------STACKED BAR CHART OF COAPPLICANTINCOME------------------------
    
    stacked_bar_data_coapplicant = fetch_stacked_bar_data_coapplicant()
    fig_stacked_bar_coapplicant, ax_stacked_bar_coapplicant = plt.subplots(figsize=(10, 6))
    sns.barplot(x='dependents', y='coapplicantincome', data=stacked_bar_data_coapplicant, estimator=np.sum, ci=None, ax=ax_stacked_bar_coapplicant)
    plt.title('Stacked Bar Plot of Coapplicant Income by Dependents')
    plt.xlabel('Dependents')
    plt.ylabel('Total Coapplicant Income')
    img_stacked_bar_coapplicant = BytesIO()
    plt.savefig(img_stacked_bar_coapplicant, format='png')
    img_stacked_bar_coapplicant.seek(0)
    plt.close()

#-------------------------Barchart----------------------------------------
    
    bar_data = fetch_bar_data()
    fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
    sns.countplot(x='education', hue='credithistory', data=bar_data, ax=ax_bar)
    plt.title('Bar Chart of Education by Credit History')
    plt.xlabel('Education')
    plt.ylabel('Count')
    plt.legend(title='Credit History')
    img_bar = BytesIO()
    plt.savefig(img_bar, format='png')
    img_bar.seek(0)
    plt.close()

#-----------------Histogram-------------------------------------------
    histogram_data = fetch_histogram_data()
    fig_histogram, ax_histogram = plt.subplots(figsize=(10, 6))
    sns.histplot(data=histogram_data, x='loanamount', hue='gender', bins=30, multiple='stack', ax=ax_histogram, element='step', stat='density')
    plt.title('Histogram of Loan Amount by Gender')
    plt.xlabel('Loan Amount')
    plt.ylabel('Density')
    img_histogram = BytesIO()
    plt.savefig(img_histogram, format='png')
    img_histogram.seek(0)
    plt.close()

#--------------------Correlogram-------------------------------------------
    correlogram_data = fetch_correlogram_data()
    fig_correlogram = sns.pairplot(correlogram_data[['applicantincome', 'loanamount']])
    plt.title(' ')
    img_correlogram = BytesIO()
    plt.savefig(img_correlogram, format='png')
    img_correlogram.seek(0)
    plt.close()









    chart_url_box = base64.b64encode(img_box.getvalue()).decode('utf8')
    chart_url_heatmap = base64.b64encode(img_heatmap.getvalue()).decode('utf8')
    chart_url_scatter = base64.b64encode(img_scatter.getvalue()).decode('utf8')
    chart_url_pie = base64.b64encode(img_pie.getvalue()).decode('utf8')
    chart_url_pie_not_approved = base64.b64encode(img_pie_not_approved.getvalue()).decode('utf8')
    chart_url_violin = base64.b64encode(img_violin.getvalue()).decode('utf8')
    chart_url_dist = base64.b64encode(img_dist.getvalue()).decode('utf8')
    chart_url_density = base64.b64encode(img_density.getvalue()).decode('utf8')
    chart_url_stacked_bar = base64.b64encode(img_stacked_bar.getvalue()).decode('utf8')
    chart_url_stacked_bar_coapplicant = base64.b64encode(img_stacked_bar_coapplicant.getvalue()).decode('utf8')
    chart_url_bar = base64.b64encode(img_bar.getvalue()).decode('utf8')
    chart_url_histogram = base64.b64encode(img_histogram.getvalue()).decode('utf8')
    chart_url_correlogram = base64.b64encode(img_correlogram.getvalue()).decode('utf8')


    return render_template('dashboard.html', chart_url_box=chart_url_box, chart_url_heatmap=chart_url_heatmap, chart_url_scatter=chart_url_scatter,chart_url_pie=chart_url_pie,chart_url_pie_not_approved=chart_url_pie_not_approved,chart_url_violin=chart_url_violin,chart_url_dist=chart_url_dist,chart_url_density=chart_url_density,chart_url_stacked_bar=chart_url_stacked_bar,chart_url_stacked_bar_coapplicant=chart_url_stacked_bar_coapplicant,chart_url_bar=chart_url_bar,chart_url_histogram=chart_url_histogram,chart_url_correlogram=chart_url_correlogram)



if __name__ == '__main__':
    app.run(debug=True)

