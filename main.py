import time
import random
from flask import Flask, render_template, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)
app.secret_key = "chaaru"
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])
user_data = {}


@app.route('/')
@limiter.limit("5 per minute")
def home():
    return render_template('home.html')


@app.route('/identity', methods=['GET', 'POST'])
# @limiter.limit("20 per minute")
def identity():
    questions = [
        {"question": "what i said for mocking that pink dress", "id": "0",
         "choices": ["Kari Thuni", "Screen Cloth", "Aragora Dress"], "answer": "Screen Cloth"},
        {"question": "What did i call you when you act egoistically?", "id": "1",
         "choices": ["Ms.Sylvie", "Ms.Boaki", "Ms.Boaki-2"], "answer": "Ms.Boaki-2"},
        {"question": "Where we first met", "id": "2", "choices": ["Keelpak", "Thiruvanmaiyur" "Tanjore"],
         "answer": "Thiruvanmaiyur"},
        {"question": "What was i wearing in our first meet?", "id": "3", "choices": ["White", "Grey", "Black"],
         "answer": "Grey"},
        {"question": "Who is the best actor?", "id": "4", "choices": ["Mahesh Babu", "SRK", "Hrithik"],
         "answer": "Mahesh Babu"},
    ]
    if request.method == 'POST':
        ip = request.remote_addr
        answer = request.form.to_dict()
        idx, ans = list(answer.items())[0]
        if questions[int(idx)]['answer'] == ans:
            user_data[ip] = time.time()
            return redirect(url_for('message'))
        else:
            return render_template('identity2.html', question=random.choice(questions),
                        error="Sherlock holmes nu sona matum pathathu answer um crct ah kandu pudikanum")

    return render_template('identity2.html', question=random.choice(questions))


@app.route('/message')
@limiter.limit("5 per minute")
def message():
    ip = request.remote_addr
    if ip not in user_data:
        return redirect(url_for('identity'))
    else:
        if abs(time.time() - user_data[ip]) <= 120:
            return render_template('message.html')
        else:
            del user_data[ip]
            return redirect(url_for('identity'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=False)