from mailbox import Message
import mailbox
from flask import Blueprint, app, jsonify, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User, Opportunity, Review, Application, UrgentHelp
from datetime import datetime


views=Blueprint('views', __name__)

#home page before logging in
@views.route('/')
def home():
    return render_template('home.html')

#students home page
@views.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # Quering/retrieving all opportunities from the database
    opportunities = Opportunity.query.all()
    
    # Quering/retrieving all notes from the database
    notes = UrgentHelp.query.all()

    # Returning both opportunities and notes in a single render_template call
    return render_template('index.html', opportunities=opportunities, notes=notes)

#sponsor posting opportunities
@views.route('/post', methods=['GET','POST'])
@login_required
def post():
    if request.method=='POST':
        title = request.form['title']
        description = request.form['description']
        type = request.form['type']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d') if request.form['deadline'] else None
        location = request.form['location']
    
        if current_user.role=='sponsor':
            new_opportunity = Opportunity(title=title, description=description, type=type, deadline=deadline, location=location, sponsor_id=current_user.id)
            db.session.add(new_opportunity)
            db.session.commit()
            flash('Opportunity successfully posted.', category='sucess')
            #return 'Opportunity posted'
        else:

          flash('Opportunity not posted.', category='error')
            #return ('Opportunity not posted')
        
    notes = UrgentHelp.query.all() 
    return render_template('post.html', notes=notes ,user=current_user)

