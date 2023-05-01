import random
from app import ADMIN_LIST

class Admin:
    def choose_admin():
        return random.choice(ADMIN_LIST)
    
    def choose_superadmin():
        return ADMIN_LIST[0]
    

    def add_admin(user_id):
        ADMIN_LIST.append(user_id)


    def delete_admin(user_id):
        try:
            ADMIN_LIST.remove(user_id)
        except:
            return