from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        'name': 'cosco',
        'items': [
            {
                'name': 'chair',
                'price': 15.99
            },
            {
                'name': 'table',
                'price': 29.99
            },
        ]
    }
]


@app.get('/store')
def get_stores():
    return {'stores': stores}


@app.post('/store')
def create_store():
    store = request.get_json()
    stores.append(store)
    print(stores)

    return store, 201


@app.post('/store/<string:name>/item')
def add_item(name):
    store = [store for store in stores if store['name'] == name]
    if not store:
        return {'response': 'store does not exist'}, 400

    store = store[0]
    item = request.get_json()
    store['items'].append(item)

    return store, 201


if __name__ == '__main__':
    app.run(debug=True)
