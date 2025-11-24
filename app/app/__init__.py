from flask import Flask
from .extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'replace_with_a_secure_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        from .models import Property
        if not Property.query.first():
            p1 = Property(name='Downtown Apartment', total_value=100000, total_fractions=100, available_fractions=100, description="Luxury apartment in the heart of the city.", location="Downtown", image_url="downtown.jpg")
            p2 = Property(name='Suburban House', total_value=200000, total_fractions=200, available_fractions=200, description="Spacious family home in the suburbs.", location="Suburbs", image_url="suburban.jpg")
            db.session.add(p1)
            db.session.add(p2)
            db.session.commit()

    return app
