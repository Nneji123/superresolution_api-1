import gdown

def url_to_id(url):
    x = url.split("/")
    return x[5]

id = url_to_id('https://drive.google.com/file/d/1ms1-uVh3VOVVlfdPWbJ8Luei3c4IJJ_J/view?usp=sharing')


def main():
    url = 'https://drive.google.com/uc?id='+id
    output = 'model.onnx'
    gdown.download(url, output, quiet=False)

if __name__=="__main__":
    main()