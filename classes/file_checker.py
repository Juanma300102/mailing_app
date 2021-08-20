

class Checker:
    def __init__(self, app) -> None:
        self.app = app
    
    def check_file(self, file:str, request) -> bool:
        if file not in request.files or request.files.get(file).filename == '':
            return False
        elif file in request.files:
            return True
    
    def check_form_part(self, part:str, request):
        if part not in request.form:
            pass
        elif part in request.form:
            pass
        
        
        
        