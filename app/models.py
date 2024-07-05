from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50),nullable = True)
    phone_no = db.Column(db.String(10),nullable = True)
    address = db.Column(db.String(80),nullable = True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.user_type}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    hospital_username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='current')
    urgency = db.Column(db.Integer, default=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    vendor = db.Column(db.String(80), nullable = True)
    phone_no = db.Column(db.String(10),nullable = True)
    distance = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return f"Order('{self.item}', '{self.amount}', '{self.status}')"
    
    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item,
            'amount': self.amount,
            'hospital_username': self.hospital_username,
            'status': self.status,
            'urgency': self.urgency,
            'timestamp': self.timestamp.isoformat()  # Convert datetime to string
        }
    
    @staticmethod
    def update_csv():
        import os
        import pandas as pd

        # Specify the directory where the CSV file will be saved
        csv_dir = os.path.join(os.path.dirname(__file__), 'csv_files')  # Path to app/csv_files

        # Ensure the directory exists
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        # Fetch all data from the database
        new_data = Order.query.all()
        data = [row.to_dict() for row in new_data]  # Convert to a list of dictionaries
        df = pd.DataFrame(data)

        # Write to CSV file
        csv_file_path = os.path.join(csv_dir, 'app.csv')
        df.to_csv(csv_file_path, index=False)
        print(f"CSV file saved to {csv_file_path}")  # Debugging line

    @staticmethod
    def _after_insert(mapper, connection, target):
        print("Order inserted, updating CSV...")  # Debugging line
        Order.update_csv()

from sqlalchemy.event import listens_for
listens_for(Order, 'after_insert', Order._after_insert)
# listens_for(Order, 'after_insert', Order._after_insert)
