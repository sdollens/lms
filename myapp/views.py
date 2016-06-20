# -*- coding: utf-8 -*-
from django.shortcuts import render
from models import *
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
import json
import simplejson
import random
import string

# Create your views here.
def noneIfEmptyString(value):
    if value == "":
        return None
    return value
def noneIfNoKey(dict, key):
    if key in dict:
        value = dict[key]
        if value == "":
            return None
        return value
    return None

class myError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def register(request):
	try:
		print request.body
		data = simplejson.loads(request.body)
		print data
		email = data['user']['email']
		password = data['user']['password']
		repassword = data['user']['repassword']
		if (password == repassword):
			lastUser = User.objects.all().last()
			userID = str(int(lastUser.UserID) + 1)
			user = User()
			user.UserID = userID
			user.password = password
			user.email = email
			user.save()
			result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
				},
			}
		else:
			raise myError('两次输入密码不同!')

	except Exception,e:
		result = {
		'successful': False,
		'error': {
			'id': '1024',
			'msg': e.args,
			},
		}
	finally:
		return HttpResponse(json.dumps(result), content_type="application/json")

def login(request):
	try:
		data = json.loads(request.body)
		email = data['user']['email']
		password = data['user']['password']
		customerUser = User()
		customerUser = User.objects.get(email=email)
		if(password == customerUser.password):
			token = Token()
			token = Token.objects.filter(user=customerUser)
			if(len(token) != 0):
				token.delete()
		else:
			raise myError('登录名或密码错误!')
		customerToken = ''.join(random.sample(string.ascii_letters + string.digits, 30))
		token = Token()
		token.token = customerToken
		token.user = customerUser
		token.expire = '-1'
		token.save()
		result = {
			'data': {
				'token': customerToken,
				'expire': -1,
			},
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			},
		}
	except myError as e:
		result = {
			'successful': False,
			'error': {
				'id': '1',
				'msg': e.value
			}
		}
	except Exception,e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.args
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')

def logout(request):
	try:
		data = json.loads(request.body)
		customerToken = data['token']
		token = Token()
		token = Token.objects.get(token=customerToken)
		token.delete()
		result = {
			'successful': True,
			'error': {
				'id': '',
				'msg': '',
			},
		}
	except Exception as e:
		result = {
			'successful': False,
			'error': {
				'id': '1024',
				'msg': e.args
			}
		}
	finally:
		return HttpResponse(json.dumps(result), content_type='application/json')