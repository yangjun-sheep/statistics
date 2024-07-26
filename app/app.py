from flask import Flask
from app.config import Config
from app.exts import db, migrate, marshmallow
from app.apis import bp
from flask_cors import CORS
from app.models import *  # noqa


app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)
migrate.init_app(app, db)

marshmallow.init_app(app)

app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(port=9000, debug=True)
