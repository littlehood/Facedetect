# encoding:utf-8
"""人脸检测模块"""
__author__ = "JIMhackKING"

import base64
import requests
import json
import access_token

'''
人脸检测接口
'''
# 传入的参数为图片的内容，不能是 bytes
def detect(image):
	img = base64.b64encode(image)

	detectUrl = "https://aip.baidubce.com/rest/2.0/face/v1/detect"
	params = {"max_face_num": 1, "face_fields": "age,beauty,expression,faceshape,gender,glasses,race",
	          "image": img}

	token = access_token.AuthService()
	detectUrl = detectUrl + "?access_token=" + token
	request = requests.post(detectUrl, data=params, headers = {'Content-Type':'application/x-www-form-urlencoded'})

	content = request.content
	if content:
	    return json.loads(content)
