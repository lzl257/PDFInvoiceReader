import os

class UploadListener():
    
    def __init__(self, upload_obj):
        self.upload_obj = upload_obj
        self.temp_dir = os.getcwd() + "/Rechnung"
        
    def upload_listen(self):
        os.system(f"mkdir {self.temp_dir}")

        uploaded_filenames = list(self.upload_obj.value.keys())
        for uploaded_filename in uploaded_filenames:
            content = self.upload_obj.value[uploaded_filename]['content']


            with open(f'{self.temp_dir}/{uploaded_filename}', 'wb') as f: 
                f.write(content)
                
    def delete(self):
        os.system(f"rm -r {self.temp_dir}")
            
            
    