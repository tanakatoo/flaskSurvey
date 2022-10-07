from flask import Flask, flash, request, jsonify, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohsosecret'
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False


# ['Yes', 'No', 'Less than $10,000', 'Yes']
responses=[]
# should_be_on_page=0

@app.route('/')
def home_page():
    return render_template('home.html', t=satisfaction_survey.title,i=satisfaction_survey.instructions)

@app.route('/questions/<int:page>')
def question(page):
    # finished survey?
    # print(should_be_on_page)
    if len(responses) >= len(satisfaction_survey.questions):
        return redirect('/thank-you')
    # if page number is wrong, redirect to correct page
    elif page !=len(responses):
    # go to correct page regardless of what they put in the url
        return redirect(url_for('question',page=str(len(responses))))
    else:
        real_page = len(responses)
        q=satisfaction_survey.questions[real_page].question
        choices = satisfaction_survey.questions[real_page].choices
        return render_template('questions.html', q=q, choicesList=choices, page_num=real_page)
        # return redirect(url_for('question',page=str(should_be_on_page)))

    # elif len(responses) == len(satisfaction_survey.questions):
    #     return redirect('/thank-you')
        
    # q=satisfaction_survey.questions[page].question
    # choices = satisfaction_survey.questions[page].choices
    # return render_template('questions.html', q=q, choicesList=choices, page_num=page)
       

@app.route('/answer', methods=["POST"])
def answer():
    
    # this is a post so we store the data in the responses
    page_num = request.form["page_num"]
    print(page_num)
    responses.append(request.form[page_num])
    next_page = int(page_num)+1
    # should_be_on_page=next_page
    print(next_page)
    
    flash(f'Thanks! This is your answer {request.form[page_num]}!')
    
    # get the next page
    if next_page > len(satisfaction_survey.questions)-1:
        
        return redirect('/thank-you')
    else:
        return redirect(url_for('question',page=str(next_page)))

@app.route('/thank-you')
def thank():
    return render_template('thank-you.html', responses=responses)