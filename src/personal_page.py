from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '3dcbeaea0404d5af70affaf4fb13d917e7fcfc71'


@app.route("/")
def index_page():
    user_id = session.get('user_id')
    if user_id is None:
        return render_template("index_login.html")
    user = Users.query.filter_by(id=user_id).first()
    return render_template("index_logout.html", name=user.name)


@app.route("/portfolio-details-battleship.html")
def details_battleship():
    return render_template('portfolio-details-battleship.html')


@app.route("/portfolio-details-botanica.html")
def details_botanica():
    return render_template('portfolio-details-botanica.html')


@app.route("/portfolio-details-dvfs.html")
def details_dvfs():
    return render_template('portfolio-details-dvfs.html')


@app.route("/portfolio-details-java.html")
def details_java():
    return render_template('portfolio-details-java.html')


@app.route("/logout_sure")
def logout_sure():
    return render_template('index_sure.html')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vk_id = db.Column(db.String(255), unique=True, nullable=True)
    vk_access_token = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<users self.name>'


@app.route("/logout")
def logout():
    if not session.get('user_id'):
        return redirect(url_for('index_page'))
    session.pop('user_id', None)
    return redirect(url_for('index_page'))


@app.route("/vk_login")
def vk_login():
    user_code = request.args.get('code')

    if not user_code:
        return redirect(url_for('index_page'))

    response = requests.get("https://oauth.vk.com/access_token?client_id=7811259&client_secret=R5KWO3NYTbNgCXu2Pwzf&redirect_uri=http://178.154.213.152/vk_login&code=" + user_code)
    access_token_json = json.loads(response.text)
    if "error" in access_token_json:
        return redirect(url_for('index_page'))

    vk_id = access_token_json['user_id']
    access_token = access_token_json['access_token']

    response = requests.get("https://api.vk.com/method/users.get?user_ids=" + str(vk_id) + "&fields=bdate&access_token=" + str(access_token) + "&v=5.130")
    vk_user = json.loads(response.text)

    print(vk_user)

    user = Users.query.filter_by(vk_id=vk_id).first()
    if user is None:
        name = vk_user['response'][0]['first_name'] + " " + vk_user['response'][0]['last_name']
        new_user = Users(name=name, vk_id=vk_id, vk_access_token=access_token)
        try:
            db.session.add(new_user)
            db.session.commit()

        except SQLAlchemyError as err:
            db.session.rollback()
            error = str(err.dict['orig'])

            print(f"ERROR adding user to DB: {error}")

            return redirect(url_for('index_page'))

        user = Users.query.filter_by(vk_id=vk_id).first()

    session['user_id'] = user.id
    return redirect(url_for('index_page'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
