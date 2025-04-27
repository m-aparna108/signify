from datetime import datetime
from bson.objectid import ObjectId
from app import mongo
from werkzeug.exceptions import BadRequest, Forbidden


def require_admin(user):
    if not user or user.get("role") != "admin":
        raise Forbidden("Admin access required.")


class Question:
    """Model for managing questions"""

    @staticmethod
    def add_question(
        question_text,
        question_media_path,  # <-- path to the question image/audio/video
        option_1,
        option_2,
        option_3,
        option_4,
        option_1_media_path,
        option_2_media_path,
        option_3_media_path,
        option_4_media_path,
        correct_answer,
        sign_id,
        user
    ):
        """Add a new question with validation and admin check"""
        require_admin(user)

        if not question_text or not all([option_1, option_2, option_3, option_4]):
            raise BadRequest("Question text and all options are required.")

        if correct_answer not in [1, 2, 3, 4]:
            raise BadRequest("Correct answer must be 1, 2, 3, or 4.")

        question_data = {
            "question_text": question_text,
            "question_media": question_media_path,
            "options": [
                {"text": option_1, "media": option_1_media_path},
                {"text": option_2, "media": option_2_media_path},
                {"text": option_3, "media": option_3_media_path},
                {"text": option_4, "media": option_4_media_path}
            ],
            "correct_answer": correct_answer,
            "sign_id": ObjectId(sign_id) if sign_id else None
        }
        mongo.db.questions.insert_one(question_data)

    @staticmethod
    def update_question(
        question_id,
        question_text,
        question_media_path,
        option_1,
        option_2,
        option_3,
        option_4,
        option_1_media_path,
        option_2_media_path,
        option_3_media_path,
        option_4_media_path,
        correct_answer,
        sign_id,
        user
    ):
        """Update an existing question with validation and admin check"""
        require_admin(user)

        if correct_answer not in [1, 2, 3, 4]:
            raise BadRequest("Correct answer must be 1, 2, 3, or 4.")

        updated_data = {
            "question_text": question_text,
            "question_media": question_media_path,
            "options": [
                {"text": option_1, "media": option_1_media_path},
                {"text": option_2, "media": option_2_media_path},
                {"text": option_3, "media": option_3_media_path},
                {"text": option_4, "media": option_4_media_path}
            ],
            "correct_answer": correct_answer,
            "sign_id": ObjectId(sign_id) if sign_id else None
        }
        mongo.db.questions.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": updated_data}
        )

    @staticmethod
    def delete_question(question_id, user):
        """Delete a question by ID (admin only)"""
        require_admin(user)
        mongo.db.questions.delete_one({"_id": ObjectId(question_id)})

    @staticmethod
    def get_question(question_id):
        """Retrieve a question by ID"""
        return mongo.db.questions.find_one({"_id": ObjectId(question_id)})


class Quiz:
    """Model for managing quizzes"""

    @staticmethod
    def add_quiz(title, description, difficulty_level, user):
        """Add a new quiz with validation and admin check"""
        require_admin(user)

        if difficulty_level not in ["Easy", "Medium", "Hard"]:
            raise BadRequest("Difficulty level must be 'Easy', 'Medium', or 'Hard'.")

        quiz_data = {
            "title": title,
            "description": description,
            "created_at": datetime.utcnow(),
            "difficulty_level": difficulty_level
        }
        mongo.db.quizzes.insert_one(quiz_data)

    @staticmethod
    def update_quiz(quiz_id, title, description, difficulty_level, user):
        """Update an existing quiz with validation"""
        require_admin(user)

        if difficulty_level not in ["Easy", "Medium", "Hard"]:
            raise BadRequest("Invalid difficulty level.")

        mongo.db.quizzes.update_one(
            {"_id": ObjectId(quiz_id)},
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "difficulty_level": difficulty_level
                }
            }
        )

    @staticmethod
    def delete_quiz(quiz_id, user):
        """Delete a quiz (admin only)"""
        require_admin(user)
        mongo.db.quizzes.delete_one({"_id": ObjectId(quiz_id)})

    @staticmethod
    def get_quiz(quiz_id):
        """Retrieve a quiz by ID"""
        return mongo.db.quizzes.find_one({"_id": ObjectId(quiz_id)})


