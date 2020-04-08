import encryption
from database import AccountDatabase

def update_password(database: AccountDatabase, key: bytes, site: str, username: str, new_password:str) -> None:
    encrypted_password = encryption.encrypt_password(new_password, key)
    database.update_item(selection.site, selection.username, encrypted_password)
