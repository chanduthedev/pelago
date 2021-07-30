from flask import Flask, jsonify, request, make_response
from utils import read_conf_file
app = Flask(__name__)

# reading conf parameters
app_config = read_conf_file()

# sections will be empty if invalid file path or file content is not
# standard format
if not app_config.sections():
    print("[ERROR] Please re-validate config file for server and DB configuration")
    exit(1)

server_host = app_config["server_config"]["server_host"]
server_port = int(app_config["server_config"]["server_port"])

db_host = app_config["db_config"]["db_host"]
db_port = int(app_config["db_config"]["db_port"])
db_name = app_config["db_config"]["db_name"]
db_packages_table = app_config["db_config"]["db_packages_table"]
db_authors_table = app_config["db_config"]["db_authors_table"]


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


if __name__ == '__main__':
    app.run(debug=False, port=server_port, host=server_host)
    print(f'Server started at port:{server_port}')
