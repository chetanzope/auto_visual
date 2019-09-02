from flask import Blueprint
from flask import render_template
from dashboard import dash_app1

dash_app = Blueprint(
    'dash_blueprint',
    __name__,
    url_prefix='/dash',
    template_folder='templates',
    static_folder='static'
)


@dash_app.route('/app1')
def app1_template():
    print("calles")
    return render_template('app1.html', dash_url=dash_app1.url_base)
