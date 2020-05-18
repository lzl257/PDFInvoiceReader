import os


class PDFReader():
    
    def __init__(self, upload_widget):
        self.upload = upload_widget
        self.temp_dir = os.getcwd() + "/Rechnung"
        
    def upload(self):        
        os.system(f"mkdir {self.temp_dir}")

        uploaded_filenames = list(self.upload.value.keys())
        for uploaded_filename in uploaded_filenames:
            content = self.upload.value[uploaded_filename]['content']


            with open(f'{self.temp_dir}/{uploaded_filename}', 'wb') as f: 
                f.write(content)
                
    
    def delete(self):
        os.system(f"rm -r {self.temp_dir}")
        os.system("rm *.txt")