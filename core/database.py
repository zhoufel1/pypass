import sqlalchemy as sql
from sqlalchemy.ext import declarative
from sqlalchemy import orm


class Database:
    Base = declarative.declarative_base()

    class Account(Base):
        __tablename__ = 'account'
        id = sql.Column(sql.Integer, primary_key=True)
        site = sql.Column(sql.String)
        username = sql.Column(sql.String)
        password = sql.Column(sql.String)

    class Password(Base):
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

    def insert_data(self, site: str,
                    username: str, password: str) -> None:
        self.session.add(self.Account(site=site,
                                      username=username, password=password))
        self.session.commit()

    def query_database(self) -> list:
        return self.session.query(self.Account).all()

    def query_site_and_user(self, site: str, username: str) -> dict:
        results = {}
        queries = self.session.query(self.Account).\
            filter(self.Account.site == site).\
            filter(self.Account.username == username)
        for instance in queries:
            if instance.site not in results:
                results[instance.site] = [instance]
            else:
                results[instance.site].append(instance)
        return results

    def query_all_entries(self) -> dict:
        results = {}
        query_all = self.session.query(self.Account).all()
        sites = sorted({x.site for x in query_all})
        for item in sites:
            query = self.session.\
                    query(self.Account).filter(self.Account.site == item)
            results[item] = query
        return results

    def is_empty(self) -> bool:
        return not self.query_database()

    def update_item(self,
                    site: str, username: str, new_password: str) -> None:
        query = self.session.query(self.Account).\
            filter(self.Account.site == site).\
            filter(self.Account.username == username)
        query[0].password = new_password
        self.session.commit()

    def drop_tables(self) -> None:
        self.session.query(self.Account).delete()
        self.session.commit()

    def delete_row(self, site: str, username: str) -> None:
        self.session.query(self.Account).filter(self.Account.site == site).\
            filter(self.Account.username == username).delete()
        self.session.commit()

    def set_password(self, password: str) -> None:
        self.session.add(self.Password(password=password))
        self.session.commit()

    def retrieve_password(self) -> bytes:
        query = self.session.query(self.Password).all()
        return query[0].password
