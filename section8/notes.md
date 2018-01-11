# Notes

- We create a folder for each user and allow them to store and access images in their own folder. The user only need to provide base filename, no directory is needed since the `ImageModel` will take care of it for us.
- Used `werkzeug` built-in `secure_filename()` function to check if filename is URL safe and does not contain illegal characters.
- Check if `filename` and `image`(from `ImageUpload.parser`) has the same file extension, if not, use the `image`'s extension.
- In the `PUT` endpoint, we deleted the old file and then upload the new file. We do not need to worry about having deleted the old file already and then find out the new file throws `UploadNotAllowed` error. Since if we find the old file with the same name, then the filename has to be legal.
- `os.path.splitext()` is used to split the extension. `splitext` stands for "split ext" not "split text". `os.path.split()` is used to extract the basename of the file. For example:

```
os.path.split(`dir/avatar.jpg`) => ('dir','avatar.jpg')
os.path.splitext(`dir/avatar.jpg`) => ('dir/avatar','.jpg') 
```
