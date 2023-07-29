from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        'name': 'my store',
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


if __name__ == '__main__':
    app.run(debug=True)
