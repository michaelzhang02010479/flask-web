import stripe
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import uuid

# 通过 static_folder 指定静态资源路径，以便 index.html 能正确访问 CSS 等静态资源
# template_folder 指定模板路径，以便 render_template 能正确渲染 index.html

# 本地静态文件放置目录
FRONTEND_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')

APP = Flask(
    __name__, static_folder=os.path.join(FRONTEND_FOLDER, "static"), template_folder=FRONTEND_FOLDER)

CORS(APP)


BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True,
        'price': '19.99'

    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False,
        'price': '9.99'
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True,
        'price': '9.99'
    }
]


@APP.route("/")
def home():
    '''
        当在浏览器访问网址时，通过 render_template 方法渲染 dist 文件夹中的 index.html。
        页面之间的跳转交给前端路由负责，后端不用再写大量的路由
    '''
    return render_template('index.html')


@APP.route('/test', methods=['GET', 'POST'])
def test():
    ''' 这个API用来测试跨域 '''
    return 'success'


@APP.route('/ping', methods=['GET'])
def ping():
    return jsonify('fromflask')


@APP.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'succes'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)

@APP.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == "GET":
        return_book = ''
        for book in BOOKS:
            if book['id'] == book_id:
                return_book = book
        response_object['book'] = return_book

    if request.method == "PUT":
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'

    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)

def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

@app.route('/charge', methods=['POST'])
def create_charge():
    post_data = request.get_json()
    amount - round(fload(post_data.get('book')['price']) * 100)
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    charge = stripe.Charge.create(
        amount = amount,
        currency = 'usd',
        card = post_data.get('token')
        description = post_data.get('book')['title']
    )
    response_object = {
        'status': 'success',
        'charge': charge
    }
    return jsonify(response_object), 200

@app.route('/charge/<charge_id>')
def get_charge(charge_id):
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    response_object = {
        'status': 'success',
        'charge': stripe.Charge.retrieve(charge_id)
    }
    return jsonify(respone_object), 200
    

if __name__ == '__main__':
    # 开启 debug模式，这样我们就不用每更改一次文件，就重新启动一次服务
    # 设置 host='0.0.0.0'，让操作系统监听所有公网 IP
    # 也就是把自己的电脑作为服务器，可以让别人访问
    APP.run(debug=True, host='0.0.0.0')