#Adding note to the database
@views.route('/writenote', methods=['GET','POST'])
@login_required
def writenote():
    if request.method=='POST':
        content=request.form['content']

        new_note=UrgentHelp(note=content, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Message posted!', category='success')
        #return redirect(url_for('views.notes'))
    return render_template('writenote.html')

#getting notes from the database
@views.route('/notes',methods=['GET','POST'])
@login_required
def notes():
    notes=UrgentHelp.query.all()
    return render_template('notes.html', notes=notes)

#Adding reviews to the database
@views.route('/writereview', methods=['GET','POST'])
@login_required
def writereview():
       if request.method=='POST':
           content=request.form['content']

           new_review=Review(content=content, user_id=current_user.id)
           db.session.add(new_review)
           db.session.commit()
           flash('Review successfully added', category='sucesss')
           #return 'review added'#redirect(url_for('views.viewreviews'))
       return render_template('writereview.html')
       
#Getting reviews from the database
@views.route('/viewreviews', methods=['GET','POST'])
@login_required
def viewreviews():
   contents=Review.query.all()
   return render_template('viewreviews.html', contents=contents)




#Managing opportunities
@views.route('/manage_opportunities')
@login_required
def manage_opportunities():
    opportunities = Opportunity.query.filter_by(sponsor_id=current_user.id).all()
    return render_template('manage_opportunities.html', opportunities=opportunities)

#Viewing opportunity
@views.route('/view_opportunity/<int:id>')
@login_required
def view_opportunity(id):
    opportunity = Opportunity.query.get(id)
    if opportunity and opportunity.sponsor_id == current_user.id:
        return render_template('view_opportunity.html', opportunity=opportunity)
    flash('Opportunity not found or you do not have permission to view it', category='error')
    return redirect(url_for('views.manage_opportunities'))

#editing opportunity
@views.route('/edit_opportunity/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_opportunity(id):
    opportunity = Opportunity.query.get(id)
    if opportunity and opportunity.sponsor_id == current_user.id:
        if request.method == 'POST':
            opportunity.title = request.form['title']
            opportunity.description = request.form['description']
            opportunity.type = request.form['type']
            #opportunity.deadline = request.form['deadline']
            deadline = datetime.strptime('2024-03-30T00:00', '%Y-%m-%dT%H:%M')
            opportunity.location = request.form['location']
            db.session.commit() 
            flash('Opportunity updated successfully!', category='success')
            return redirect(url_for('views.manage_opportunities'))
        return render_template('edit_opportunity.html', opportunity=opportunity)
    flash('Opportunity not found or you do not have permission to edit it', category='error')
    return redirect(url_for('views.manage_opportunities'))

#Deleting opportunity
@views.route('/delete_opportunity/<int:id>', methods=['POST'])
@login_required
def delete_opportunity(id):
    opportunity = Opportunity.query.get(id)
    if opportunity and opportunity.sponsor_id == current_user.id:
        db.session.delete(opportunity)
        db.session.commit()
        flash('Opportunity deleted successfully!', category='success')
    else:
        flash('Opportunity not found or you do not have permission to delete it', category='error')
    return redirect(url_for('views.manage_opportunities'))


from flask import render_template, redirect, url_for, flash
from .models import Opportunity

@views.route('/view_opportunity4btn/<int:opportunity_id>', methods=['GET', 'POST'])
def view_opportunity4btn(opportunity_id):
    # Fetch the opportunity details from the database using the opportunity_id
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    
    if request.method == 'POST':
        # Handle the form submission if needed
        pass
    
    # Render the template with the opportunity details
    return render_template('view_opportunity4btn.html', opportunity=opportunity)




#Admin activities
@views.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@views.route('/opportunities')
def view_opportunities():  
    # Retrieve opportunities data from the database
    opportunities = Opportunity.query.all()
    return render_template('opportunities.html', opportunities=opportunities)

@views.route('/reviews')
def view_reviews():
    # Retrieve reviews data from the database
    reviews = Review.query.all()
    return render_template('admin/reviews.html', reviews=reviews)

@views.route('/urgent_notes')
def view_urgent_notes():
    # Retrieve urgent notes data from the database
    urgent_notes =UrgentHelp.query.all()
    return render_template('admin/urgent_notes.html', urgent_notes=urgent_notes)

@views.route('/manage_users')
def manage_users():
    # Retrieve users from the database
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@views.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.role=request.form['role']
        # Update other user attributes as needed
        db.session.commit()
        return redirect(url_for('manage_users'))
    return render_template('edit_user.html', user=user)

from flask import redirect, url_for

@views.route('/delete_user/<int:user_id>', methods=['GET','POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return 'User deleted'


#Opportunity dropdownlist
#get bursaries
@views.route('/get_bursaries', methods=['GET'])
@login_required
def get_bursaries():
    # Retrieve bursaries from the database where the type is 'bursary'
    bursaries = Opportunity.query.filter_by(type='Bursary').all()
    return render_template('get_bursaries.html', bursaries=bursaries)

#get scholaships
@views.route('/get_scholarships', methods=['GET','POST'])
@login_required
def get_scholarships():
        scholarships=Opportunity.query.filter_by(type='Scholarship').all()
        return render_template('get_scholarships.html', scholarships=scholarships)

#get grants
@views.route('/get_grants', methods=['GET','POST'])
@login_required
def get_grants():
        grant=Opportunity.query.filter_by(type='Grant').all()
        return render_template('get_grants.html', grant=grant)

#get internships
@views.route('/get_internships', methods=['GET','POST'])
@login_required
def get_internships():
        internships=Opportunity.query.filter_by(type='Internship').all()
        return render_template('get_internships.html', internships=internships)

@views.route('/get_learnerships', methods=['GET','POST'])
@login_required
def get_learnership():
        learnerships=Opportunity.query.filter_by(type='Learnership').all()
        return render_template('get_learnership.html', learnerships=learnerships)

#email
@views.route('/send_email', methods=['POST', 'GET'])
@login_required
def send_email():
    recipient = request.form.get('recipient')
    subject = request.form.get('subject')
    message_body = request.form.get('message')

    if not recipient or not subject or not message_body:
        return jsonify({'error': 'Recipient, subject, and message are required.'}), 400
    try:    
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = message_body
        mailbox.send(msg)
        # Render the 'email_sent.html' template
        return render_template('email_sent.html', recipient=recipient, subject=subject), 200
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500
