from app import create_app
from app.extensions import db
from app.models import Property, PriceHistory
from datetime import datetime, timedelta
import random

app = create_app()

def seed_history():
    with app.app_context():
        # Create table if not exists (since we added a new model)
        db.create_all()
        
        properties = Property.query.all()
        for prop in properties:
            # Check if history already exists
            if PriceHistory.query.filter_by(property_id=prop.id).first():
                print(f"History already exists for {prop.name}")
                continue
                
            print(f"Generating history for {prop.name}...")
            base_price = prop.total_value / prop.total_fractions
            current_price = base_price
            
            # Generate 30 days of data
            start_date = datetime.utcnow() - timedelta(days=30)
            
            for i in range(30):
                # Random fluctuation between -5% and +5%
                change = random.uniform(-0.05, 0.05)
                current_price = current_price * (1 + change)
                
                # Ensure price doesn't go too low
                if current_price < base_price * 0.5:
                    current_price = base_price * 0.5
                
                timestamp = start_date + timedelta(days=i)
                
                history = PriceHistory(
                    property_id=prop.id,
                    price=current_price,
                    timestamp=timestamp
                )
                db.session.add(history)
            
            # Add current price as the last point
            db.session.add(PriceHistory(property_id=prop.id, price=base_price, timestamp=datetime.utcnow()))
            
        db.session.commit()
        print("History seeding complete.")

if __name__ == "__main__":
    seed_history()
