import database as datas

deta = datas.deta
db = deta.Base("users")

def insert_user(username, name, password):
    return db.put({"key":username,"name":name, "password":password})

def get_all_users():
    all_users = db.fetch()
    return all_users.items

def get_user(username):
    return db.get(username)
