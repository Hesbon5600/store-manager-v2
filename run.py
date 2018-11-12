'''Run the application'''
from app import create_app
from app.api.v2.models.dbmodels import Dtb

app = create_app('development')

DBOBJ = Dtb()
DBOBJ.create_tables()


@app.route('/')
def index():
    return "<p><a \
    href='https://documenter.getpostman.com/view/4074074/RzZ1qN7c'>\
    Documentation link</a></p>"

if __name__ == "__main__":
    app.run(debug=True)
