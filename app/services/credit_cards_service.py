"""
Credit card storage. The full card number is validated at the API boundary
(app/schemas/credit_card.py) but only the last 4 digits ever reach this
function or the database -- see the README's Security notes section.
"""

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

    # Create credit card object linked to user_id (only last 4 digits retained)
    card = CreditCard(
        user_id=user.id,
        last4=data.card_number[-4:],
        card_holder_name=data.card_holder_name,
        exp_month=data.exp_month,
        exp_year=data.exp_year,
    )

    db.add(card) # Add card to session
    db.commit() # Save to database
    return True
