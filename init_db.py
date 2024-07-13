from ext import app, db
from models import Guitar, Bass, Keyboard, Microphone, Accessory, Comment, User, Card, Basket





with app.app_context():
    db.drop_all()
    db.create_all()

    admin_user = User(username="admin", password="adminpass", role="Admin")
    db.session.add(admin_user)
    db.session.commit()




