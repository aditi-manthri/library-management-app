from typing import Any
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,unset_jwt_cookies
from flask_cors import CORS
from datetime import datetime
from flask_restful import Resource,Api
from flask_caching import Cache
from sqlalchemy import or_, and_,func
from sqlalchemy.orm import joinedload
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import io
from flask import send_file


app = Flask(__name__)
CORS(app,origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['JWT_SECRET_KEY'] = 'GROCERY'
db = SQLAlchemy(app)
jwt = JWTManager(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(256), nullable=False)
    last_login = db.Column(db.DateTime)

class Sections(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    description = db.Column(db.String(256))

class Book(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(256))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    description = db.Column(db.String(256))
    section = db.Column(db.String(256))
    pdf = db.Column(db.String(512))

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requested_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_book = db.Column(db.Integer, db.ForeignKey('book.id'))
    user = db.Column(db.String(256))
    book = db.Column(db.String(256))
    approved = db.Column(db.Boolean)

class Issued(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    issued_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    issued_book = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_issued = db.Column(db.DateTime)
    date_returned = db.Column(db.DateTime)
    book = db.Column(db.String(256))
    author = db.Column(db.String(256))
    description = db.Column(db.String(256))
    pdf = db.Column(db.String(512))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issued.id'))
    feedback = db.Column(db.String(256))    
    
class Read(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())

with app.app_context():
    db.create_all()
    admin_username = 'admin'
    admin_password = 'admin'

    if not User.query.filter_by(username=admin_username).first():
        hashed_password = generate_password_hash(admin_password, method='pbkdf2:sha256')
        admin_user = User(username=admin_username, password=hashed_password,role='admin', email='admin@readr.com')
        db.session.add(admin_user)
        db.session.commit()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/books/search', methods=['GET'])
def search_books():
    query = request.args.get('query')
    results = Book.query.filter(
        db.or_(
            Book.title.contains(query),
            Book.author.contains(query),
            Book.section.contains(query)
        )
    ).all()
    return jsonify([book.serialize() for book in results])

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role')
        
        if User.query.filter_by(username=username).first():
            return {'error':'Username already exists'}, 400
        
        hashed = generate_password_hash(password,method='pbkdf2:sha256')
        if role == 'user':
            new_user = User(username=username,password=hashed,role='user', email=email)

        db.session.add(new_user)
        db.session.commit()

        return {'message':'Signup Successful'}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            user.last_login = datetime.now()
            db.session.commit()

            access_token = create_access_token(identity={
                'username':user.username
            })

            return {'message':'Login Successful','access_token':access_token,'userRole':user.role,'user_id': user.id}, 200
        else:
            return {'error':'Invalid Username or Password'}, 401

class SectionResource(Resource):
    @jwt_required()
    def get(self,section_id=None):
        if section_id is None:
            sections = Sections.query.all()
            section_list = [{'id':section.id,'name':section.name, 'description': section.description} for section in sections]

            return jsonify(section_list)
        else:
            section = Sections.query.get(section_id)
            if section:
                return {'id':section.id,'name':section.name}
            else:
                return {'error':'Section not found'}, 400
            
    def post(self):
        data = request.get_json()
        section_name = data.get('name')
        section_description = data.get('description')

        if not section_name:
            return {'error':'Section name is required'}, 400
        existing_section = Sections.query.filter(and_(db.func.lower(Sections.name)==section_name)).first()
        if existing_section:
            return {'error':'Section already exists'} , 400

        new_section = Sections(name = section_name, description = section_description)

        db.session.add(new_section)
        db.session.commit()

        return {'message':'Section created succesfully'}, 201
    
    def put(self,section_id):
        if not section_id:
            return {'error':'Section ID is required'} , 400
        section = Sections.query.get(section_id)

        if not section:
            return {'error':'Section not found'},400
        data = request.get_json()
        new_section_name = data.get('name')
        section.name = new_section_name
        new_description = data.get('description')
        section.description = new_description
        db.session.commit()

    def delete(self,section_id):
        if not section_id:
            return {'error':'Section ID is required'},400
        
        section = Sections.query.get(section_id)
        if not section:
            return {'error':'Section not found'},400
        db.session.delete(section)
        db.session.commit()

        return {'message':'Section deleted succesfully'},200

class BookResource(Resource):
    def get(self,section_id=None):
        if section_id is None:
            books = Book.query.all()
        else:    
            books = Book.query.filter_by(section_id=section_id).all()
        book_list = [{'id':book.id,'name':book.name,'author':book.author,'section': book.section, 'description':book.description,'pdf':book.pdf} for book in books]
        return jsonify(book_list)
    
    def post(self, section_id):
        data = request.get_json()
        book_name = data.get('name')
        author_name = data.get('author')
        section = Sections.query.get(section_id) 
        section_name = section.name
        description = data.get('description')
        pdf = data.get('pdf')

        if not book_name:
            return {'error':'Book name is required'}, 400
        existing_section = Sections.query.filter(and_(db.func.lower(Sections.name)==book_name)).first()
        if existing_section:
            return {'error':'Book already exists'} , 400

        new_book = Book(name = book_name, author = author_name, section_id = section_id, section = section_name, description = description, pdf = pdf)
        db.session.add(new_book)
        db.session.commit()

        return {'message':'Book created succesfully'}, 201        
    
    def put(self,book_id):
        if not book_id:
            return {'error':'Book ID is required'} , 400
        book = Book.query.get(book_id)

        if not book:
            return {'error':'Book not found'},400
        data = request.get_json()
        new_book_name = data.get('name')
        book.name = new_book_name
        new_author = data.get('author')
        book.author = new_author
        new_description = data.get('description')
        book.description = new_description  
        new_pdf = data.get('pdf')
        book.pdf = new_pdf
        book.section_id = data.get('section_id', book.section_id)
        db.session.commit()

        return {'message': 'Book updated successfully'}, 200
    
    def delete(self,book_id):
        if not book_id:
            return {'error':'Book ID is required'},400
        
        book = Book.query.get(book_id)
        if not book:
            return {'error':'Book not found'},400
        db.session.delete(book)
        db.session.commit()

        return {'message':'Book deleted succesfully'},200

class SearchResource(Resource):
    @jwt_required()
    def post(self):
        search_query = request.json.get('search_query')

        books = Book.query.join(Sections).filter(
            or_(
                Book.name.ilike(f'%{search_query}%'),
                Book.section.ilike(f'%{search_query}%'),
                Book.author.ilike(f'%{search_query}%')
            )
        ).all()

        book_list = [
        {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'section': book.section,
        }
        for book in books
    ]

        return jsonify(book_list)

class UserRequestResource(Resource):
    def get(self):
        requests = Requests.query.all()
        return [{'id': req.id, 'requested_user': req.requested_user, 'requested_book': req.requested_book, 'approved': req.approved} for req in requests]
    
    def post(self, user_id):
        data = request.get_json()
        requested_book = data['book_id']
        requested_user = data['user_id']

        num_requests = Requests.query.filter_by(requested_user=requested_user).count()
        if num_requests >= 5:
            return {'error': 'You can only have 5 requests at once.'}, 400

        existing_request = Requests.query.filter_by(requested_user=requested_user, requested_book=requested_book).first()
        if existing_request:
            return {'message': 'A request for this book by this user already exists'}, 400
        new_request = Requests(requested_user=requested_user, requested_book=requested_book, approved=False, user=User.query.get(requested_user).username, book=Book.query.get(requested_book).name)
        db.session.add(new_request)
        db.session.commit()
        return {'message': 'Request created successfully'}, 201

class AdminRequestResource(Resource):
    def get(self):
        requests = Requests.query.all()
        book_list = [{'id':request.id,'requested_user':request.requested_user,'requested_book':request.requested_book,'approved': request.approved, 'user': request.user, 'book': request.book} for request in requests]
        return jsonify(book_list)
    
    def post(self, request_id):
        data = request.get_json()
        new_approved = data['approved']
        request_obj = Requests.query.get(request_id)
        if not request:
            return {'message': 'Request not found'}, 404

        request_obj.approved = new_approved
        db.session.commit()

        if new_approved:
            issued = Issued.query.filter_by(issued_user=request_obj.requested_user, issued_book=request_obj.requested_book).first()
            if not issued:
                date_issued = datetime.now()
                date_returned = date_issued + timedelta(days=7)
                issued = Issued(request_id=request_obj.id, issued_user=request_obj.requested_user, issued_book=request_obj.requested_book, date_issued=date_issued, date_returned=date_returned, book=Book.query.get(request_obj.requested_book).name, author=Book.query.get(request_obj.requested_book).author, description=Book.query.get(request_obj.requested_book).description, pdf=Book.query.get(request_obj.requested_book).pdf)
                read = Read(book_id=request_obj.requested_book, user_id=request_obj.requested_user, timestamp=date_returned)
                db.session.add(read)
                db.session.add(issued)

        else:
            issued = Issued.query.filter_by(issued_user=request_obj.requested_user, issued_book=request_obj.requested_book).first()
            if issued:
                db.session.delete(issued)    
        db.session.commit()

        return {'message': 'Request updated successfully'}, 200
    
    def delete(self, request_id):
        issued = Issued.query.filter_by(request_id=request_id).first()
        if issued:
            db.session.delete(issued)
        request = Requests.query.get(request_id)
        if not request:
            return {'error':'Request not found'},400
        db.session.delete(request)
        db.session.commit()

        return {'message':'Request deleted succesfully'},200
        
class IssuedResource(Resource):
    def get(self, user_id):
        if user_id is None:
            issued = Issued.query.all()
        else:
            issued = Issued.query.filter_by(issued_user=user_id).all()
        issued_list = [{'id':issue.id,'request_id': issue.request_id, 'issued_user':issue.issued_user,'issued_book':issue.issued_book,'date_issued':issue.date_issued,'date_returned':issue.date_returned, 'book':issue.book, 'author': issue.author, 'description':issue.description, 'pdf': issue.pdf} for issue in issued]
        return jsonify(issued_list)
    
    def post(self, issued_id):
        issued = Issued.query.get(issued_id)

        if not issued:
            return {'message': 'Issued item not found'}, 404
        
        issued.date_returned = issued.date_issued + timedelta(days=7)
        db.session.commit()

        return {'message': 'Return date updated successfully'}, 200
    
    def delete(self, issued_id):
        issued = Issued.query.get(issued_id)
        requested = Requests.query.get(issued.request_id)
        if not issued:
            return {'error':'Issue not found'},400
        db.session.delete(issued)
        db.session.delete(requested)
        db.session.commit()

        return {'message':'Issue deleted succesfully'},200

class FeedbackResource(Resource):
    def post(self):
        issue_id = request.json.get('issue_id')
        feedback_text = request.json.get('feedback')
        issue = Issued.query.get(issue_id)
        feedback = Feedback(user_id=issue.issued_user, book_id=issue.issued_book, issue_id = issue_id, feedback=feedback_text)
        db.session.add(feedback)
        db.session.commit()

        return {'message': 'Feedback submitted successfully'}, 201
        
    def get(self):
        feedbacks = Feedback.query.all()
        feedback_list = [{'id': feedback.id, 'user_id': feedback.user_id, 'book_id': feedback.book_id, 'issue_id': feedback.issue_id, 'feedback': feedback.feedback} for feedback in feedbacks]
        return jsonify(feedback_list)

class AdminStatsPieResource(Resource):
    def get(self):
        sections = db.session.query(Book.section, db.func.count(Book.id)).group_by(Book.section).all()
        section_names = [section[0] for section in sections]
        section_counts = [section[1] for section in sections]

        plt.figure(figsize=(10, 5))
        plt.pie(section_counts, labels=section_names, autopct='%1.1f%%')
        centre_circle = plt.Circle((0, 0), 0.75, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title('Section Division')

        img1 = io.BytesIO()
        plt.savefig(img1, format='png')
        plt.close()
        img1.seek(0)

        return send_file(img1, mimetype='image1/png')
    
class AdminStatsBarResource(Resource):
    def get(self):
        users = db.session.query(User.username, db.func.count(Issued.issued_book)).join(Issued, User.id == Issued.issued_user).group_by(User.username).all()
        usernames = [user[0] for user in users]
        book_counts = [user[1] for user in users]

        plt.figure(figsize=(10, 5))
        plt.bar(usernames, book_counts)
        plt.xlabel('Username')
        plt.ylabel('Number of Books Issued')
        plt.title('Books Issued')

        img2 = io.BytesIO()
        plt.savefig(img2, format='png')
        plt.close()
        img2.seek(0)

        return send_file(img2, mimetype='image2/png')   
            
api.add_resource(SignupResource,'/signup')
api.add_resource(LoginResource,'/login')
api.add_resource(SectionResource,'/sections','/sections/<int:section_id>')
api.add_resource(BookResource,'/books','/books/<int:section_id>', '/books/edit/<int:book_id>')
api.add_resource(SearchResource,'/search')
api.add_resource(UserRequestResource, '/users/<int:user_id>/requests')
api.add_resource(AdminRequestResource, '/admin/requests','/admin/requests/<int:request_id>' )
api.add_resource(IssuedResource, '/issued/user/<int:user_id>','/issued/<int:issued_id>')
api.add_resource(FeedbackResource, '/feedback')
api.add_resource(AdminStatsPieResource, '/adminstats/pie')
api.add_resource(AdminStatsBarResource, '/adminstats/bar')

@app.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    resp = jsonify({'message':'Logged out successfully'})
    unset_jwt_cookies(resp)
    return resp,200

if __name__ == '__main__':
    app.run(port=8000, debug=True)