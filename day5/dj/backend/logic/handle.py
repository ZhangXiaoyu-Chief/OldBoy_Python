from backend.db.sql_api import select
def home():
    res = select('user')
    print('welcome to my home page ...')
    print(res)

def movie():
    print('welcome to movie page ...')

def tv():
    print('welcome to tv page ...')