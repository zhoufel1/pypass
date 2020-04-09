import sqlalchemy as sql
from sqlalchemy.ext import declarative
from sqlalchemy import orm

class AccountDatabase:
    Base = declarative.declarative_base()

    class Account(Base):
        __tablename__ = 'account'
        id = sql.Column(sql.Integer, primary_key=True)
        site = sql.Column(sql.String)
        username = sql.Column(sql.String)
        password = sql.Column(sql.String)

    class MasterPassword(Base):
        __tablename__ = 'password'
        id = sql.Column(sql.Integer, primary_key=True)
        password = sql.Column(sql.String)

    def __init__(self) -> None:
        self.engine = sql.create_engine('sqlite:///account_database.db')
        self.Base.metadata.bind = self.engine
        self.DBSession = orm.sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def create_database(self) -> None:
        self.Base.metadata.create_all(self.engine)

    def is_empty(self) -> bool:
        return not self.query_all_unfiltered()

    def insert_account(self, site: str, username: str, password: str) -> None:
        self.session.add(self.Account(site=site, username=username, password=password))
        self.session.commit()

    def query_all_unfiltered(self) -> list:
        return self.session.query(self.Account).all()

    def query_by_site_and_user(self, site: str, username: str) -> dict:
        results = {}
        queries = self.session.query(self.Account).filter(self.Account.site == site).filter(self.Account.username == username)
        for instance in queries:
            if instance.site not in results:
                results[instance.site] = [instance]
            else:
                results[instance.site].append(instance)
        return results

    def query_all_categorized(self) -> dict:
        results = {}
        query_all = self.session.query(self.Account).all()
        sites = sorted({x.site for x in query_all})
        for item in sites:
            query = self.session.query(self.Account).filter(self.Account.site == item)
            results[item] = query
        return results

    def update_entry_password(self, site: str, username: str, new_password: str) -> None:
        query = self.session.query(self.Account).filter(self.Account.site == site).filter(self.Account.username == username)
        query[0].password = new_password
        self.session.commit()

    def delete_entry(self, site: str, username: str) -> None:
        self.session.query(self.Account).filter(self.Account.site == site).filter(self.Account.username == username).delete()
        self.session.commit()

    def delete_all(self) -> None:
        self.session.query(self.Account).delete()
        self.session.commit()

    def set_master_password(self, password: str) -> None:
        self.session.add(self.MasterPassword(password=password))
        self.session.commit()

    def retrieve_master_password(self) -> bytes:
        query = self.session.query(self.MasterPassword).all()
        try:
            return query[0].password
        except:
            raise Exception("Master password was not saved on initialization. Delete account_database.db")
