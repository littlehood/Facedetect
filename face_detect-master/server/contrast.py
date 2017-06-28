# encoding: utf-8

from scripts import match
import getlist
from os import path
from bottle import run, route, request, response, static_file, error
from jinja2 import Template, FileSystemLoader, Environment

# 添加环境变量
__import__("sys").path.append("..")
from scripts import detect

env = Environment(loader=FileSystemLoader("./templates"))
with open("templates/upload.html") as f:
    uploadhtml = f.read()


# 绑定404错误界面
@error(404)
def error404(error):
    return "<h1>404:"


@route("/")
def get():
    response.set_header('Content-Type', 'text/html; charset=utf-8')
    return uploadhtml


@route("/<filepath:path>")
def load_file(filepath):
    return static_file(filepath, "./images")


@route("/", method="POST")
def post():
    # 加载模板
    template = env.get_template("match_result.html")
    # 设置headers
    response.set_header('Content-Type', 'text/html; charset=utf-8')
    response.set_header('Server', 'Super PC Server')

    # 获取表单提交的文件
    file1 = request.files.get("file1")
    if not file1:
        return '<div align="center"><font size="190">文件上传失败。</font></div>'
    # 判断文件类型
    name, ext = path.splitext(file1.filename)
    if ext not in ('.png', '.jpg', '.jpeg'):
        return '''<div align="center"><h1><font color="#CC6633">File extension not allowed.</font></h1>
                  <h1>文件类型错误（只支持 png,jpg,jpeg 格式）或者文件名含有中文</h1></div>'''

    # 保存文件，并判断文件是否存在
    try:
        file1.save("./images/" + file1.filename)
    except IOError:
        image = open("./images/" + file1.filename, 'rb').read()
        img = dict_img(image)
        contr = dict_contr(image)
        s = template.render(ip_address=request["REMOTE_ADDR"],
                            filename=file1.filename,
                            explain=u"已经存在，忽略上传。",
                            img = img,
                            contr = contr
                            )
    else:
        image = open("./images/" + file1.filename, 'rb').read()
        img = dict_imgoff(image)
        contr = dict_controff(image)
        s = template.render(ip_address=request["REMOTE_ADDR"],
                            filename=file1.filename,
                            explain=u"成功上传，尺寸为：%d bytes" % len(image),
                            img=img,
                            contr=contr
                            )
    return s


def math_result(images):
    list = getlist.GetFileList('images', [])

    contr = 0
    dict_ = {}
    for i in list:
        with open(i, 'rb') as f:
            image2 = f.read()
        try:
            result = match.match(images, image2)["result"][0]["score"]
            result = int(result)
            image = i
            # print i
            # print u"比对结果：%d 分" %result
            dict_[image] = result
            if (contr < result):
                contr = result
                image_result = image
        except:
            result = -1

    dict = sorted(dict_.items(), key=lambda d: d[1], reverse=True)
    # print u"最相似图片： %s" %image_result
    # print u"最高比对结果： %d分" %contr
    dict.append(image_result)
    dict.append(contr)
    new_dict = (dict[0][0], dict[0][1],dict[1][0],dict[1][1])
    return new_dict

def dict_img(image):
    list = math_result(image)

    imglist = list[0]
    imglist = imglist[7:]
    return imglist

def dict_contr(image):
    list = math_result(image)

    contrlist = list[1]
    return contrlist

def dict_imgoff(image):
    list = math_result(image)

    imglist = list[2]
    imglist = imglist[7:]
    return imglist

def dict_controff(image):
    list = math_result(image)

    contrlist = list[3]
    return contrlist

if __name__ == '__main__':
    run()