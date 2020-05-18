import base64
from IPython.display import HTML


def create_download_link(df, title = "下载CSV", filename = "iaa_report.csv"):  
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = f'<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    
    return HTML(html)