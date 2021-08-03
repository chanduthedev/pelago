import utils
import os
from db_operations import DBOperations
separator = os.path.sep


db_instance = DBOperations('localhost', 27017)


def main():
    response = utils.get_package_list(
        "http://cran.r-project.org/src/contrib/PACKAGES")
    # deleting existing tables to avoid duplicates
    db_instance.delete_packages_table()
    db_instance.delete_authors_table()

    # Creating new tables.
    db_instance.create_packages_table
    db_instance.create_authors_table
    if response['code'] != 200:
        print(response['message'])
        exit()
    package_details = response['data']
    # print(package_details)
    # Processing 100 packages for now.
    counter = 100
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
                inserted_author = db_instance.add_to_authors(
                    {"Name": maintainer.split('<')[0], "Email": maintainer.split('<')[1][:-1]})
                print(
                    f"Inserted Name and email, generated id: {inserted_author.inserted_id}")
            inserted_package = db_instance.add_to_packages(final_pack_details)
            print(
                f"Inserted package details, generated id: {inserted_package.inserted_id}")
        else:
            print(f"{pack_name} {pack_version} {download_resp['message']}")


if __name__ == "__main__":
    main()
