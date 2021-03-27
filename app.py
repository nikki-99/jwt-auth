from flask import Flask, jsonify, request, render_template, session, make_response
from functools import wraps
import jwt
import datetime





app = Flask(__name__)


app.config['SECRET_KEY']="hard to guess"


# decorator
def check_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped    
        



@app.route('/')
def index():
    # if not session.get('logged_in'):
    return render_template('login.html')
    # else:
    #     return "Currently Logged In!"    




@app.route('/public')
def public():
    return '<h1>Anyone can see this page</h1>'




@app.route('/auth')
@check_token
def private():
    return "<h1>This is only for those who have valid token</h1>"



@app.route('/login', methods=['POST'])
def login():
    if request.form['name'] and request.form['password']:
        # session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        },
        app.config['SECRET_KEY'])
        return jsonify({'token': token})
    else:    
        return make_response('Unable to verify', 403)

