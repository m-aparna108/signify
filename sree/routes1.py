
#------------------------------------------------------------------
# quiz create 
from flask import Blueprint, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from bson import ObjectId
import os
import datetime
from flask_login import current_user
from functools import wraps
from app import mongo, login_manager
from app.models import User
from app.forms1 import QuizWithQuestionForm, StandaloneQuestionForm, QuestionToQuizForm

quiz_bp = Blueprint('quiz', __name__)
UPLOAD_FOLDER = 'app/static/uploads'  # adjust as needed

from datetime import datetime
import pytz

local_tz = pytz.timezone('Asia/Kolkata')


# Utility: Save uploaded file and return relative path
def save_media_file(file):
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return f"uploads/{filename}"
    return None

# Admin check decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('login'))  # or wherever your login route is
        return f(*args, **kwargs)
    return decorated_function

# Routes for creating quiz and questions...

# Route: Create quiz with first (or multiple) questions
@quiz_bp.route('/create_quiz_with_question', methods=['POST'])
def create_quiz_with_question():
    title = request.form.get("quiz_title")
    description = request.form.get("quiz_description")
    difficulty = request.form.get("quiz_difficulty")

    if not title or not difficulty:
        flash("Title and difficulty are required.", "error")
        return redirect(url_for('quiz.quiz_create'))

    quiz_id = mongo.db.quizzes.insert_one({
        "title": title,
        "description": description,
        "difficulty_level": difficulty,
        "created_at": datetime.now(local_tz)
    }).inserted_id

    titles = request.form.getlist("question_title[]")
    correct_answers = request.form.getlist("correct_answer[]")
    question_medias = request.files.getlist("question_media[]")
    options_a = request.form.getlist("option_a[]")
    options_b = request.form.getlist("option_b[]")
    options_c = request.form.getlist("option_c[]")
    options_d = request.form.getlist("option_d[]")
    option_a_medias = request.files.getlist("option_a_media[]")
    option_b_medias = request.files.getlist("option_b_media[]")
    option_c_medias = request.files.getlist("option_c_media[]")
    option_d_medias = request.files.getlist("option_d_media[]")

    for i in range(len(titles)):
        q_media = save_media_file(question_medias[i]) if i < len(question_medias) else None
        o_a_media = save_media_file(option_a_medias[i]) if i < len(option_a_medias) else None
        o_b_media = save_media_file(option_b_medias[i]) if i < len(option_b_medias) else None
        o_c_media = save_media_file(option_c_medias[i]) if i < len(option_c_medias) else None
        o_d_media = save_media_file(option_d_medias[i]) if i < len(option_d_medias) else None

        question_id = mongo.db.questions.insert_one({
            "title": titles[i],
            "media": q_media,
            "options": {
                "A": {"text": options_a[i], "media": o_a_media},
                "B": {"text": options_b[i], "media": o_b_media},
                "C": {"text": options_c[i], "media": o_c_media},
                "D": {"text": options_d[i], "media": o_d_media},
            },
            "correct_answer": correct_answers[i],
            "created_at": datetime.now(local_tz)
        }).inserted_id
        
        mongo.db.quizquestions.insert_one({
            "quiz_id": quiz_id,
            "question_id": question_id,
            "created_at": datetime.now(local_tz)
        })

    flash("Quiz and questions created successfully!", "success")
    return redirect(url_for('quiz.quiz_create'))

