from werkzeug import secure_filename
from flask_uploads import UploadSet, IMAGES
import os

from models.user import UserModel

IMAGE_SET = UploadSet('images', IMAGES)


class ImageModel:
    def __init__(self, user):
        self.folder = f'user_{user.id}'

    @classmethod
    def is_filename_safe(cls, filename):
        return filename == secure_filename(filename)

    @classmethod
    def get_basename(cls, filename):
        # split into (directory, basename)
        return os.path.split(filename)[1]

    @classmethod
    def get_extension(cls, filename):
        return os.path.splitext(filename)[1]

    @classmethod
    def get_true_filename(cls, image, filename):
        true_ext = cls.get_extension(image.filename)
        if not filename:    # filename unspecified
            # use image name
            return true_ext
        # if filename is specified, test if extension is true
        if cls.get_extension(filename) == true_ext:
            return cls.get_basename(filename)
        else:
            # get basename and then split extension
            name_and_ext = os.path.splitext(cls.get_basename(filename))
            print(f'use true extension <{true_ext}> instead of <{name_and_ext[1]}>')
            # split the basename and concatenate with true extention
            return name_and_ext[0] + true_ext

    def exists(self, filename):
        return os.path.isfile(IMAGE_SET.path(filename, self.folder))

    def get_path(self, filename):
        return IMAGE_SET.path(filename, self.folder)

    def save_to_disk(self, image, filename):
        return IMAGE_SET.save(image, self.folder, filename)

    def delete_from_disk(self, filename):
        os.remove(IMAGE_SET.path(filename, self.folder))
