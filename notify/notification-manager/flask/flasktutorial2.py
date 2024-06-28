from flask import Flask, redirect, url_for, render_template
app=Flask(__name__)

@app.route('/<name>/<vision>')
def index(name, vision):
    return render_template("index.html", content=name, final=vision)
if __name__=="__main__":
    app.run(debug=True)
