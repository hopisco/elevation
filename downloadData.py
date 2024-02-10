#!/usr/bin/python
import requests # get the requsts library from https://github.com/requests/requests
import zipfile, io
import glob, os
import time
import multiprocessing

# overriding requests.Session.rebuild_auth to mantain headers when redirected
class SessionWithHeaderRedirection(requests.Session):

    AUTH_HOST = 'urs.earthdata.nasa.gov'
    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from
    # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url

        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)

            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']

        return

def getUrl(url):
    # create session with the user credentials that will be used to authenticate access to the data
    username = urs.earthdata.nasa.gov_USERNAME
    password= urs.earthdata.nasa.gov_USER_PASSWORD

    session = SessionWithHeaderRedirection(username, password)

    retry = 0
    try:
        while True:
            try:
                response = session.get(url, stream=True)
                response.raise_for_status()
                break

            except:
                retry += 1
                if retry > 10:
                    raise Exception("Error getting {}".format(url))

        # save the file
        with io.BytesIO() as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                f.write(chunk)
            
            z = zipfile.ZipFile(f)
            z.extractall("elevationTiles/")

            for f in glob.glob("elevationTiles/*_num.tif"):
                os.remove(f)

    except Exception as e:
        # handle any errors here
        print(e)

if __name__ == "__main__":
    # Using readlines()
    file1 = open('list.txt', 'r')
    Lines = file1.readlines()

    count = 0

    # Strips the newline character
    start = time.time()
    process_list = []

    for line in Lines:
        while len(process_list) > 10:
            # Did a process finish ?       
            tmp = []

            for process in process_list:
                process.join(timeout=0)
                if process.is_alive():
                    tmp.append(process)

            process_list = tmp.copy()

        #print("[Info] {} process are running".format(len(process_list)))
        url = line.strip()
        
        proc = multiprocessing.Process(target=getUrl, args=(url,))
        process_list.append(proc)
        proc.start()

        count += 1
        
        print("[Started] {}/22912 in {} seconds".format(count, time.time()-start))

        #extract(url)