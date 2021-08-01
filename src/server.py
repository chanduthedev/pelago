from flask import Flask, jsonify, request, make_response
from utils import read_conf_file, find_package
app = Flask(__name__)

# reading conf parameters
app_config = read_conf_file()

# sections will be empty if invalid file path or
# file content is not in standard format
if not app_config.sections():
    print("[ERROR] Please re-validate config file for server and DB configuration")
    exit(1)

server_host = app_config["server_config"]["server_host"]
server_port = int(app_config["server_config"]["server_port"])


@app.route('/search', methods=['GET'])
def package_search():
    """
        API to search given package name details from DB.
        Returns: response object with package details if found
    """
    try:
        # read package name from query param
        package_name = request.args.get('q')

        # returnint error message for empty package name
        if not package_name:
            print("# returnint error message for empty package name")
            return make_response(jsonify({
                'code': 40005,
                'message': 'Package name cannot be empty'
            }), 200)

        print(f"In search api, package_name:{package_name}")
        #  Searching for package in DB
        # found_package = packages_table.find({"Package": {"$eq": package_name}})
        # found_package_list = db_curser_to_list(found_package)
        res_data = find_package(package_name)
        return make_response(res_data, 200)
    except Exception as err:
        return make_response(jsonify({
            'code': 40006,
            'message': str(err)
        }), 200)


@app.errorhandler(400)
def bad_request(error):
    """
        To handle unexpected errors.
    """
    print("In error handler funciton")
    return error


if __name__ == '__main__':
    app.run(debug=False, port=server_port, host=server_host)
    print(f'Server started at port:{server_port}')
