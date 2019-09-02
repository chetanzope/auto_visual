# from . import blueprint
from flask import Flask,  render_template, url_for
from app.home.routes import blueprint
from app.dash.routes import dash_app
from dashboard import dash_app1

app = Flask(__name__, static_url_path='/static')


@app.route("/")
def home():
    print("X" * 50)
    return render_template('index.html')

#
# @app.route('/app1/')
# def app1_template():
#     print("Here")
#     return render_template('app1.html', dash_url=dash_app1.url_base)


if __name__ == '__main__':
    app.register_blueprint(blueprint)
    app.register_blueprint(dash_app)
    app = dash_app1.add_dash(app)
    app.run(debug=True)
