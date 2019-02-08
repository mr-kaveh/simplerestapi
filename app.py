from flask import Flask, jsonify, request, Response
import json
from bookModel import *
from settings import *


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
def add_book():
    '''

    :return:
    '''
    request_data = request.get_json()
    if (validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            'error': 'Invalid book object passed in request',
            'helpString': "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 'isbn number'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='appliation/json')
        return response


@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return jsonify(Book.get_book(isbn))


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json(force=True)
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response('', status=204)
    return response


@app.route('/update/<int:isbn>', methods=['PATCH'])
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
