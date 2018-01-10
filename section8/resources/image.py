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
        """
        This endpoint is used to upload and create an image file. It uses the
        JWT to retrieve user information and save the image in the user's folder.
        If a file with the same name exists in the user's folder, name conflicts
        will be automatically resolved by appending a underscore and a smallest
        unused integer. (eg. filename.png to filename_1.png).

        """
        data = self.parser.parse_args()

        # we use a sub folder for each user using the user.id
        user = current_identity
        folder = 'user_{}'.format(user.id)

        # # check if the image file already exists under the current user's folder
        # if os.path.isfile(image_set.path(data['image'].filename,folder)):
        #     return {'message': 'File <{}> already exists.'.format(data['image'].filename)}, 400
        # save the image into the user's folder
        try:
            # save(self, storage, folder=None, name=None)
            filename = image_set.save(data['image'],folder)
            # use url(self, filename) if prefer to return url
            return {'filename': filename}, 201
        except UploadNotAllowed:    # forbidden file type
            return {'message': 'Extension <{}> is not allowed.'.format(
                os.path.splitext(data['image'].filename)[1])}, 400

    @jwt_required()
    def put(self):
        """
        This endpoint is used to update an image only. If the requested image
        file does not exist, a 404 will be returned. If the file does exist,
        then the image file will be overwritten by the uploaded image.
        """
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
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        data = self.parser.parse_args()

        user = current_identity
        folder = 'user_{}'.format(user.id)

        try:
            return send_file(image_set.path(data['filename'],folder))
        except FileNotFoundError:
            return {'message': 'Image <{}> not found.'.format(data['filename'])}, 404

    @jwt_required()
    def delete(self):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to retrieve user information.
        """
        data = self.parser.parse_args()

        user = current_identity
        folder = 'user_{}'.format(user.id)

        try:
            os.remove(image_set.path(data['filename'],folder))
        except FileNotFoundError:
            return {'message': 'File <{}> not found!'.format(data['filename'])}, 404
        except:
            traceback.print_exc()
            return {'message': 'Internal Server Error.'}, 500
        return {'message': 'File <{}> deleted!'.format(data['filename'])}, 200
