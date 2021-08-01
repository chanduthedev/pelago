from pymongo import MongoClient


class DBOperations:
    """
    All DB related operations
    """

    def __init__(self, db_host="localhost", db_port=27017, db_name="pelago", package_tbl="packages", authors_tbl="authors"):
        self.db_client = MongoClient(host=db_host, port=db_port)
        self.db_name = self.db_client[db_name]
        self.packages_table = self.db_name[package_tbl]
        self.authors_table = self.db_name[authors_tbl]

    def create_db(self, db_name):
        self.db_name = self.db_client[db_name]

    def create_packages_table(self, table_name):
        self.packages_table = self.db_name[table_name]

    def get_packages_table(self):
        return self.packages_table

    def delete_packages_table(self):
        if self.packages_table:
            self.packages_table.drop()

    def create_authors_table(self, table_name):
        self.authors_table = self.db_name[table_name]
        print(self.authors_table)

    def get_authors_table(self):
        return self.authors_table

    def delete_authors_table(self):
        if self.authors_table:
            self.authors_table.drop()

    def add_to_packages(self, package_data):
        return self.packages_table.insert_one(package_data)

    def add_to_authors(self, authors_data):
        return self.authors_table.insert_one(authors_data)

    def find_package(self, package_name):
        return self.packages_table.find({"Package": {"$eq": package_name}})

        # reading conf parameters
# app_config = read_conf_file()
# db_host = app_config["db_config"]["db_host"]
# db_port = int(app_config["db_config"]["db_port"])
# db_name = app_config["db_config"]["db_name"]
# db_packages_table = app_config["db_config"]["db_packages_table"]
# db_authors_table = app_config["db_config"]["db_authors_table"]

# db_client = MongoClient(host=db_host, port=db_port)
# print("Connected to DB")

# db = db_client[db_name]
# packages_table = db[db_packages_table]
# print(f"{packages_table}")

# authors_table = db[db_authors_table]
# print(f"{authors_table}")


# def read_package(package_name):
#     try:
#         found_package = packages_table.find({"Package": {"$eq": package_name}})
#         return {
#             "code": 200,
#             "message": "Package details found.",
#             "data": found_package
#         }

#     except Exception as err:
#         return {
#             "code": 50001,
#             "message": str(err)
#         }


# def get_package_details(package_name):
#     """[summary]

#     Returns:
#         [type]: [description]
#     """
#     res = read_package(package_name)
#     if (res['code'] != 50001):
#         found_package_list = db_curser_to_list(res['data'])
#         message = "Package Details found"
#         if not found_package_list:
#             message = "No package details found"

#         return {
#             "code": 200,
#             "message": message,
#             "data": found_package_list
#         }
#     return res
