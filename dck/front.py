from flask import Flask, request

app = Flask(__name__)


@app.route('/ppxd', methods=['POST'])
def hello_world():
    postdata = request.form['downloadurl']
    print(postdata)
    print('-'*20)
    return 'Hello, World!'


# if __name__ == "__main__":
#     app.run("127.0.0.1", 8888,debug=True)
