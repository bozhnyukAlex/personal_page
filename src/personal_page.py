from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')


@app.route("/")
def main_page():
    return render_template('index.html')


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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
