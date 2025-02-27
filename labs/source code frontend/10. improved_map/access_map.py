'''
***WARNING:*** if it stops working:
- delete browsing data OR
- go in incognito mode OR
- open new window OR
- sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
'''

from flask import Flask
from flask import render_template

app = Flask(__name__, static_url_path='')

@app.route("/")
def main():
    return render_template("index.html", apikey="your key...")

if __name__ == "__main__":
    app.run(debug=True)