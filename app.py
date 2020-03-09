from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from repoContributers import get_org_contribution

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if(request.method == "POST"):
        print(request.form)
        org = request.form['org']
        n = request.form['n']
        m = request.form['m']
        repos = get_org_contribution(org, int(n), int(m))
        if(repos == "404"):
            return 'Couldn\'t find the given organization or value of n <=0 or value of m<=0 '
        return render_template('index.html', repos=repos)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
