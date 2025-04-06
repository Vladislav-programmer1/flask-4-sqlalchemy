from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager, login_required, logout_user

# from api.jobs_api import jobs_bp
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.make_job_form import MakeJobForm

from sqlalchemy import select, func

app = Flask(__name__)
# app.register_blueprint(jobs_bp, url_prefix="/api")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    query = session.query(Jobs)
    jobs = []

    for job in query:
        team_leader_id = job.team_leader
        team_leader = session.query(User.name).filter(User.id == team_leader_id).first()[0]
        some_job = [job.job, team_leader, job.work_size, job.collaborators, job.is_finished]
        jobs.append(some_job)

    return render_template("actions.html", jobs=jobs)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
        return redirect("/")
    return render_template("login.html", title="Authorisation", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.password.data != form.repeat_password.data:
        return render_template("register.html", title="Регистрация",
                               message="Пароли не совпадают", form=form)

    session = db_session.create_session()
    if form.validate_on_submit():
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", title="Регистрация",
                               message="Такой пользователь уже существует", form=form)

        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()

        login_user(user)
        return redirect("/")
    return render_template("register.html", title="Registration", form=form)


@app.route("/addjob", methods=["POST", "GET"])
def add_job():
    form = MakeJobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        leader = session.query(User.id).filter(User.id == form.team_leader_id.data)
        if not list(leader):
            return render_template("make_job_form.html", title="Добавление работы",
                                   messsage="Не существует пользователя с таким id", form=form)

        collaborators = list(map(int, form.collaborators.data.split(", ")))
        if len(list(session.query(User.id).filter(User.id.in_(collaborators)))) != len(collaborators):
            return render_template("make_job_form.html", title="Добавление работы",
                                   messsage="Не существует пользователей с таким id", form=form)

        job = Jobs(
            job=form.title.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            team_leader=form.team_leader_id.data,
        )
        session.add(job)
        session.commit()

        return redirect("/")
    return render_template("make_job_form.html", title="Добавление работы", form=form)


def main():
    db_session.global_init("db/mars.db")
    app.run(host="127.0.0.1", port=8080)


if __name__ == '__main__':
    main()