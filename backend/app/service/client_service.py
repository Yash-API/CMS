from sqlalchemy.orm import Session
from app.models import Client, ClientPayment
from sqlalchemy.exc import SQLAlchemyError

def update_client_info(db: Session, client_id: int, client_data):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return None
    for key, value in client_data.dict(exclude_unset=True).items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

def add_payment(db: Session, payment_data):
    try:
        # Create new client payment record
        new_payment = ClientPayment(
            client_id=payment_data.client_id,
            payment_received_date=payment_data.payment_received_date,
            payment_received_amount=payment_data.payment_received_amount
        )
        db.add(new_payment)

        # Update client's total_payment_received and pending_payment
        client = db.query(Client).filter(Client.id == payment_data.client_id).first()
        if client:
            if client.total_payment_received is None:
                client.total_payment_received = 0
            client.total_payment_received += payment_data.payment_received_amount

            if client.budget is not None:
                client.pending_payment = client.budget - client.total_payment_received
            else:
                client.pending_payment = None

            db.add(client)

        db.commit()
        db.refresh(new_payment)
        return new_payment
    except SQLAlchemyError as e:
        db.rollback()
        raise e
