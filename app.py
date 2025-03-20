from flask import Flask, render_template, redirect, url_for, jsonify, request, flash
from models import db, User, Event  # models.py에서 모델 가져오기
from forms import EventForm, RegistrationForm, LoginForm, ProfileForm
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import jsonify
import requests

load_dotenv()  # .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '로그인이 필요합니다. 페이지에 접근하려면 로그인하세요.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('이미 사용 중인 이메일입니다. 다른 이메일을 사용하세요.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')  # 해시 메서드 수정
            new_user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('회원가입이 완료되었습니다.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('calendar_view'))
        else:
            flash('유효하지 않은 로그인 정보입니다.', 'danger')
    return render_template('login.html', form=form)

@app.route('/')
def calendar_view():
    return render_template('calendar.html')

@app.route('/api/events')
@login_required
def api_events():
    try:
        events = Event.query.filter_by(user_id=current_user.id).all()
        event_list = [{
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'tags': e.tags,
            'category': e.category,
            'date': e.date.strftime('%Y-%m-%d') 
        } for e in events]
        return jsonify(event_list)
    except Exception as e:
        print(f"가져오는 중 오류 발생: {e}")
        return jsonify({"error": "가져오는 중 오류가 발생했습니다."}), 500


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if request.method == 'POST':
        print(request)
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            user_id=current_user.id,
            tags=form.tags.data,
            category=form.category.data
        )
        db.session.add(new_event)
        db.session.commit()
        flash("일정이 추가되었습니다.", "success")
        return redirect(url_for('calendar_view'))
    else:
        form = EventForm()
        return render_template('event_form.html', title="일정 추가", form=form)

@app.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        flash("권한이 없습니다.", "danger")
        return redirect(url_for('calendar_view'))
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.tags = form.tags.data
        event.category = form.category.data
        db.session.commit()
        flash("일정이 수정되었습니다.", "success")
        return redirect(url_for('calendar_view'))
    return render_template('event_form.html', title="일정 수정", form=form)



@app.route('/update_event/<int:event_id>', methods=['POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        return jsonify({"error": "권한이 없습니다."}), 403

    if not request.is_json:
        return jsonify({"error": "Invalid content type"}), 415

    try:
        data = request.get_json()
        event.title = data.get('title', event.title)
        event.date = datetime.strptime(data.get('date', event.date.strftime('%Y-%m-%d')), '%Y-%m-%d')
        event.description = data.get('description', event.description)
        event.category = data.get('category', event.category)
        db.session.commit()
        return jsonify({"success": "일정이 업데이트되었습니다."})
    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"error": f"서버에서 오류가 발생했습니다: {e}"}), 500
    
@app.route('/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    print(f"현재 사용자 ID: {current_user.id}, 이벤트 소유자 ID: {event.user_id}")
    if event.user_id != current_user.id:
        flash("권한이 없습니다.", "danger")
        return redirect(url_for('calendar_view'))
    try:
        db.session.delete(event)
        db.session.commit()
        flash("삭제되었습니다.", "success")
        return '', 204
    except Exception as e:
        print(f"삭제 중 오류 발생: {e}")
        db.session.rollback()
        return jsonify({"error": "삭제에 실패했습니다."}), 500

@app.route('/search', methods=['GET'])
@login_required
def search_events():
    query = request.args.get('query')
    category = request.args.get('category')
    events = Event.query.filter(Event.user_id == current_user.id)
    if query:
        events = events.filter((Event.title.contains(query)) | (Event.description.contains(query)) | (Event.tags.contains(query)))
    if category:
        events = events.filter_by(category=category)
    event_list = [{
        'id': e.id,
        'title': e.title,
        'start': e.date.strftime('%Y-%m-%d'),
        'description': e.description
    } for e in events]
    return jsonify(event_list)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        if form.password.data and not check_password_hash(current_user.password_hash, form.current_password.data):
            flash('현재 비밀번호가 틀렸습니다.', 'danger')
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.password.data:
                current_user.password_hash = generate_password_hash(form.password.data)
            db.session.commit()
            flash('회원정보가 수정되었습니다.', 'success')
            return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    events = Event.query.filter_by(user_id=user.id).all()
    
    # 사용자가 소유한 모든 이벤트 삭제
    for event in events:
        db.session.delete(event)
    
    logout_user()
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('calendar_view'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 데이터베이스 초기화
    app.run()