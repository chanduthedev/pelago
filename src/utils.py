import configparser
import urllib.request
import tarfile
import ssl
import os
import requests
separator = os.path.sep

# temporary fix to access as a un-verified user
ssl._create_default_https_context = ssl._create_unverified_context


def get_root_folder():
    return os.path.dirname(os.path.abspath(__file__))


def read_conf_file():
    config_file = 'config.cfg'
    # load all input params from config file
    config = configparser.ConfigParser()

    # reading config file
    config.read(config_file)

    return config


def get_package_list(package_url):
    """Get all package details from the given url

    Args:
        package_url (str): URL of the package list to download

    Returns:
        [type]: [description]
    """
    try:
        print(f"In get_package_list, url:{package_url}")
        resp = requests.get(package_url)
        all_pack_details = str(resp.content).split('\\n\\n')
        all_pack_details_list = [str(each_pack).split('\\n')
                                 for each_pack in all_pack_details]
        packages = {}
        for pack_list in all_pack_details_list:
            pack_name = pack_list[0].split(":")[1].strip()
            pack_version = pack_list[1].split(":")[1].strip()
            packages[pack_name] = pack_version

        return {"code": 200, "message": "Success", "data": packages}
    except Exception as err:
        return {"code": 40004, "message": str(err)}


def download_and_extract_tarfile(package_name, package_version):
    """
    Downloading the given package version and uncompress it in the local folder

    Args:
        package_name (str): Package name
        package_version (str): Package version

    Returns:
        [dict]: JSON response with code and message
    """
    try:
        tarfile_url = "https://cran.r-project.org/src/contrib/{0}_{1}{2}".format(
            package_name, package_version, ".tar.gz")
        ftp_stream = urllib.request.urlopen(tarfile_url)
        tar_file = tarfile.open(fileobj=ftp_stream, mode="r|gz")
        downloading_path = get_root_folder()+separator+"../packages"
        tar_file.extractall(downloading_path)

        if os.path.exists(downloading_path+separator+package_name):
            print(f"{package_name} package downloaded and uncomressed successfully")
            return {"code": 200,
                    "message": "Package downloaded and uncomressed successfully"}
        else:
            return {"code": 40001,
                    "message": "Package downloading failed"}

    except Exception as err:
        print(
            f"In download_and_extract_tarfile, {package_name} got exception :{str(err)}")
        return {"code": 40002, "message": str(err)}


def read_package_description(package_path, package_name):
    """
    Read package description from the package folder
    and form the data into json object to insert into database

    Args:
        package_path (str): Package path file location
        package_name (str): Package name

    Returns:
        [dict]: [json response with code, message and data if available]
    """
    print(
        f"In read_package_description package_path:{package_path} package_name:{package_name}")
    package_datails = {}
    pack_desc_file = package_path+separator+package_name+"/DESCRIPTION"
    try:
        with open(pack_desc_file, "r") as inputfile:

            for each_line in inputfile:
                split_line_list = each_line.split(": ", 1)
                if len(split_line_list) == 2:
                    key = split_line_list[0].strip()
                    value = split_line_list[1].strip()
                    package_datails[key] = value
                else:
                    print(f"Not a valid discription line: {each_line}")
    except FileNotFoundError:
        return {"code": 40003,
                "message": "File not found"}
    else:
        print(f"Retrieved package Details:{package_datails}")
        return {"code": 200,
                "message": "Package data retrieved successfully",
                "data": package_datails}


def db_curser_to_list(pack_curser):
    """
    DB cursor object coverted into readable list of objects
    by deleting _id property.

    Args:
        pack_curser (Object): DB cursor object

    Returns:
        list: list of found package details in json object
    """
    found_package_list = []
    for package in pack_curser:
        del package['_id']
        found_package_list.append(package)
    return found_package_list
