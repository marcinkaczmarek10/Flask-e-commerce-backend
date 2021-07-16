from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class SessionManager:
    def __init__(self, session=db.session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            raise err
        finally:
            self.session.close()
