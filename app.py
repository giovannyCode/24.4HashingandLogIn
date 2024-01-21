from flask import Flask, request, render_template, redirect,flash, session ,json,jsonify

from models import db, connect_db, User,FeedBack
from forms import UserForm, LoginForm,FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] ="oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashingandlogin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
"""db.drop_all()
db.create_all()"""

@app.route("/")
def index_page():
    form = UserForm()
    return render_template ('register.html' ,form = form)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name =form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        new_user = User.register(username, password,email,first_name, last_name)
        db.session.add(new_user)
        try:
         db.session.commit()
        except IntegrityError as e:
           error_text = str(e)
           form.username.errors.append(f"IntegrityError: {error_text}")
           return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f'/users/{new_user.username}')
          
    return render_template('register.html', form=form)

@app.route('/users/<string:username>', methods=['GET'])
def users(username):
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    user = User.query.get_or_404(username)

    return render_template('secret.html', user =user)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<string:username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if "username" not in session:
        return redirect(f'/login') 

    form = FeedbackForm()
    if form.validate_on_submit():
        tittle = form.tittle.data
        content = form.content.data
        username = session['username']
        new_feedback = FeedBack(tittle=tittle,content =content,username =username)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback Created!', 'success')
        return redirect(f'/users/{username}')
    return render_template('addfeedback.html', form=form)


@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    if "username" not in session and username != session['username']:
        return redirect(f'/login')
     
    user =User.query.get_or_404(username) 
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted', 'success')
    session.pop('username')
    return redirect(f'/login') 


@app.route('/feedback/<int:feedbackid>/delete', methods=['POST'])
def delete_feedback(feedbackid):
    feedback =FeedBack.query.get_or_404(feedbackid) 
    if "username" not in session and feedback.username != session['username']:
        flash('You do not have privileges to delete this feedback', 'error')
        return redirect(f'/login') 
    
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback has been deleted', 'success')
    return redirect(f'/users/{feedback.username}')
    
@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def update_feedback(id):
    feedback =FeedBack.query.get_or_404(id) 
    if "username" not in session and feedback.username != session.get('username'):
        flash('You do not have privileges to update this feedback', 'error')
        return redirect(f'/login') 

    form = FeedbackForm(obj=feedback)
   
    if form.validate_on_submit():
        feedback.tittle =  form.tittle.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback Updated!', 'success')
        return redirect(f'/users/{feedback.username}')
    else:
         return render_template('updatefeedback.html', form=form, feedback =feedback)    
    


 
