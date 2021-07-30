from flask import Flask, jsonify, request, make_response
app = Flask(__name__)


@app.route('/search', methods=['GET'])
def package_search():
    """
        API to search given package name details from DB.
        Returns: response object with package details if found
    """
    # read package name from query param
    package_name = request.args.get('q')

    return make_response(jsonify({
        'code': 200,
        'message': 'Success',
        "data": {"package_name": package_name}
    }), 200)


@app.errorhandler(400)
def bad_request(error):
    """
        To handle unexpected errors.
    """
    print("in errro")
    return error


server_port = 7788
if __name__ == '__main__':
    app.run(debug=False, port=server_port, host='0.0.0.0')
    print(f'Server started at port:{server_port}')
