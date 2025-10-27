from django.contrib.auth.decorators import login_required
from flask import Flask, render_template, request, redirect, url_for,flash
from flask_login import LoginManager, current_user
from werkzeug.utils import secure_filename
import os
import time

from routes.models_routes import User, db
from routes.authentication import authentication_route

app = Flask(__name__)
app.secret_key = "jhguyhiugnbk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'static/profile_pics'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

login_manager = LoginManager(app)
login_manager.login_view = "login_page"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Database of user
db.init_app(app)
user_db = User()

#Authentication route
authentication_route(app)


@app.route('/')
def home_page():
    if current_user.is_authenticated:
        user_info = {
            "fullname": current_user.fullname,
            "email": current_user.email,
            "profile_image": current_user.profile_image,
            "user_name": current_user.user_name,
        }
    else:
        return redirect(url_for('landing_page'))

    return render_template('home.html', user_info=user_info)

@app.route('/profile')
def user_profile():
    user_info = {
        "fullname": current_user.fullname,
        "email": current_user.email,
        "profile_image": current_user.profile_image,
        "user_name": current_user.user_name,
        "about": current_user.about,
        "profession": current_user.profession,
        "bio": current_user.bio,

    }
    return render_template('profile.html', user_info=user_info)

@app.route('/landing_page')
def landing_page():
    return render_template('landing_page.html')


@app.route('/editing_profile', methods=['GET', 'POST'])
def editing_profile_page():
    if request.method == 'POST':
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    try:
                        # Generate unique filename to avoid conflicts
                        file_text = os.path.splitext(file.filename)[1]
                        filename = secure_filename(f"{current_user.id}_{int(time.time())}{file_text}")
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        # Save file
                        file.save(file_path)
                        # Update database
                        current_user.profile_image = filename

                        flash('Profile picture updated successfully!', 'success')
                        updated = True
                    except Exception as e:
                        print(f"Error saving file: {str(e)}")
                        flash('Error updating profile picture', 'error')
                else:
                    flash('Invalid file type', 'error')

        #getting other info from user
        username = request.form.get('user_name')
        if username and current_user.user_name != username:
            current_user.user_name = username
            flash('Username updated successfully!', 'success')
            updated = True

        about = request.form.get('about')
        if about and current_user.about != about:
            current_user.about = about
            flash('Your about updated successfully!', 'success')
            updated = True

        profession = request.form.get('profession')
        if profession and current_user.profession != profession:
            current_user.profession = profession
            flash('Your profession updated successfully!', 'success')
            updated = True

        bio = request.form.get('bio')
        if bio and current_user.bio != bio:
            current_user.bio = bio
            flash('Your bio updated successfully!', 'success')
            updated = True

        if updated:
            db.session.commit()

        return redirect(url_for('editing_profile_page'))

    user_info = {
        "fullname": current_user.fullname,
        "email": current_user.email,
        "profile_image": current_user.profile_image,
        "user_name": current_user.user_name,
        "about": current_user.about,
        "profession": current_user.profession,
        "bio": current_user.bio,
    }
    return render_template('edite_profile.html', user_info=user_info)

@app.route('/post_blog')
def post_blog():
    return render_template('make_post.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)