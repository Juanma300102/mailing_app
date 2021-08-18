

class FileChecker:
    def __init__(self, app) -> None:
        self.app = app
    
    def check_file(self, file:str, request) -> bool:
        if file not in request.files or request.files.get(file).filename == '':
            return False
        elif file in request.files:
            return True
        
        
        