# Route: Add standalone question (not tied to any quiz)
@quiz_bp.route('/add_standalone_question', methods=['POST'])
def add_standalone_question():
    print("inside the add_standalone")
    titles = request.form.getlist("question_title[]")
    correct_answers = request.form.getlist("correct_answer[]")
    question_medias = request.files.getlist("question_media[]")
    options_a = request.form.getlist("option_a[]")
    options_b = request.form.getlist("option_b[]")
    options_c = request.form.getlist("option_c[]")
    options_d = request.form.getlist("option_d[]")
    option_a_medias = request.files.getlist("option_a_media[]")
    option_b_medias = request.files.getlist("option_b_media[]")
    option_c_medias = request.files.getlist("option_c_media[]")
    option_d_medias = request.files.getlist("option_d_media[]")
    print("Form data received:")
    print("Titles:", request.form.getlist("question_title[]"))
    print("Correct answers:", request.form.getlist("correct_answer[]"))
    print("Option A:", request.form.getlist("option_a[]"))
    print("Files:", request.files.getlist("question_media[]"))
    for i in range(len(titles)):
        print("inside the for in range ")
        q_media = save_media_file(question_medias[i]) if i < len(question_medias) else None
        o_a_media = save_media_file(option_a_medias[i]) if i < len(option_a_medias) else None
        o_b_media = save_media_file(option_b_medias[i]) if i < len(option_b_medias) else None
        o_c_media = save_media_file(option_c_medias[i]) if i < len(option_c_medias) else None
        o_d_media = save_media_file(option_d_medias[i]) if i < len(option_d_medias) else None
        print ("270")
        mongo.db.questions.insert_one({
            "title": titles[i],
            "media": q_media,
            "options": {
                "A": {"text": options_a[i], "media": o_a_media},
                "B": {"text": options_b[i], "media": o_b_media},
                "C": {"text": options_c[i], "media": o_c_media},
                "D": {"text": options_d[i], "media": o_d_media},
            },
            "correct_answer": correct_answers[i],
            "created_at": datetime.now(local_tz)
        })
        print("Quiz created at:", datetime.now(local_tz))
    print("flash cad")
    flash("Standalone question(s) added successfully!", "success")
    print("working")
    return redirect(url_for('quiz.quiz_create'))

# Route: Add question(s) to an existing quiz by title
@quiz_bp.route('/add_question_to_quiz', methods=['POST'])
def add_question_to_quiz():
    titles = request.form.getlist("question_title[]")
    quiz_titles = request.form.getlist("assign_quiz[]")
    correct_answers = request.form.getlist("correct_answer[]")
    question_medias = request.files.getlist("question_media[]")
    options_a = request.form.getlist("option_a[]")
    options_b = request.form.getlist("option_b[]")
    options_c = request.form.getlist("option_c[]")
    options_d = request.form.getlist("option_d[]")
    option_a_medias = request.files.getlist("option_a_media[]")
    option_b_medias = request.files.getlist("option_b_media[]")
    option_c_medias = request.files.getlist("option_c_media[]")
    option_d_medias = request.files.getlist("option_d_media[]")

    for i in range(len(titles)):
        quiz_title = quiz_titles[i]
        quiz = mongo.db.quizzes.find_one({"title": quiz_title})
        if not quiz:
            flash(f"Quiz '{quiz_title}' not found.", "error")
            continue

        q_media = save_media_file(question_medias[i]) if i < len(question_medias) else None
        o_a_media = save_media_file(option_a_medias[i]) if i < len(option_a_medias) else None
        o_b_media = save_media_file(option_b_medias[i]) if i < len(option_b_medias) else None
        o_c_media = save_media_file(option_c_medias[i]) if i < len(option_c_medias) else None
        o_d_media = save_media_file(option_d_medias[i]) if i < len(option_d_medias) else None

        question_id = mongo.db.questions.insert_one({
            "title": titles[i],
            "media": q_media,
            "options": {
                "A": {"text": options_a[i], "media": o_a_media},
                "B": {"text": options_b[i], "media": o_b_media},
                "C": {"text": options_c[i], "media": o_c_media},
                "D": {"text": options_d[i], "media": o_d_media},
            },
            "correct_answer": correct_answers[i],
            "created_at": datetime.now(local_tz)
        }).inserted_id

        mongo.db.quizquestions.insert_one({
            "quiz_id": quiz["_id"],
            "question_id": question_id,
            "created_at": datetime.now(local_tz)
        })

    flash("Question(s) successfully added to existing quiz!", "success")
    return redirect(url_for('quiz.quiz_create'))



@quiz_bp.route('/quiz/create', methods=['GET', 'POST'])

def quiz_create():
    quiz_form = QuizWithQuestionForm()
    standalone_question_form = StandaloneQuestionForm()
    question_to_quiz_form = QuestionToQuizForm()

    all_quizzes = list(mongo.db.quizzes.find({}))  # assuming you're using MongoDB

    return render_template(
        'quiz_create.html',
        quiz_form=quiz_form,
        standalone_question_form=standalone_question_form,
        question_to_quiz_form=question_to_quiz_form,
        all_quizzes=all_quizzes
    )

#-------------------------------------------------------------------------------------------------
