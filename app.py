from flask import Flask
from config import Config
import models
import auth
import gastos


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.teardown_appcontext(models.close_db)
    app.register_blueprint(auth.bp)
    app.register_blueprint(gastos.bp)

    @app.template_filter("moneda")
    def moneda(valor):
        return f"S/ {valor:,.2f}"

    with app.app_context():
        models.init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)