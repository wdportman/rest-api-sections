from flask_restful import Resource, reqparse
from werkzeug import FileStorage
from flask_uploads import UploadSet, IMAGES, UploadNotAllowed
from flask import send_file
from flask_jwt import jwt_required,current_identity
import os, traceback

image_set = UploadSet('images', IMAGES)


class ImageUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
        type=FileStorage,
        location='files',
        required=True,
        help='Please specify the file to upload.'
    )

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        # we use a sub folder for each user using the user.id
        user = current_identity
        folder = 'user_{}'.format(user.id)

        # check if the image file already exists under the current user's folder
        if os.path.isfile(image_set.path(data['image'].filename,folder)):
            return {'message': 'File <{}> already exists.'.format(data['image'].filename)}, 400
        # save the image into the user's folder
        try:
            filename = image_set.save(data['image'],folder)
            return {'filename': filename}, 201
        except UploadNotAllowed:    # forbidden file type
            return {'message': 'Extension <{}> is not allowed.'.format(
                os.path.splitext(data['image'].filename)[1])}, 400

    @jwt_required()
    def put(self):  # update an image
        data = self.parser.parse_args()

        # we use a sub folder for each user using the user.id
        user = current_identity
        folder = 'user_{}'.format(user.id)

        # check if the image file exists under the current user's folder
        if not os.path.isfile(image_set.path(data['image'].filename,folder)):
            return {'message': 'Image <{}> not found.'.format(data['image'].filename)}, 404
        # update the image if exists
        try:
            os.remove(image_set.path(data['image'].filename,folder))
            filename = image_set.save(data['image'],folder)
            return {"filename": filename}, 200
        except UploadNotAllowed:    # forbidden file type
            return {'message': 'Extension <{}> is not allowed.'.format(
                os.path.splitext(data['image'].filename)[1])}, 400


class Image(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('filename',
        type=str,
        required=True,
        help='Please specify the filename.'
    )

    @jwt_required()
    def post(self):
        data = self.parser.parse_args()

        user = current_identity
        folder = 'user_{}'.format(user.id)
        try:
            return send_file(image_set.path(data['filename'],folder))
        except FileNotFoundError:
            return {'message': 'Image <{}> not found.'.format(data['filename'])},404

    @jwt_required()
    def delete(self):
        data = self.parser.parse_args()

        user = current_identity
        folder = 'user_{}'.format(user.id)
        try:
            os.remove(image_set.path(data['filename'],folder))
        except FileNotFoundError:
            return {'message': 'File <{}> not found!'.format(data['filename'])},404
        except:
            traceback.print_exc()
            return {'message': 'error'},500
        return {'message': 'File <{}> deleted!'.format(data['filename'])},200
