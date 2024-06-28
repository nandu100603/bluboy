from flask import Flask, redirect, url_for
app=Flask(__name__)
@app.route('/')
def pri():
    return "bhanu"

@app.route('/<name>')
def sec(name):
    return f"hello {name}"
@app.route("/admin")
def admin():
    return redirect(url_for("sec",name="bhanu"))

if __name__==('__main__'):
    app.run(debug=True)
