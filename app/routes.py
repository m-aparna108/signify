from app import app, mongo
from flask import render_template
from app.forms import LoginForm, RegisterForm
from app.models import User
from flask import redirect, url_for, flash, request, session
from werkzeug.security import check_password_hash
from flask import request, jsonify
from bson import ObjectId,errors
from app.models import Sign
import os
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
UPLOAD_FOLDER = "static/sign_images/"  # Store images in this folder
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
            if image.filename and "." in image.filename:
                ext = image.filename.rsplit(".", 1)[1].lower()
                if ext in ALLOWED_EXTENSIONS:
                    #image_filename = f"{sign_id}.{ext}"  # Save with sign ID
                    image_filename = f"{name.replace(' ', '_')}.{ext}"  # Use sign name
                    image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                    image.save(image_path)
                    update_data["image"] = image_path  # Update MongoDB

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





from app import routes