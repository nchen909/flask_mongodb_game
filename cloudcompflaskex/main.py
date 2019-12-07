#encoding:utf-8
#!/usr/bin/env python
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort
import time
import os
from strUtil import Pic_str
import base64
from flask_bootstrap import Bootstrap
# import ansible.runner
# import commands

app = Flask(__name__)
bootstrap = Bootstrap(app)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
 
# @app.route('/upload')
# def upload_test():
#     return render_template('upload_pic.html')

@app.route('/')
def upload():
    return render_template('upload_pic.html')


# 上传文件
@app.route('/up_photo', methods=['POST'], strict_slashes=False)
def api_upload():
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['photo']
    if f and allowed_file(f.filename):
        fname = secure_filename(f.filename)
        print(fname)
        ext = fname.rsplit('.', 1)[1]
        new_filename = Pic_str().create_uuid() + '.' + ext
        f.save(os.path.join(file_dir, new_filename))
    
        return jsonify({"success": 0, "msg": "上传成功"})
    else:
        return jsonify({"error": 1001, "msg": "上传失败"})
    #cmd = 'curl -X POST -H "ServiceID:uaiservice-ad53msad" -H "Token:32f184961bc5d17e10c372ecad40e475" http://uinference-sh2.ucloud.cn/service  -T 2.jpg'
    cmd=' curl -X POST -H "ServiceID:uaiservice-zsegqykh" -H "Token:5e40cfa614aba43c8f81da595e4d3b20" http://uinference-sh2.service.ucloud.cn/service -T 2.png'
    msg = os.popen(cmd).read()
    print(msg)
    render_template('upload_pic.html', result=msg)


@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)
        pass


@app.route('/cmd', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        cmd = request.form.get('cmd', type=str, default=None)
        ip = request.form.get('ip', type=str, default=None)
        host_cfg = os.path.join(basedir, 'host.cfg')
        print(cmd, ip, host_cfg)
        # 1 or None None or 1
        # 1 and None None or 1
        # if cmd or ip:
        # 对比结果
        if cmd and ip:
            # runner = ansible.runner.Runner(
            #     host_list=os.path.join(basedir, host_cfg),
            #     module_name='shell',
            #     module_args=cmd,
            #     pattern=ip,
            #     forks=10
            # )
            # datastructure = runner.run()
            for key, value in datastructure.items():
                if 'contacted' in key:
                    exec_result = value
            return render_template('upload_pic.html', result="test", ip=ip, cmd=cmd)
        else:
            return render_template('upload_pic.html')
    else:
        return render_template('upload_pic.html')   
    
# show photo
@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

 
if __name__ == '__main__':
    app.run(debug=True,host='10.24.5.57',port=5000)#'10.24.5.57'