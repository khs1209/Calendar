from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField ,TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[Length(min=6, max=20)])
    confirm_password = PasswordField('비밀번호 확인', validators=[Length(min=6, max=20), EqualTo('password')])
    submit = SubmitField('회원가입')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('이미 사용 중인 사용자 이름입니다.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('이미 사용 중인 이메일입니다.')

class LoginForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired()])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    password = PasswordField('비밀번호', validators=[Length(min=6, max=20)])
    submit = SubmitField('로그인')

class EventForm(FlaskForm):
    title = StringField('일정', validators=[DataRequired()])
    description = TextAreaField('설명')
    date = DateField('날짜', format='%Y-%m-%d', validators=[DataRequired()]) 
    tags = StringField('태그')  # 태그
    category = StringField('카테고리')  # 카테고리
    submit = SubmitField('추가')

class ProfileForm(FlaskForm):
    username = StringField('아이디', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('이메일', validators=[DataRequired(), Email()])
    current_password = PasswordField('현재 비밀번호', validators=[Length(min=6, max=20)])
    password = PasswordField('새 비밀번호', validators=[Length(min=6, max=20)])
    confirm_password = PasswordField('새 비밀번호 확인', validators=[EqualTo('password')])
    submit = SubmitField('수정')