
from src.shared_models import SharedModel, db


class Organization(SharedModel):

    name = db.Column(db.Text)

    symbol = db.Column(db.Text)
    market = db.Column(db.Text)
