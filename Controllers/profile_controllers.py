import os
import base64
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
                profile = Profile.create_profile(name,cpf,phone,image_path,user_id)
                if profile:
                    return {"success": "Perfil criado com sucesso!"}
                return {"error": "Erro ao criar o perfil. Tente novamente!"}

            return

    @staticmethod
    def get_profile(user_id):
        return Profile.find_profile_by_User_id(user_id)

    @staticmethod
    def get_profile(user_id):
        profile = Profile.view_profile(user_id)
        if profile and profile.image:
            image_path = profile.image
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    profile.image = base64.b64encode(image_file.read()).decode("utf-8")
            else:
                profile.image = None
        return profile

    @staticmethod
    def get_profile_by_User_id(user_id):
        return Profile.find_profile_by_User_id(user_id)

    @staticmethod
    def get_all_profiles():
        return Profile.view_all_profiles()