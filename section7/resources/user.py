from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank.'
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field cannot be blank.'
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be blank.'
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        if UserModel.find_by_email(data['email']):
            return {'message': 'A user with that email already exists'}, 400

        user = UserModel(data['username'], data['email'], data['password'])
        user.save_to_db()
        try:
            response = user.send_confirmation_email()
            if response.status_code != 200:
                print(response.status_code)
                print(response.json())
                raise Exception("Error in sending confirmation email, user registration failed.")
        except Exception as e:
            user.delete_from_db()  # rollback
            return {'message': str(e)}, 500

        return {'message': 'User created successfully.'}, 201



class UserConfirm(Resource):

    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if not user:
            return {'message': 'User Not Found'}, 404

        user.activated = True
        user.save_to_db()

        # TODO: replace response with a web page
        return {'message': 'User register confirmed'}, 200


class User(Resource):

    def get(self, _id):
        user = UserModel.find_by_id(_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return {'user': user.json()}, 200
