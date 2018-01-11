from flask_restful import Resource, reqparse
from werkzeug import FileStorage
from flask_uploads import UploadNotAllowed
from flask import send_file
from flask_jwt import jwt_required, current_identity
import traceback

from models.image import ImageModel


class ImageUpload(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('image',
        type=FileStorage,
        location='files',
        required=True,
        help='Please specify the file to upload.'
    )
    parser.add_argument('filename', type=str, required=False)

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
        image_helper = ImageModel(user)
        data['filename'] = image_helper.get_true_filename(**data)
        if not image_helper.is_filename_safe(data['filename']):
            return {'message': f'Filename <{data["filename"]}> is illegal.'}, 400

        # # check if the image file already exists under the current user's folder
        # if image_helper.exists(data['filename']):
        #     return {'message': f'File <{data["filename"]}> already exists.'}, 400
        # save the image into the user's folder
        try:
            # save(self, storage, folder=None, name=None)
            saved_filename = image_helper.save_to_disk(**data)
            # here we only return the basename of the image and hide the
            # internal folder structure from our user
            basename = image_helper.get_basename(saved_filename)
            return {'message': f'Image <{basename}> uploaded!'}, 201
        except UploadNotAllowed:    # forbidden file type
            extension = image_helper.get_extension(data['filename'])
            return {'message': f'Extension <{extension}> is not allowed.'}, 400

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
        image_helper = ImageModel(user)
        data['filename'] = image_helper.get_true_filename(**data)
        # check if the image file exists under the current user's folder
        if not image_helper.exists(data['filename']):
            return {'message': f'Image <{data["filename"]}> not found.'}, 404
        # update the image if exists
        try:
            # delete previous file and save new file
            image_helper.delete_from_disk(data['filename'])
            updated_file = image_helper.save_to_disk(**data)
            updated_filename = image_helper.get_basename(updated_file)
            return {'message': f'Image <{updated_filename}> updated!'}, 200
        except:
            # the filename has to be legal thus we do not know what went wrong
            return {'message': 'Internal server error!'}, 500


class Image(Resource):

    @jwt_required()
    def get(self, filename):
        """
        This endpoint returns the requested image if exists. It will use JWT to
        retrieve user information and look for the image inside the user's folder.
        """
        user = current_identity
        image_helper = ImageModel(user)

        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {'message': f'Illegal filename <{filename}> requested.'}, 400
        try:
            # try to send the requested file to the user with status code 200
            return send_file(image_helper.get_path(filename))
        except FileNotFoundError:
            return {'message': f'Image <{filename}> not found.'}, 404

    @jwt_required()
    def delete(self,filename):
        """
        This endpoint is used to delete the requested image under the user's folder.
        It uses the JWT to retrieve user information.
        """
        user = current_identity
        image_helper = ImageModel(user)

        # check if filename is URL secure
        if not image_helper.is_filename_safe(filename):
            return {'message': f'Illegal filename<{filename}> requested.'}, 400

        try:
            image_helper.delete_from_disk(filename)
            return {'message': f'File <{filename}> deleted!'}, 200
        except FileNotFoundError:
            return {'message': f'File <{filename}> not found!'}, 404
        except:
            traceback.print_exc()
            return {'message': 'Internal Server Error.'}, 500