class QuizQuestion:
    """Model for managing quiz-question mappings"""

    @staticmethod
    def add_quiz_question(quiz_id, question_id, user):
        """Map a question to a quiz (admin only)"""
        require_admin(user)

        mapping_data = {
            "quiz_id": ObjectId(quiz_id),
            "question_id": ObjectId(question_id),
            "created_at": datetime.utcnow()
        }
        mongo.db.quizquestions.insert_one(mapping_data)

    @staticmethod
    def get_questions_for_quiz(quiz_id):
        """Retrieve all questions for a quiz"""
        mappings = list(mongo.db.quizquestions.find({"quiz_id": ObjectId(quiz_id)}))
        question_ids = [m["question_id"] for m in mappings]
        return list(mongo.db.questions.find({"_id": {"$in": question_ids}}))


class QuizAttempt:
    """Model for managing quiz attempts"""

    @staticmethod
    def add_attempt(user_id, quiz_id, score):
        """Record a quiz attempt"""
        attempt_data = {
            "user_id": ObjectId(user_id),
            "quiz_id": ObjectId(quiz_id),
            "score": score,
            "attempt_date": datetime.utcnow()
        }
        mongo.db.quizattempts.insert_one(attempt_data)

    @staticmethod
    def get_attempts_by_user(user_id):
        """Get all attempts for a user"""
        return list(mongo.db.quizattempts.find({"user_id": ObjectId(user_id)}))

    @staticmethod
    def get_attempts_for_quiz(quiz_id):
        """Get all attempts for a quiz"""
        return list(mongo.db.quizattempts.find({"quiz_id": ObjectId(quiz_id)}))

#----------------------------------------------------------------------------------
# Example User model
# app/models1.py
from flask_login import UserMixin  # Ensure this is imported

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        # Add other attributes as needed

    @staticmethod
    def get(user_id):
        # Replace with your actual logic to fetch the user from MongoDB
        user_data = mongo.db.users.find_one({"user_id": user_id})
        if user_data:
            user = User(user_data["user_id"])
            # Add other attributes if needed
            return user
        return None

from datetime import datetime
from bson.objectid import ObjectId
from app import mongo
from werkzeug.exceptions import BadRequest


class QuizAttempt:
    """Model for managing quiz attempts"""

    @staticmethod
    def add_attempt(user_id, quiz_id, score):
        """Record a new quiz attempt"""
        if not user_id or not quiz_id:
            raise BadRequest("User ID and Quiz ID are required.")
        if not isinstance(score, (int, float)):
            raise BadRequest("Score must be a number.")

        attempt_data = {
            "user_id": ObjectId(user_id),
            "quiz_id": ObjectId(quiz_id),
            "score": score,
            "attempt_date": datetime.utcnow()
        }
        result = mongo.db.quizattempts.insert_one(attempt_data)
        return str(result.inserted_id)

    @staticmethod
    def get_attempt(attempt_id):
        """Retrieve a specific attempt by attempt_id"""
        return mongo.db.quizattempts.find_one({"_id": ObjectId(attempt_id)})

    @staticmethod
    def get_attempts_by_user(user_id):
        """Retrieve all attempts made by a specific user"""
        return list(mongo.db.quizattempts.find({"user_id": ObjectId(user_id)}))

    @staticmethod
    def get_attempts_for_quiz(quiz_id):
        """Retrieve all attempts for a specific quiz"""
        return list(mongo.db.quizattempts.find({"quiz_id": ObjectId(quiz_id)}))

    @staticmethod
    def delete_attempt(attempt_id):
        """Delete a specific attempt by attempt_id"""
        mongo.db.quizattempts.delete_one({"_id": ObjectId(attempt_id)})

    @staticmethod
    def update_attempt_score(attempt_id, new_score):
        """Update the score of a specific attempt"""
        if not isinstance(new_score, (int, float)):
            raise BadRequest("New score must be a number.")
        
        mongo.db.quizattempts.update_one(
            {"_id": ObjectId(attempt_id)},
            {"$set": {"score": new_score}}
        )
