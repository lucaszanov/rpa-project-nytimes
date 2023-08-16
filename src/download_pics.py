import urllib

class DownloadPics:

    def __init__(self):
        pass

    def download_pic(self, url, filename):
        urllib.request.urlretrieve(url, filename)
