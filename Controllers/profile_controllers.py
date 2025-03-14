import os
from werkzeug.utils import secure_filename
from Models.profile import Profile, SessionLocal

UPLOAD_FOLDER = "static/uploads/"

class ProfileController:
    @staticmethod
    def create_profile_ct(name, cpf, phone, image_file, user_id):
            if image_file:
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
                Profile.create_profile(name,cpf,phone,image_path,user_id)

            return True

    @staticmethod
    def get_profile(user_id):
        return Profile.find_by_user_id(user_id)
