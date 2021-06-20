from flask import Flask,render_template,flash, request, redirect, url_for,send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image


UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst




@app.route('/')
def home():

    if os.path.exists("static/merged_image_v.jpg"):
        os.remove("static/merged_image_v.jpg")

    if os.path.exists("static/merged_image_h.jpg"):
        os.remove("static/merged_image_h.jpg")

    if os.path.exists("static/image1.jpg"):
        os.remove("static/image1.jpg")

    if os.path.exists("static/image2.jpg"):
        os.remove("static/image2.jpg")

    return render_template('index.html')



@app.route('/download/<val>')
def download(val):
    if val=="hor":
        file_path = "static/merged_image_h.jpg"
        return send_file(file_path, as_attachment=True, attachment_filename='merged_file_h.jpg')
    
    if val=="ver":
        file_path = "static/merged_image_v.jpg"
        return send_file(file_path, as_attachment=True, attachment_filename='merged_file_v.jpg')
    return render_template('index.html')




@app.route('/upload', methods=['POST'])
def upload():

    if request.method == 'POST':
        try:    
            image1=request.files["image1"]
            image2=request.files["image2"]

            # image1.save(secure_filename(image1.filename))
            # image1.save(secure_filename(image2.filename))

            # image1=Image.open(image1.filename)
            # image2=Image.open(image2.filename)
            image1=Image.open(image1)
            image2=Image.open(image2)
            

            image1.save("static/image1.jpg","JPEG")
            image2.save("static/image2.jpg","JPEG")


            # image1 = image1.resize((426, 240))
            # image1_size = image1.size
            # image2_size = image2.size
            # new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
            # new_image.paste(image1,(0,0))
            # new_image.paste(image2,(image1_size[0],0))
            ver=request.form.get('vertical')
            hor=request.form.get('horizontal')
            print(ver)
            print(hor)
            
            if ver:
                new_image=get_concat_v(image1,image2)
                new_image.save("static/merged_image_v.jpg","JPEG")
                ver=1

            if hor:
                new_image=get_concat_h(image1,image2)
                new_image.save("static/merged_image_h.jpg","JPEG")
                hor=1
        
        except:
            return render_template("index.html", message="Please Upload only image files.")

            
    return render_template("index.html", message="merged",hor=hor,ver=ver)




#Read the two images
# image1 = Image.open('images/elephant.jpg')

# image2 = Image.open('images/ladakh.png')

# image1 = image1.resize((426, 240))
# image1_size = image1.size
# image2_size = image2.size
# new_image = Image.new('RGB',(2*image1_size[0], image1_size[1]), (250,250,250))
# new_image.paste(image1,(0,0))
# new_image.paste(image2,(image1_size[0],0))
# new_image.save("images/merged_image.jpg","JPEG")
# new_image.show()    

if __name__ == '__main__':
    app.secret_key = 'asdjieijkse2jidjiweojidjiwjeiji'
    app.run(debug=True)