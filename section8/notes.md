# Notes

- We created a folder for each user and allow them to store and access images in their own folder. The user only need to provide base filename, no directory is needed since the `ImageModel` will take care of it for us.
- We stored all user's avatar in a separate folder than the user upload folder. We used the user's id to create the unique filename for the user's avatar. (e.g. `user_1_avatar.jpg`)
- Used `werkzeug` built-in `secure_filename()` function to check if filename is URL safe and does not contain illegal characters.
- Check if `filename` and `image`(from `ImageUpload.parser`) has the same file extension, if not, use the `image`'s extension.
- In the `PUT` endpoint, we deleted the old file and then upload the new file. We do not need to worry about having deleted the old file already and then find out the new file throws `UploadNotAllowed` error. Since if we find the old file with the same name, then the filename has to be legal.
- `os.path.splitext()` is used to split the extension. `splitext` stands for "split ext" not "split text". `os.path.split()` is used to extract the basename of the file. For example:

```
os.path.split(`dir/avatar.jpg`) => ('dir','avatar.jpg')
os.path.splitext(`dir/avatar.jpg`) => ('dir/avatar','.jpg')
```

- When uploading an image ,if the `RequestParser` raises error even when you have indeed provided the required data with proper argument name, it is probably because we forgot to add `location='files'` in he argument configuration.

- We used two `UploadSet` (`IMAGE_SET` and `AVATAR_SET`) to manage user image and avatar uploads, and store images and avatars in parallel folders. In this way, we can separately manage these two set of assets more conveniently. When never we need to do something with avatar, we use `AVATAR_SET`, and use `IMAGE_SET` to deal with user image uploads, we do not need to worry about their folders and filenames etc.
