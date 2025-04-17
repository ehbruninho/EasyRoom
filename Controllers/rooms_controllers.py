import base64
import os
from werkzeug.utils import secure_filename
from Models.rooms import Salas

UPLOAD_FOLDER = 'static/uploads/rooms'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta existe

class RoomController:
    @staticmethod
    def create_room(name, description, capacity, disp, type, local, foto):
        try:
            image_path = None

            # Valida se uma imagem foi enviada para o diretório definido inicialmente
            if foto:
                filename = secure_filename(foto.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                foto.save(image_path)

            sala = Salas.create_room(name, description, capacity, disp, type, local, image_path)
            if sala:
                return {"success": "Sala criada com sucesso!"}
            return {"error": "Erro ao registrar a sala. Tente novamente!"}

        except Exception as e:
            print(f"Erro ao criar sala: {e}")
            return {"error": "Ocorreu um erro no servidor. Tente novamente mais tarde."}

    @staticmethod
    def get_rooms_images():
        salas = Salas.view_room()  # Isso já retorna uma lista de salas
        for sala in salas:
            if sala.foto and os.path.exists(sala.foto):
                with open(sala.foto, "rb") as image:
                    sala.foto = base64.b64encode(image.read()).decode('utf-8')
            else:
                sala.foto = None
        return salas
    @staticmethod
    def get_images_room_by_id(room_id):
        sala = Salas.view_room_by_id(room_id)
        if sala.foto and os.path.exists(sala.foto):
            with open(sala.foto, "rb") as image:
                sala.foto = base64.b64encode(image.read()).decode('utf-8')
        return sala

    @staticmethod
    def get_rooms():
        return Salas.view_room()
    @staticmethod
    def get_rooms_by_id(room_id):
        return Salas.view_room_by_id(room_id)
    @staticmethod
    def remove_room(room_id):
        return Salas.remove_room(room_id)

    @staticmethod
    def att_room(room_id, description, capacity, disp, type, local, foto):
        try:
            image_path = None

            # Valida se uma imagem foi enviada para o diretório definido inicialmente
            if foto:
                filename = secure_filename(foto.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                foto.save(image_path)

            sala = Salas.update_room(room_id, description, capacity, disp, type, local, image_path)
            if sala:
                return {"success": "Sala criada com sucesso!"}
            return {"error": "Erro ao registrar a sala. Tente novamente!"}

        except Exception as e:
            print(f"Erro ao criar sala: {e}")
            return {"error": "Ocorreu um erro no servidor. Tente novamente mais tarde."}
