import os
import sys
import requests
from shareplum import Office365

# Set Login Info
username = os.environ['SHAREPUSH_USER']
password = os.environ['SHAREPUSH_PASS']
site_name = os.environ['SHAREPUSH_SITE']
base_path = os.environ['SHAREPUSH_URL']
doc_library = os.environ['SHAREPUSH_DOCLIB']
nested_folder = os.environ['SHAREPUSH_FOLDER']
file_name = os.environ.get('SHAREPUSH_FILE', sys.argv[1] if len(sys.argv) > 1 else '' )

# Obtain auth cookie
authcookie = Office365(base_path, username=username, password=password).GetCookies()
session = requests.Session()
session.cookies = authcookie
session.headers.update({'user-agent': 'python_bite/v1'})
session.headers.update({'accept': 'application/json;odata=verbose'})

session.headers.update({'X-RequestDigest': 'FormDigestValue'})
response = session.post(url=base_path + "/sites/" + site_name + "/_api/web/GetFolderByServerRelativeUrl('" + doc_library + "')/Files/add(url='a.txt',overwrite=true)",
                         data="")
session.headers.update({'X-RequestDigest': response.headers['X-RequestDigest']})

# Upload file
with open(file_name, 'rb') as file_input:
    try:
        response = session.post(
            url=base_path + "/sites/" + site_name + f"/_api/web/GetFolderByServerRelativeUrl('" + nested_folder + "')/Files/add(url='"
            + os.path.basename(file_name) + "',overwrite=true)",

            data=file_input)
        print("response: ", response.status_code) #it returns 200
        if response.status_code == 200:
            print("File uploaded successfully")
        else:
            sys.exit("File uploaded failed")
    except Exception as err:
        sys.exit("Something went wrong: " + str(err))
