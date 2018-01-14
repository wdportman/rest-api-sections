from werkzeug import secure_filename
from flask_uploads import UploadSet, IMAGES
import os, re, traceback

from models.user import UserModel

IMAGE_SET = UploadSet('images', IMAGES)
AVATAR_SET = UploadSet('avatars', IMAGES)


class ImageModel:
    def __init__(self, user):
        self.folder = f'user_{user.id}'
        self.avatar = f'user_{user.id}_avatar'

    # check filename security using regular expression
    @classmethod
    def is_filename_safe_regex(cls, filename):
        allowed_format = ''
        # format IMAGES into regex, eg:
        # ('jpeg','png') --> 'jpeg|png'
        for fmt in IMAGES:
            allowed_format += fmt + '|'
        # remove last '|'
        allowed_format = allowed_format[:-1]

        # allowed_chars are a-z A-Z 0-9 _ and .
        # starts with allowed_chars at least one time
        # followed by a dot (.) and a allowed_format at the end
        regex = f'^[a-zA-Z0-9_\.]+\\.({allowed_format})$'
        return re.match(regex, filename) is not None

    @classmethod
    def is_filename_safe(cls, filename):
        return filename == secure_filename(filename)

    @classmethod
    def get_basename(cls, filename):
        """
        return file's basename, for example
        get_basename('some/folder/image.jpg') returns 'image.jpg'
        """
        # split into (directory, basename)
        return os.path.split(filename)[1]

    @classmethod
    def get_extension(cls, filename):
        """
        return file's extension, for example
        get_extension('image.jpg') returns '.jpg'
        """
        return os.path.splitext(filename)[1]

    @classmethod
    def get_true_filename(cls, image, filename):
        """
        This method will generate a true file name for the given file
        If the filename is specified, it will check if it's using the
        filename has the same extension as the given image, and subsitute
        its extension if there's a difference.
        If the filename is not specified, it will return the image's name
        """
        true_ext = cls.get_extension(image.filename)
        if not filename:    # filename unspecified
            # use image name
            return cls.get_basename(image.filename)
        # if filename is specified, test if extension is true
        if cls.get_extension(filename) == true_ext:
            return cls.get_basename(filename)
        else:
            # get basename and then split extension
            name, ext = os.path.splitext(cls.get_basename(filename))
            print(f'use true extension <{true_ext}> instead of <{ext}>')
            # split the basename and concatenate with true extention
            return name + true_ext

    def exists(self, filename):
        """
        check if the image exists in the user's folder
        """
        return os.path.isfile(IMAGE_SET.path(filename, self.folder))

    def get_path(self, filename):
        """
        return the absolute path the to file
        """
        return IMAGE_SET.path(filename, self.folder)

    def save_user_avatar(self, image):
        """
        save the user's profile image
        if there is already an avatar for the current user
        delete the previous avatar and then save the new one
        """
        self.delete_user_avatar()
        ext = self.get_extension(image.filename)
        return AVATAR_SET.save(image, name = f'{self.avatar}{ext}')   # (file, folder, name)

    def delete_user_avatar(self):
        for _format in IMAGES:
            # eg: look for user_1.jpg in static/img/avatar folder
            filename = AVATAR_SET.path(f'{self.avatar}.{_format}')
            if os.path.isfile(filename):
                os.remove(filename)
                return

    def get_user_avatar(self):
        """
        check if the user's avatar file exists in the avatar folder
        """
        for _format in IMAGES:
            # eg: look for user_1.jpg in static/img/avatar folder
            filename = AVATAR_SET.path(f'{self.avatar}.{_format}')
            if os.path.isfile(filename):
                return filename

    def save_to_disk(self, image, filename):
        return IMAGE_SET.save(image, self.folder, filename)

    def delete_from_disk(self, filename):
        os.remove(IMAGE_SET.path(filename, self.folder))
