from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo
from bson.objectid import ObjectId

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


from app import mongo