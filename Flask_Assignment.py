
#1. Create a Flask app that displays "Hello, World!" on the homepage.


from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
    
# 2. Build a Flask app with static HTML pages and navigate between them.

from flask import Flask, render_template

app =Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html') 

if __name__ == '__main__':
    app.run(debug=True, port=5001)
    
# 3. Develop a Flask app that uses URL parameters to display dynamic content.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/user/<username>')
def user_profile(username):
    return render_template('index1.html', username=username)  

if __name__ == '__main__':
    app.run(debug=True)


# 4. Create a Flask app with a form that accepts user input and displays it.

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name  = request.form['username']
        return render_template('index2.html',user_name = name )
    else:
        return render_template('index2.html')
if __name__ =='__main__':
    app.run(debug = True)

# 5. Implement user sessions in a Flask app to store and display user-specific data.

import os
from flask import Flask, session, request, render_template

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/set_data', methods=['POST'])
def set_data():
    username = request.form.get('username')
    favorite_color = request.form.get('favorite_color')
    session['username'] = username
    session['favorite_color'] = favorite_color
    return 'data stored successfully!'

@app.route('/get_data')
def get_data():
    username = session.get('username')
    favorite_color = session.get('favorite_color')
    if username:
        return render_template('index.html', username=username, favorite_color=favorite_color)
    else:
        return 'No user data found!'

if __name__ == "__main__":
    app.run(debug =True)

#6. Build a Flask app that allows users to upload files and display them on the website.



from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index4.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return redirect(request.url)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('index5.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)


# 7. Integrate a SQLite database with Flask to perform CRUD operations on a list of items.





# 8. Implement user authentication and registration in a Flask app using Flask-Login

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
login_manager = LoginManager()
login_manager.init_app(app)

# Mock User Model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Mock User Database
users = {1: {'id': 1, 'username': 'user1', 'password': 'password1'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users.values() if user['username'] == username and user['password'] == password), None)
        if user:
            login_user(User(user['id']))
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return 'Welcome to the Dashboard!'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

# 9. Create a RESTful API using Flask to perform CRUD operations on resources like books or movies

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Book:
    def __init__(self, id, title, author, year):
        self.id = id
        self.title = title
        self.author = author
        self.year = year

books = []  

class BookList(Resource):
    def get(self):
        return books

class BookResource(Resource):
    def get(self, book_id):
        for book in books:
            if book.id == book_id:
                return book
        return {"message": "Book not found"}, 404

    def put(self, book_id):
        data = request.get_json(force=True)  
        updated_book = Book(book_id, data["title"], data["author"], data["year"])
        for i, book in enumerate(books):
            if book.id == book_id:
                books[i] = updated_book
                return updated_book, 200  
        return {"message": "Book not found"},

    def delete(self, book_id):
        for i, book in enumerate(books):
            if book.id == book_id:
                del books[i]
                return {"message": "Book deleted successfully"}, 200
        return {"message": "Book not found"}, 404  # error 

# Register routes
api.add_resource(BookList, "/books")
api.add_resource(BookResource, "/books/<int:book_id>")

if __name__ == "__main__":
    app.run(debug=True)


# 10. Design a Flask app with proper error handling for 404 and 500 errors.

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Flask App!"

@app.route("/<path:path>")
def handle_dynamic_route(path):
    if path == "secret":
        raise Exception("Secret path not allowed")
    return f"Hello from path: {path}"

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    print(f"An error occurred: {error}")
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)

# 11. Create a real-time chat application using Flask-SocketIO.

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
socketio = SocketIO(app)

users = {}  

@app.route('/')
def index():
    return render_template('index8.html')

@socketio.on('connect')
def handle_connect():
    print('User connected')

@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(socketio.sid)  
    if user:
        emit('user_disconnected', user, broadcast=True)  

@socketio.on('send_message')
def handle_send_message(data):
    username = users[socketio.sid]  
    message = data['message']
    emit('incoming_message', {'username': username, 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)


#12. Build a Flask app that updates data in real-time using WebSocket connections.




from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' 
socketio = SocketIO(app)  # Initialize SocketIO with the Flask app instance

data = 0

def update_data():
    global data
    data += 1
    socketio.emit('update_data', data)  
    threading.Timer(1, update_data).start() 

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('update_data', data)
    update_data()  

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)

# 13. Implement notifications in a Flask app using websockets to notify users of updates.

from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
socketio = SocketIO(app)

# User dictionary to store connection IDs (replace with user authentication)
connected_users = {}

def update_data():
  global connected_users
  # Simulate data update (replace with your data fetching logic)
  data = "New update available!"
  for user_id, sid in connected_users.items():
    socketio.emit('notification', data, room=sid)  # Send notification to specific user
  threading.Timer(5, update_data).start()  # Schedule next update in 5 seconds

@app.route('/')
def index():
  return render_template('index9.html')

@socketio.on('connect')
def handle_connect():
  user_id = "user_1"  # Replace with actual user ID from authentication
  sid = socketio.server.environ['sid']
  connected_users[user_id] = sid
  print(f'Client {user_id} connected (sid: {sid})')

@socketio.on('disconnect')
def handle_disconnect():
  user_id = [k for k, v in connected_users.items() if v == socketio.server.environ['sid']][0]
  del connected_users[user_id]
  print(f'Client {user_id} disconnected')

if __name__ == '__main__':
  update_data_thread = threading.Thread(target=update_data)
  update_data_thread.daemon = True
  update_data_thread.start()
  socketio.run(app, debug=True)



