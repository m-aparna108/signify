from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
from bson.objectid import ObjectId
from werkzeug.exceptions import BadRequest, Forbidden
from datetime import datetime
"""class User:
   

    @staticmethod
    def create_user(name, email, username, password):
      
        hashed_password = generate_password_hash(password)
        user_data = {"name": name, "email": email, "username": username, "password": hashed_password}
        mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
       
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def check_password(stored_password, provided_password):
        
        return check_password_hash(stored_password, provided_password)
"""
class User:
    """User model for MongoDB"""

    @staticmethod
    def create_user(name, email, username, password):
        """Create a new user with a hashed password and assign role"""

        # Check if an admin already exists
        existing_admin = mongo.db.users.find_one({"role": "admin"})
        
        # If no admin exists, first user is admin; others are normal users
        role = "admin" if not existing_admin else "user"

        hashed_password = generate_password_hash(password)
        user_data = {
            "name": name,
            "email": email,
            "username": username,
            "password": hashed_password,
            "role": role
        }
        mongo.db.users.insert_one(user_data)

    @staticmethod
    def find_by_username(username):
        """Find user by username and return all details"""
        return mongo.db.users.find_one({"username": username})

    @staticmethod
    def check_password(stored_password, provided_password):
        """Check if the password matches"""
        return check_password_hash(stored_password, provided_password)
    

    
"""
class Sign:
    #Sign model for managing sign language learning content

    @staticmethod
    def add_sign(category, name, image, description):
        #Add a new sign language entry
        sign_data = {
            "category": category,
            "name": name,
            "image": image,  # Image can be stored as a URL or base64
            "description": description
        }
        mongo.db.signs.insert_one(sign_data)

    @staticmethod
    def get_signs(page=1, per_page=5, search_query=None, category=None):
        #Retrieve signs with pagination, search, and category filter
        query = {}
        if search_query:
            query["name"] = {"$regex": search_query, "$options": "i"}
        if category:
            query["category"] = category

        signs = (
            mongo.db.signs.find(query)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
        total = mongo.db.signs.count_documents(query)

        return list(signs), total
    


    

    @staticmethod
    def update_sign(sign_id, category, name, image, description):
        #Update an existing sign
        mongo.db.signs.update_one(
            {"_id": sign_id},
            {"$set": {"category": category, "name": name, "image": image, "description": description}}
        )

    @staticmethod
    def delete_sign(sign_id):
        #Delete a sign entry
        mongo.db.signs.delete_one({"_id": sign_id})




    @staticmethod
    def update_sign(sign_id, category, name, image, description):
        #Update an existing sign
        mongo.db.signs.update_one(
            {"_id": ObjectId(sign_id)},  # Convert string ID to ObjectId
            {"$set": {"category": category, "name": name, "image": image, "description": description}}
        )

    @staticmethod
    def delete_sign(sign_id):
        #Delete a sign entry
        mongo.db.signs.delete_one({"_id": ObjectId(sign_id)})  # Convert string ID to ObjectId
"""

class Sign:
    """Sign model for managing sign language learning content"""

    @staticmethod
    def add_sign(category, name, image, description):
        """Add a new sign language entry"""
        sign_data = {
            "category": category,
            "name": name,
            "image": image,  # Image can be stored as a URL or base64
            "description": description
        }
        mongo.db.signs.insert_one(sign_data)

    @staticmethod
    def get_signs(page=1, per_page=5, search_query=None, category=None):
        """Retrieve signs with pagination, search, and category filter"""
        query = {}
        if search_query:
            query["name"] = {"$regex": search_query, "$options": "i"}
        if category:
            query["category"] = category

        signs = (
            mongo.db.signs.find(query)
            .skip((page - 1) * per_page)
            .limit(per_page)
        )
        total = mongo.db.signs.count_documents(query)

        return list(signs), total

    @staticmethod
    def update_sign(sign_id, category, name, image, description):
        """Update an existing sign"""
        try:
            object_id = ObjectId(sign_id)  # Convert sign_id to ObjectId
            mongo.db.signs.update_one(
                {"_id": object_id},
                {"$set": {"category": category, "name": name, "image": image, "description": description}}
            )
            return True
        except Exception as e:
            print(f"Update Error: {e}")
            return False

    @staticmethod
    def delete_sign(sign_id):
        """Delete a sign entry"""
        try:
            object_id = ObjectId(sign_id)  # Convert sign_id to ObjectId
            mongo.db.signs.delete_one({"_id": object_id})
            return True
        except Exception as e:
            print(f"Deletion Error: {e}")
            return False

#-----------------------testing----------------

class Quiz:
    """Model for managing quizzes"""

    @staticmethod
    def add_quiz(title, description, difficulty_level):
        

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
    def update_quiz(quiz_id, title, description, difficulty_level):
        

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
       
        mongo.db.quizzes.delete_one({"_id": ObjectId(quiz_id)})

    @staticmethod
    def get_quiz(quiz_id):
        """Retrieve a quiz by ID"""
        return mongo.db.quizzes.find_one({"_id": ObjectId(quiz_id)})

#------------------------------------------------------------------------


class Question:
    """Model for managing questions"""

    @staticmethod
    def add_question(question_text, options, correct_answer, media_path=None):
        """Add a new question"""
        question = {
            "question_text": question_text,
            "options": options,
            "correct_answer": correct_answer,
            "media_path": media_path,
            "created_at": datetime.utcnow()
        }
        result = mongo.db.questions.insert_one(question)
        return str(result.inserted_id)

    @staticmethod
    def get_question_by_id(question_id):
        """Retrieve a question by its ID"""
        question = mongo.db.questions.find_one({"_id": ObjectId(question_id)})
        return question

    @staticmethod
    def update_question(question_id, updated_data):
        """Update an existing question"""
        result = mongo.db.questions.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": updated_data}
        )
        return result.modified_count

    @staticmethod
    def delete_question(question_id):
        """Delete a question by its ID"""
        result = mongo.db.questions.delete_one({"_id": ObjectId(question_id)})
        return result.deleted_count


class QuizQuestion:
    """Model for managing quiz-question mappings"""

    @staticmethod
    def add_quiz_question(quiz_id, question_id, user):
        """Map a question to a quiz (admin only)"""
        

        mapping_data = {
            "quiz_id": ObjectId(quiz_id),
            "question_id": ObjectId(question_id),
            "created_at": datetime.utcnow()
        }
        result = mongo.db.quizquestions.insert_one(mapping_data)
        return str(result.inserted_id)

    @staticmethod
    def get_questions_for_quiz(quiz_id):
        """Retrieve all questions linked to a specific quiz"""
        mappings = list(mongo.db.quizquestions.find({"quiz_id": ObjectId(quiz_id)}))
        question_ids = [mapping["question_id"] for mapping in mappings]
        return list(mongo.db.questions.find({"_id": {"$in": question_ids}}))



from app import mongo