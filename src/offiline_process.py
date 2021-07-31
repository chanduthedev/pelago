from pymongo import MongoClient
import utils
import os
separator = os.path.sep


db_client = MongoClient(host="localhost", port=27017)
print("Connected to DB")

db = db_client['pelago']
packages_table = db['packages']
print("Deleting existing packages collection if any in DB")
packages_table.drop()
packages_table = db['packages']
print(f"{packages_table}")

authors_table = db['authors']
print("Deleting existing authors collection if any in DB")
authors_table.drop()
authors_table = db['authors']
print(f"{authors_table}")


def main():
    response = utils.get_package_list(
        "http://cran.r-project.org/src/contrib/PACKAGES")
    if response['code'] != 200:
        print(response['message'])
        exit()
    package_details = response['data']
    # print(package_details)
    counter = 50
    for pack_name, pack_version in package_details.items():
        print(f"Processing {pack_name}_{pack_version}")
        if not counter:
            break
        counter -= 1
        download_resp = utils.download_and_extract_tarfile(
            pack_name, pack_version)
        if download_resp['code'] == 200:
            package_path = utils.get_root_folder()+separator+"../packages"
            json_data = utils.read_package_description(package_path, pack_name)
            final_pack_details = {
                "Package": pack_name, "Version": pack_version}
            data = json_data['data']
            final_pack_details['Date/Publication'] = data.get(
                'Date/Publication', 'NA')
            final_pack_details['Title'] = data.get('Title', 'NA')
            final_pack_details['Description'] = data.get('Description', 'NA')
            final_pack_details['Author'] = data.get('Author', 'NA')
            maintainer = data.get('Maintainer', 'NA')
            final_pack_details['Maintainer'] = maintainer
            if len(maintainer.split('<')) == 2:
                final_pack_details['Name'] = maintainer.split('<')[0].strip()
                final_pack_details['Email'] = maintainer.split('<')[1][:-1]
                inserted_author = authors_table.insert_one(
                    {"Name": maintainer.split('<')[0], "Email": maintainer.split('<')[1][:-1]})
                print(
                    f"Inserted Name and email, generated id: {inserted_author.inserted_id}")
            inserted_package = packages_table.insert_one(final_pack_details)
            print(
                f"Inserted package details, generated id: {inserted_package.inserted_id}")
        else:
            print(f"{pack_name} {pack_version} {download_resp['message']}")


if __name__ == "__main__":
    main()
