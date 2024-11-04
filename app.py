from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

# App configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model definition
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # Stores IP address

# Create the database and the comment table
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        new_comment = request.form['comment']
        commenter_ip = request.remote_addr  # Get the commenter's IP address
        comment = Comment(content=new_comment, ip_address=commenter_ip)
        db.session.add(comment)
        db.session.commit()
    comments = Comment.query.all()  # Retrieve all comments from the database
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(host='192.168.0.2', port=8000)
