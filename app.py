from flask import Flask, render_template, request, redirect, url_for, flash
import qrcode
from io import BytesIO
import base64
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Sample reviews
SAMPLE_REVIEWS = [
    {
        'name': 'Dr. Sarah Johnson',
        'rating': 5,
        'comment': 'Exceptional dental care! The team at Indurkar Dental Clinic is incredibly professional and caring. The facilities are modern and clean, and the treatment was painless. Highly recommend!',
        'created_at': datetime(2024, 5, 15)
    },
    {
        'name': 'Rajesh Kumar',
        'rating': 5,
        'comment': 'Best dental clinic in the area! Dr. Indurkar and his team are very knowledgeable and make you feel comfortable throughout the procedure. The follow-up care is excellent.',
        'created_at': datetime(2024, 5, 10)
    },
    {
        'name': 'Priya Sharma',
        'rating': 5,
        'comment': 'I had a wonderful experience at Indurkar Dental Clinic. The staff is friendly, the waiting time is minimal, and the treatment was top-notch. The clinic maintains high standards of hygiene.',
        'created_at': datetime(2024, 5, 5)
    }
]

with app.app_context():
    db.create_all()
    # Add sample reviews if the database is empty
    if Feedback.query.count() == 0:
        for review in SAMPLE_REVIEWS:
            feedback = Feedback(**review)
            db.session.add(feedback)
        db.session.commit()

def generate_qr_code():
    # Google Maps URL for Indurkar Dental Clinic
    url = "https://www.google.com/maps/place/INDURKAR+DENTAL+CLINIC/@19.1844115,77.2981665,17z/data=!3m1!4b1!4m6!3m5!1s0x3bd1d3586995a1ab:0x176bbc2f1428b7ba!8m2!3d19.1844115!4d77.3007414!16s%2Fg%2F11h3zmmjt_?entry=ttu"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create an image from the QR Code
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for displaying in HTML
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

@app.route('/')
def index():
    qr_code = generate_qr_code()
    return render_template('index.html', qr_code=qr_code)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        if not all([name, rating, comment]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('feedback'))
        
        feedback = Feedback(name=name, rating=int(rating), comment=comment)
        db.session.add(feedback)
        db.session.commit()
        
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
    
    # Get all reviews, including sample reviews
    reviews = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('feedback.html', reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True) 