from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    steps = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id

def extract_numbers(steps):
    numbers = re.findall(r'\d+',steps)
    numbers = [int(num) for num in numbers]
    return numbers


@app.route('/total_sum')
def calculate_total_sum():
    total_sum = 0
    articles = Article.query.all()
    for article in articles:
        if isinstance(article.steps, str):
            numbers = [int(num) for num in re.findall(r'\d+', article.steps)]
            total_sum += sum(numbers)
    return render_template('total_sum.html', total_sum=total_sum)


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/create-article', methods = ['POST', 'GET'])
def create_articel():
    if request.method == 'POST':
        steps = request.form['steps']
        text = request.form['text']
        article = Article(steps =steps, text = text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "ОШИБКА"
    else:
        return render_template("create-article.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
