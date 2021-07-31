import utils
import os
separator = os.path.sep


def main():
    package_details = utils.get_package_list(
        "http://cran.r-project.org/src/contrib/PACKAGES")
    # print(package_details)
    counter = 5
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
            print(final_pack_details)
        else:
            print(f"{pack_name} {pack_version} {download_resp['message']}")


if __name__ == "__main__":
    main()
