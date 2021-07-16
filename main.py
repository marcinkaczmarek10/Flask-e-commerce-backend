from src import create_app

app = create_app()

@app.route('/')
def home():
    return '"<p>Hello World</p>'



if __name__ == '__main__':
    app.run()