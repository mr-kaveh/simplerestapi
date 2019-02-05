from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'name': 'Cooking Book',
        'price': 7.99,
        'isbn': 998656565232
    },
    {
        'name': 'Jonge Hafteh',
        'price': 8.99,
        'isbn': 99844878545454
    }
]


@app.route('/')
def hello_world():
    '''

    :return: A Hello World message
    '''
    return 'Hello World!'


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
    if(validBookObject(request_data)):
        new_book = {
                'name': request_data['name'],
                'price': request_data['price'],
                'isbn': request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books/' + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            'error': 'Invalid book object passed in request',
            'helpString': "Data passed in similar to this {'name': 'bookname', 'price': 7.99, 'isbn': 'isbn number'}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg) , status=400, mimetype='appliation/json')
        return response


@app.route('/books')
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    for book in books:
        if book['isbn'] == isbn:
            value = {
                'name': book['name'],
                'price': book['price'],
            }
    return jsonify(value)

@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    return jsonify(request.get_json())


app.run(debug=True, port=5000)
