from flask import Flask, flash, request, jsonify, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohsosecret'
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False


# ['Yes', 'No', 'Less than $10,000', 'Yes']
responses=[]

@app.route('/')
def home_page():
    return render_template('home.html', t=satisfaction_survey.title,i=satisfaction_survey.instructions)

@app.route('/questions/<int:page>')
def question(page):
        q=satisfaction_survey.questions[page].question
        choices = satisfaction_survey.questions[page].choices
        return render_template('questions.html', q=q, choicesList=choices, page_num=page)
       

@app.route('/answer', methods=["POST"])
def answer():
    # this is a post so we store the data in the responses
    page_num = request.form["page_num"]
    responses.append(request.form[page_num])
    next_page = int(page_num)+1
    flash(f'Thanks! This is your answer {request.form[page_num]}!')
    
    
    # get next question
    # q=satisfaction_survey.questions[next_page].question
    # choices = satisfaction_survey.questions[next_page].choices
    # get the next page
    print(next_page)
    if next_page == 4:
        
        return redirect('/thank-you')
    elif next_page < 4:
        return redirect(url_for('question',page=str(next_page)))
@app.route('/thank-you')
def thank():
    return render_template('thank-you.html', responses=responses)