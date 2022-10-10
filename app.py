from flask import Flask, flash, request, jsonify, redirect, render_template, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ohsosecret'
debug=DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False


# ['Yes', 'No', 'Less than $10,000', 'Yes']
# responses=[]
# should_be_on_page=0

@app.route('/')
def home_page():
    return render_template('home.html', t=satisfaction_survey.title,i=satisfaction_survey.instructions)

@app.route('/setSession', methods=["POST"])
def set_session():
    session["responses"]=[]
    return redirect('/questions/0')

@app.route('/questions/<int:page>')
def question(page):
    # finished survey?
    # print(should_be_on_page)
    if len(session['responses']) >= len(satisfaction_survey.questions):
        flash("You're done already!")
        return redirect('/thank-you')
    # if page number is wrong, redirect to correct page
    elif page !=len(session['responses']):
    # go to correct page regardless of what they put in the url
        flash("You're trying to access an invalid question!")
        return redirect(url_for('question',page=str(len(session['responses']))))
    else:
        real_page = len(session['responses'])
        q=satisfaction_survey.questions[real_page].question
        choices = satisfaction_survey.questions[real_page].choices
        allow_text = satisfaction_survey.questions[real_page].allow_text
        return render_template('questions.html', q=q, choicesList=choices, page_num=real_page, allow_text=allow_text)
        # return redirect(url_for('question',page=str(should_be_on_page)))

    # elif len(responses) == len(satisfaction_survey.questions):
    #     return redirect('/thank-you')
        
    # q=satisfaction_survey.questions[page].question
    # choices = satisfaction_survey.questions[page].choices
    # return render_template('questions.html', q=q, choicesList=choices, page_num=page)
       

@app.route('/answer', methods=["POST"])
def answer():
    # need to save comments too using tuples [('answer',comment),answer]
    
    # this is a post so we store the data in the responses
    page_num = request.form["page_num"]
    if 'responses' in session:
        res = session['responses']
        if request.form.get('comments'):
            ans=(request.form[page_num],request.form['comments'])
        else:
            ans=request.form[page_num]
        print('********')
        print(ans)
        res.append(ans)
        session['responses'] = res
        print('**********')
        print(res)
        next_page = int(page_num)+1
        flash(f'Thanks! This is your answer {request.form[page_num]}!')
    
        # get the next page
        if next_page > len(satisfaction_survey.questions)-1:
            return redirect('/thank-you')
        else:
            return redirect(url_for('question',page=str(next_page)))
    else:
        return redirect('/')
        

@app.route('/thank-you')
def thank():
    # set cookie to let them know they filled it out already
    a = make_response(render_template('thank-you.html', ans=res))
    a.set_cookie('filled-out',True)
    res = {}
    response = session['responses']
    allQ = []
    for q in satisfaction_survey.questions:
        allQ.append(q.question)
    for key in allQ:
        for value in response:
            res[key] = value
            response.remove(value)
            break
    return a