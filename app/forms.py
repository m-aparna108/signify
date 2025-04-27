from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import StringField, SelectField, SubmitField

# Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Registration Form
class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")



#-------------------------for testing---------
class CreateQuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()])
    description = StringField('Description')
    difficulty_level = SelectField('Difficulty Level', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], validators=[DataRequired()])
    submit = SubmitField('Create Quiz')

#-----------------------for create question-----------
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Optional

class StandaloneQuestionForm(FlaskForm):
    # Question text
    question_text = StringField('Question Text', validators=[DataRequired()])
    # Question image (optional)
    question_image = FileField('Question Image (optional)', validators=[Optional()])
    # Answer options
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    # Correct answer
    correct_answer = SelectField('Correct Answer', choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')], validators=[DataRequired()])
    # Assign to quiz (optional)
    quiz_title = SelectField('Assign to Quiz (Optional)', choices=[], validators=[Optional()])
    # Submit button
    submit = SubmitField('Create Question')

    