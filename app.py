from flask import Flask, jsonify, request, Response
import json, jwt, datetime
from bookModel import *
from userModel import *
from settings import *
from functools import wraps


@app.route('/login', methods=['POST'])
def get_token():
    request_data = request.get_json()
    username = str(request_data['username'])
    password = str(request_data['password'])
    match = User.username_password_match(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response('', 401, mimetype='application/json')


def validBookObject(bookObject):
    '''
    validates book objects passed in
    :param bookObject:
    :return: Whether the bookObject is valid or not
    '''
    if ('name' in bookObject and
            'price' in bookObject and
            'isbn' in bookObject):
        return True
    else:
        return False


@app.route('/books', methods=['POST'])
@token_required
def add_book():
    '''

    :return:
    '''
    request_data = request.get_json()
    if (validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(request_data['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            'error': 'Invalid book object passed in request',
            'helpString': "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 'isbn number'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='appliation/json')
        return response


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a Valid Token To View This Page'}), 401
    return wrapper


@app.route('/books')
@token_required
def get_books():
    return jsonify({'books': Book.get_all_books()})


@app.route('/books/<int:isbn>')
@token_required
def get_book_by_isbn(isbn):
    return jsonify(Book.get_book(isbn))


@app.route('/books/<int:isbn>', methods=['PUT'])
@token_required
def replace_book(isbn):
    request_data = request.get_json(force=True)
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response('', status=204)
    return response


@app.route('/update/<int:isbn>', methods=['PATCH'])
@token_required
def update_book(isbn):
    request_data = request.get_json(force=True)
    updated_book = {}
    if ('name' in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if ('price' in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response('', status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


@app.route('/delete/<int:isbn>', methods=['DELETE'])
@token_required
def delete_book(isbn):
    if (Book.delete_book(isbn)):
        response = Response('', status=204)
        return response

    invalidBookObjectErrorMsg = {
        'error': 'Invalid book object passed in request',
        'helpString': "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 'isbn number'}"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='appliation/json')
    return response


app.run(debug=True, port=5000)
