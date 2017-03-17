from flask import Flask
import requests
import base64
import re
import sys

app = Flask(__name__)

@app.route("/v1/<filename>")
def get_content(filename):
    url = get_url(filename)
    file_content = get_file_content(url)
    return file_content

def get_file_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return base64.decodestring(response.json()['content'])
    else:
        return "Failed to get latest commits."

def get_url(filename):
    git_repo = app.config.get('git_repo')
    m = re.search('https://github.com/(.*)', git_repo)
    url = 'https://api.github.com/repos/' + m.group(1) + '/contents/' + filename
    return url

if __name__ == "__main__":
    app.config['git_repo'] = sys.argv[1]
    app.run(debug=True, host='0.0.0.0')