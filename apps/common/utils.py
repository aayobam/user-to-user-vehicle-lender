class Validators:
    @staticmethod
    def validate_file_size(document):
        content_types = ['application/pdf',
                         'img/jpg', 'imagg/png', 'image/jpeg']
        content_type = document.filename.split('.')[::-1]
        if content_type not in content_types:
            return False
        return True

    @staticmethod
    def validate_password(password: str, confirm_password: str):
        if confirm_password == password:
            return True
        return False
