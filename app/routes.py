from app import app, mongo
from app.forms import LoginForm, RegisterForm, CreateQuizForm, StandaloneQuestionForm
from app.models import User, Sign, Quiz, Question, QuizQuestion
from flask import redirect, url_for, flash, request, session, jsonify, current_app, render_template
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from bson import ObjectId,errors
import os
from math import ceil
from datetime import datetime



@app.route("/")
def home():
    return render_template("landing.html")  


"""@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(form.username.data)
        if user and User.check_password(user["password"], form.password.data):
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)"""

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"username": form.username.data})
        
        if user and check_password_hash(user["password"], form.password.data):
            session["user_id"] = str(user["_id"])
            session["role"] = user["role"]
            session["username"] = user["username"]  
            session["email"] = user["email"]  

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("user_dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.find_by_username(form.name.data)
        if existing_user:
            flash("Username already exists. Choose another.", "danger")
        else:
            User.create_user(form.name.data, form.email.data, form.name.data, form.password.data)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)

"""@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f"Welcome {session['username']}! You are logged in."
    else:
        flash("Please login first.", "warning")
        return redirect(url_for("login"))
"""
@app.route("/admin/dashboard")
def admin_dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html",username=session.get("username"),email=session.get("email"))

@app.route("/user/dashboard")
def user_dashboard():
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for("login"))
    return render_template("user_dashboard.html",username=session.get("username"),email=session.get("email"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

@app.route("/manage_learning")
def manage_learning():
    return render_template("manage_learning.html")


@app.route("/add_sign", methods=["POST"])
def add_sign():
    data = request.form
    image_file = request.files["image"]
    image_url = f"/static/uploads/{image_file.filename}"
    image_file.save(f"app/static/uploads/{image_file.filename}")

    mongo.db.signs.insert_one({
        "category": data["category"],
        "name": data["name"],
        "image": image_url,
        "description": data["description"]
    })
    return jsonify({"message": "Sign added successfully"})

@app.route("/get_signs", methods=["GET"])
def get_signs():
    page = int(request.args.get("page", 1))
    search_query = request.args.get("search", "")
    category = request.args.get("category", "")

    signs, total = Sign.get_signs(page=page, search_query=search_query, category=category)
    return jsonify({"signs": signs, "total": total})

"""
@app.route("/edit_sign/<sign_id>", methods=["PUT"])
def edit_sign(sign_id):
    data = request.json  # Get data from the frontend
    mongo.db.signs.update_one(
        {"_id": ObjectId(sign_id)},
        {"$set": {
            "name": data["name"],
            "description": data["description"]
        }}
    )
    return jsonify({"message": "Sign updated successfully"})

"""
UPLOAD_FOLDER = os.path.join("app","static", "sign_images")  # relative path
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
@app.route("/update_sign/<sign_id>", methods=["PUT"])
def update_sign(sign_id):
    try:
        # Find the existing sign in MongoDB
        sign = mongo.db.signs.find_one({"_id": ObjectId(sign_id)})
        if not sign:
            return jsonify({"error": "Sign not found"}), 404

        name = request.form.get("name", sign["name"])
        description = request.form.get("description", sign["description"])
        update_data = {"name": name, "description": description}

        # Ensure the upload folder exists
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Check if a new image is uploaded
        if "image" in request.files:
            image = request.files["image"]
            print(" Got image from form:", image.filename)
            if image.filename and "." in image.filename:
                ext = image.filename.rsplit(".", 1)[1].lower()
                if ext in ALLOWED_EXTENSIONS:
                    #image_filename = f"{sign_id}.{ext}"  # Save with sign ID
                    image_filename = f"{name.replace(' ', '_')}.{ext}"  # Use sign name
                    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                    print(f"Saving image to: {image_path}")
                    image.save(image_path)
                    print(" Image saved!")
                    update_data["image"] = f"/static/sign_images/{image_filename}"  # Update MongoDB

        # Update sign details in MongoDB
        mongo.db.signs.update_one({"_id": ObjectId(sign_id)}, {"$set": update_data})
        
        return jsonify({"message": "Sign updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

"""
@app.route("/update_sign/<sign_id>", methods=["PUT"])
def update_sign(sign_id):
    try:
        print("Received request:", request.form, request.files)
         # Validate ObjectId
        if not ObjectId.is_valid(sign_id):
            return jsonify({"error": "Invalid sign ID"}), 400
        sign = mongo.db.signs.find_one({"_id": ObjectId(sign_id)})
        if not sign:
            return jsonify({"error": "Sign not found"}), 404

        name = request.form.get("name", sign["name"]).strip()
        description = request.form.get("description", sign["description"]).strip()

        if not name or not description:
            return jsonify({"error": "Missing name or description"}), 400
        
        
        update_data = {"name": name, "description": description}

        # Check if a new image is uploaded
        if "image" in request.files and request.files["image"].filename :
            image = request.files["image"]
            image_path = f"static/uploads/{image.filename}"
            image.save(image_path)
            update_data["image"] = image_path  # Update image path in DB
        else:
            update_data["image"] = sign.get("image")  # Keep existing image

        # Update sign details in MongoDB
        mongo.db.signs.update_one({"_id": ObjectId(sign_id)}, {"$set": update_data})
        
        return jsonify({"message": "Sign updated successfully"}), 200

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"error": str(e)}), 500

"""
@app.route("/delete_sign/<sign_id>", methods=["DELETE"])
def delete_sign(sign_id):
    """Delete a sign entry by ID"""


    try:
        # Validate if sign_id is a valid ObjectId
        if not ObjectId.is_valid(sign_id):
            return jsonify({"error": "Invalid ID format"}), 400

        object_id = ObjectId(sign_id)  # Convert to ObjectId
        result = mongo.db.signs.delete_one({"_id": object_id})

        if result.deleted_count == 0:
            return jsonify({"error": "Sign not found"}), 404

        return jsonify({"message": "Sign deleted successfully"}), 200

    except errors.InvalidId:
        return jsonify({"error": "Invalid ObjectId"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/learning_module")
def learning_module():
    page = int(request.args.get("page", 1))
    search_query = request.args.get("search", "")
    category = request.args.get("category", "")

    signs, total = Sign.get_signs(page=page, search_query=search_query, category=category)

    return render_template("learning_module.html", signs=signs, total=total, page=page, search_query=search_query, category=category)



#-------------------------------practice module-----------------

@app.route('/practice')
def practice():
    return render_template('practice.html')

from flask import Response, jsonify
from ml_model.video_stream import generate_frames, get_latest_prediction

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_prediction')
def get_prediction():
    return jsonify({'prediction': get_latest_prediction()})

#-------------------------------------------------------------------------
@app.route('/quiz-admin-dashboard')
def quiz_admin_dashboard():
    # Count total users
    total_users = mongo.db.users.count_documents({})

    # Count total quizzes
    total_quizzes = mongo.db.quizzes.count_documents({})

    # Calculate average score from all quiz attempts
    attempts = list(mongo.db.quizattempts.find({}))
    total_attempts = len(attempts)

    if total_attempts > 0:
        total_score = sum(attempt.get("score", 0) for attempt in attempts)
        average_score = round(total_score / total_attempts, 2)
    else:
        average_score = 0

    return render_template(
        'quiz_admin_dashboard.html',  # << template name updated
        total_users=total_users,
        total_quizzes=total_quizzes,
        average_score=average_score,
        total_attempts=total_attempts
    )


#----------------------------------------------------testing image insertion to mongo------

@app.route('/admin/create_quiz', methods=['GET', 'POST'])
def create_quiz():
    form = CreateQuizForm()

    if form.validate_on_submit():
        try:
            # Add quiz to MongoDB
            Quiz.add_quiz(
                title=form.title.data,
                description=form.description.data,
                difficulty_level=form.difficulty_level.data,
            )
            # Flash success message
            flash('Quiz created successfully!', 'success')

            # Clear the form data after successful submission
            form.title.data = ''
            form.description.data = ''
            form.difficulty_level.data = ''

        except Exception as e:
            flash(str(e), 'danger')

    created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('create_quiz_only.html', form=form, created_at=created_at)
  

#--------------------create questions------------------

@app.route("/add_standalone_question", methods=["GET", "POST"])
def add_standalone_question():
    form = StandaloneQuestionForm()

    # Populate quiz_title dropdown
    quizzes = mongo.db.quizzes.find()
    form.quiz_title.choices = [('', 'None')] + [(quiz['title'], quiz['title']) for quiz in quizzes]

    if request.method == "POST":
        if form.validate_on_submit():
            # Save the question image if uploaded
            question_image = form.question_image.data
            media_path = None

            if question_image:
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                filename = secure_filename(question_image.filename)
                save_path = os.path.join(upload_folder, filename)
                question_image.save(save_path)
                media_path = f"/static/uploads/{filename}"

            # Prepare the options
            options = [
                {"option_text": form.option1.data},
                {"option_text": form.option2.data},
                {"option_text": form.option3.data},
                {"option_text": form.option4.data}
            ]

            # Add the standalone question
            question_id = Question.add_question(
                question_text=form.question_text.data,
                options=options,
                correct_answer=form.correct_answer.data,
                media_path=media_path
            )

            # If a quiz is selected, map the question to the quiz
            if form.quiz_title.data:
                quiz = mongo.db.quizzes.find_one({"title": form.quiz_title.data})
                if quiz:
                    QuizQuestion.add_quiz_question(
                        quiz_id=quiz["_id"],
                        question_id=question_id,
                        user=None
                    )

            flash("Question created successfully!", "success")
            return redirect(url_for('add_standalone_question'))
        else:
            print(form.errors)
    return render_template("create_questions.html", form=form)

#------------------------------ Edit Quizzes ------------------------------#
# Route to display quizzes with pagination
@app.route('/admin/quiz_management', methods=['GET'])
def quiz_management():
    try:
        page = int(request.args.get('page', 1))
        per_page = 10

        # Get filters
        search_query = request.args.get('search', '').strip()
        difficulty_filter = request.args.get('difficulty', '')
        sort_order = request.args.get('sort', '')

        # Build MongoDB query
        query = {}
        if search_query:
            query['title'] = {'$regex': search_query, '$options': 'i'}  # case-insensitive search
        if difficulty_filter:
            query['difficulty_level'] = difficulty_filter

        # Build sort option
        sort = [('created_at', -1)]  # Default: newest first
        if sort_order == 'oldest':
            sort = [('created_at', 1)]

        total_quizzes = mongo.db.quizzes.count_documents(query)
        quizzes_cursor = mongo.db.quizzes.find(query).sort(sort).skip((page - 1) * per_page).limit(per_page)
        quizzes = list(quizzes_cursor)

        total_pages = ceil(total_quizzes / per_page)

        return render_template('quiz_management.html', quizzes=quizzes, page=page, total_pages=total_pages)

    except Exception as e:
        flash(str(e), 'danger')
        return render_template('quiz_management.html', quizzes=[], page=1, total_pages=1)



@app.route('/admin/update_or_delete_quiz', methods=['POST'])
def update_or_delete_quiz():
    try:
        if 'update' in request.form:
            quiz_id = request.form['update']
            title = request.form.get(f'title_{quiz_id}')
            description = request.form.get(f'description_{quiz_id}')
            difficulty_level = request.form.get(f'difficulty_level_{quiz_id}')

            Quiz.update_quiz(quiz_id, title, description, difficulty_level)
            flash('Quiz updated successfully!', 'success')

        elif 'delete' in request.form:
            quiz_id = request.form['delete']
            Quiz.delete_quiz(quiz_id, user=None)

            flash('Quiz deleted successfully!', 'success')

    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('quiz_management', page=request.args.get('page', 1)))


#-------------------------questions update ----------------------
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from bson import ObjectId
import os

 # Make sure you have this!

# MongoDB setup
from app import mongo

# Collections
questions_collection = mongo.db.questions
quizzes_collection = mongo.db.quizzes
quizquestions_collection = mongo.db.quizquestions

# Upload folder
UPLOAD_FOLDER = 'app/static/uploads'  # adjust if needed
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ------------------------- ROUTES ----------------------------

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
import os
from math import ceil
from bson import ObjectId

@app.route('/admin/manage_questions', methods=['GET', 'POST'])
def manage_questions():
    try:
        page = int(request.args.get('page', 1))
        per_page = 10

        # Filters
        quiz_title = request.args.get('quiz_title', '')
        difficulty = request.args.get('difficulty', '')
        search = request.args.get('search', '').strip()

        # Query
        query = {}
        if search:
            query['question_text'] = {'$regex': search, '$options': 'i'}
        if difficulty:
            query['difficulty'] = difficulty
        if quiz_title:
            # Filter by quiz: Find all question_ids for this quiz first
            quiz = mongo.db.quizzes.find_one({'title': quiz_title})
            if quiz:
                quiz_question_ids = mongo.db.quizquestions.find({'quiz_id': quiz['_id']}).distinct('question_id')
                query['_id'] = {'$in': quiz_question_ids}
            else:
                query['_id'] = {'$in': []}  # No questions if quiz not found

        total_questions = mongo.db.questions.count_documents(query)
        questions_cursor = mongo.db.questions.find(query).skip((page - 1) * per_page).limit(per_page)
        questions = list(questions_cursor)

        # Get all quizzes for dropdown
        quizzes = list(mongo.db.quizzes.find())
        quiz_titles = [quiz['title'] for quiz in quizzes]

        total_pages = ceil(total_questions / per_page)

        return render_template('manage_questions.html', 
                               questions=questions, 
                               quiz_titles=quiz_titles, 
                               page=page, 
                               total_pages=total_pages)

    except Exception as e:
        flash(str(e), 'danger')
        return render_template('manage_questions.html', questions=[], quiz_titles=[], page=1, total_pages=1)


@app.route('/admin/update_or_delete_question', methods=['POST'])
def update_or_delete_question():
    try:
        if 'update' in request.form:
            question_id = request.form['update']
            question = mongo.db.questions.find_one({'_id': ObjectId(question_id)})
            if not question:
                flash('Question not found!', 'danger')
                return redirect(url_for('manage_questions'))

            # Get updated fields
            question_text = request.form.get(f'question_text_{question_id}')
            option1 = request.form.get(f'option1_{question_id}')
            option2 = request.form.get(f'option2_{question_id}')
            option3 = request.form.get(f'option3_{question_id}')
            option4 = request.form.get(f'option4_{question_id}')
            correct_answer = request.form.get(f'correct_answer_{question_id}')
            quiz_title = request.form.get(f'quiz_title_{question_id}')
            difficulty = request.form.get(f'difficulty_{question_id}')

            # Handle optional image update
            image_file = request.files.get(f'question_image_{question_id}')
            media_path = question.get('media_path')
            if image_file and image_file.filename:
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                filename = secure_filename(image_file.filename)
                save_path = os.path.join(upload_folder, filename)
                image_file.save(save_path)
                media_path = f'/static/uploads/{filename}'

            # Update in questions table
            mongo.db.questions.update_one(
                {'_id': ObjectId(question_id)},
                {'$set': {
                    'question_text': question_text,
                    'options': [
                        {'option_text': option1},
                        {'option_text': option2},
                        {'option_text': option3},
                        {'option_text': option4}
                    ],
                    'correct_answer': correct_answer,
                    'media_path': media_path,
                    'difficulty': difficulty
                }}
            )

            # Update in quizquestions if needed
            if quiz_title:
                quiz = mongo.db.quizzes.find_one({'title': quiz_title})
                if quiz:
                    # Check if mapping exists already
                    mapping = mongo.db.quizquestions.find_one({'question_id': ObjectId(question_id)})
                    if mapping:
                        mongo.db.quizquestions.update_one(
                            {'question_id': ObjectId(question_id)},
                            {'$set': {'quiz_id': quiz['_id']}}
                        )
                    else:
                        mongo.db.quizquestions.insert_one({
                            'quiz_id': quiz['_id'],
                            'question_id': ObjectId(question_id)
                        })

            flash('Question updated successfully!', 'success')

        elif 'delete' in request.form:
            question_id = request.form['delete']

            # Delete from questions table
            mongo.db.questions.delete_one({'_id': ObjectId(question_id)})

            # Also delete mapping in quizquestions table
            mongo.db.quizquestions.delete_many({'question_id': ObjectId(question_id)})

            flash('Question deleted successfully!', 'success')

    except Exception as e:
        flash(str(e), 'danger')

    return redirect(url_for('manage_questions', page=request.args.get('page', 1)))
