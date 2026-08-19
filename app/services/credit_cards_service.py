from sqlalchemy.orm import Session
from app.models.user import User
from app.models.credit_card import CreditCard
from app.schemas.credit_card import CreditCardCreate

# Create a credit card associated with a specific user
def create_credit_card_for_user(db: Session, username: str, data: CreditCardCreate) -> bool:
    
    # Find user by username
    user = db.query(User).filter(User.username == username).first()
    
    # If user does not exist, return False
    if not user:
        return False

    # Create credit card object linked to user_id
    card = CreditCard(
        user_id=user.id,
        card_number=data.card_number,
        card_holder_name=data.card_holder_name,
        exp_month=data.exp_month,
        exp_year=data.exp_year,
    )

    db.add(card) # Add card to session
    db.commit() # Save to database
    return True
