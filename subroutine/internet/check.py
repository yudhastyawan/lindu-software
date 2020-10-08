import urllib.request
import urllib.error
import requests
import webbrowser

def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib.error.URLError as err:
        return False

if __name__ == '__main__':
    check = internet_on()
    print(check)
    response = requests.get("https://api.github.com/repos/numpy/numpy/releases/latest")
    print(response.json()["tag_name"])
    print(response.json()["body"])
    webbrowser.open("https://github.com/comp-geoph-itera/lindu-software/releases", new=2)