from db import queries

class AccessStatus:
    DEFAULT = 0
    ALLOWED = 1
    DENIED = 2


class Authorization:
    @staticmethod
    def check_access(user_id):
        user_access_status = queries.check_access(user_id)
        if user_access_status == None:
            queries.add_user(user_id)
            return False
        return user_access_status[0] != AccessStatus.ALLOWED        


    def deny_access(user_id):
        queries.set_access(user_id, AccessStatus.DENIED)

    
    def allow_access(user_id):
        queries.set_access(user_id, AccessStatus.ALLOWED)