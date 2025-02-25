
from database import SessionLocal, User






def func():
    session = SessionLocal()
    user = session.query(User).filter(User.id == 1).first()
    if user:
        print('found user')
        return True
        
    print('not found user')
    return False