from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from flask import send_file
from werkzeug import FileStorage

from models.user import UserModel
from models.image import ImageModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class UserAvatar(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
        type=FileStorage,
        location='files',
        required=True,
        help="This field cannot be blank."
    )

    @jwt_required()
    def put(self):  # make sure the avatar is there (overwrite if necessary)
        data = self.parser.parse_args()

        user = current_identity
        image_helper = ImageModel(user)
        filename = image_helper.save_user_avatar(data['image'])

        return {'message': f'User avatar saved as <{filename}>'}, 200

    @jwt_required()
    def get(self):
        user = current_identity
        image_helper = ImageModel(user)
        filename = image_helper.get_user_avatar()
        if not filename:
            return {'message': 'The current user does not have an avatar yet.'}, 404
        return send_file(filename)

    @jwt_required()
    def delete(self):
        user = current_identity
        image_helper = ImageModel(user)
        filename = image_helper.get_user_avatar()
        if not filename:
            return {'message': 'The current user does not have an avatar yet.'}, 404
        try:
            image_helper.delete_user_avatar()
            return {'message': 'Avatar deleted for current user!'}, 200
        except:
            return {'message': 'Internal server error while deleting avatar!'}, 500
