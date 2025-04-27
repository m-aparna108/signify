from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Optional, ValidationError

def validate_question_or_media(form, field):
    """Ensure that either question text or media is provided."""
    if not form.question_text.data and not form.question_media.data:
        raise ValidationError("Either question text or media is required.")

def validate_option_or_media(form, field):
    """Ensure that either option text or media is provided."""
    option_number = field.name.split("_")[-1]  # e.g., 'option_1', 'option_2'
    option_text = getattr(form, f"option_{option_number}").data
    option_media = getattr(form, f"option_{option_number}_media").data

    if not option_text and not option_media:
        raise ValidationError(f"Either option {option_number} text or media is required.")

class QuizWithQuestionForm(FlaskForm):
    # Quiz fields
    title = StringField("Quiz Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    difficulty_level = SelectField("Difficulty", choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Hard", "Hard")])

    # Question fields
    question_text = TextAreaField("Question Text", validators=[Optional(), validate_question_or_media])
    question_media = FileField("Question Media", validators=[Optional()])

    option_1 = StringField("Option 1 Text", validators=[Optional(), validate_option_or_media])
    option_1_media = FileField("Option 1 Media", validators=[Optional()])

    option_2 = StringField("Option 2 Text", validators=[Optional(), validate_option_or_media])
    option_2_media = FileField("Option 2 Media", validators=[Optional()])

    option_3 = StringField("Option 3 Text", validators=[Optional(), validate_option_or_media])
    option_3_media = FileField("Option 3 Media", validators=[Optional()])

    option_4 = StringField("Option 4 Text", validators=[Optional(), validate_option_or_media])
    option_4_media = FileField("Option 4 Media", validators=[Optional()])

    correct_answer = SelectField("Correct Answer", choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], coerce=int)



class StandaloneQuestionForm(FlaskForm):
    question_text = TextAreaField("Question Text", validators=[Optional(), validate_question_or_media])
    question_media = FileField("Question Media", validators=[Optional()])

    option_1 = StringField("Option 1 Text", validators=[Optional(), validate_option_or_media])
    option_1_media = FileField("Option 1 Media", validators=[Optional()])

    option_2 = StringField("Option 2 Text", validators=[Optional(), validate_option_or_media])
    option_2_media = FileField("Option 2 Media", validators=[Optional()])

    option_3 = StringField("Option 3 Text", validators=[Optional(), validate_option_or_media])
    option_3_media = FileField("Option 3 Media", validators=[Optional()])

    option_4 = StringField("Option 4 Text", validators=[Optional(), validate_option_or_media])
    option_4_media = FileField("Option 4 Media", validators=[Optional()])

    correct_answer = SelectField("Correct Answer", choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], coerce=int)




class QuestionToQuizForm(FlaskForm):
    quiz_title = SelectField("Select Quiz", choices=[], validators=[DataRequired()])  # You should populate this dynamically
    
    question_text = TextAreaField("Question Text", validators=[Optional(), validate_question_or_media])
    question_media = FileField("Question Media", validators=[Optional()])

    option_1 = StringField("Option 1 Text", validators=[Optional(), validate_option_or_media])
    option_1_media = FileField("Option 1 Media", validators=[Optional()])

    option_2 = StringField("Option 2 Text", validators=[Optional(), validate_option_or_media])
    option_2_media = FileField("Option 2 Media", validators=[Optional()])

    option_3 = StringField("Option 3 Text", validators=[Optional(), validate_option_or_media])
    option_3_media = FileField("Option 3 Media", validators=[Optional()])

    option_4 = StringField("Option 4 Text", validators=[Optional(), validate_option_or_media])
    option_4_media = FileField("Option 4 Media", validators=[Optional()])

    correct_answer = SelectField("Correct Answer", choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4")], coerce=int)

 
