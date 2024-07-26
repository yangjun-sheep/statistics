# TODO 对接用户中心
class UserService:

    def get_by_id(self, id):
        data = {
            1: {
                'id': 1,
                'name': 'Jack'
            },
            2: {
                'id': 2,
                'name': 'Han'
            },
            3: {
                'id': 3,
                'name': 'Tom'
            }
        }
        return data.get(id)

    def auth(self, token):
        return 1


user_service = UserService()
