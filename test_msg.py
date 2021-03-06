from socket import *
import sys
import json
import time
import thread


HOST = '127.0.0.1'
PORT = 10101
MAX_LENGTH = 4096
ADDR = (HOST, PORT)

def until_crlf(line):
	return line.split('\r')[0]

def print_response(prefix, data):
	data = data.replace('\r\n', '\n')
	rows = data.split('\n')
	for row in rows:
		if not row:
			continue

		print '%s response :' % prefix

		parsed = json.loads(row)
		print json.dumps(parsed, indent=4, sort_keys=True)


def client1():
	sock_client1 = socket(AF_INET, SOCK_STREAM)
	try:
		sock_client1.connect(ADDR)
	except Exception as e:
		print e
		sys.exit()


	sock_client1.send('%s\r\n' % (json.dumps({
		'target': 1, 
		'id': 'testuser2',
		'password': 'testuser2'
	})))
	data = sock_client1.recv(MAX_LENGTH)
	print_response('client1', data)

	decoded = json.loads(data)
	access_token = decoded['access_token']

	while True:
		time.sleep(5)

		sock_client1.send('%s\r\n' % (json.dumps({
			'target': 2, 
			'access_token': access_token,
			'message': 'hello world!'
		})))
		print '(client1) chaaaaaaaat!'

		data = sock_client1.recv(MAX_LENGTH)
		print_response('client1', data)

		# sock_client1.send('%s\r\n' % (json.dumps({
		# 	'target': 5, 
		# 	'access_token': access_token
		# })))
		# print '(client1) lobby check!'

		# data = sock_client1.recv(MAX_LENGTH)
		# print_response(data)


def client2():
	sock_client2 = socket(AF_INET, SOCK_STREAM)
	try:
		sock_client2.connect(ADDR)
	except Exception as e:
		print e
		sys.exit()

	sock_client2.send('%s\r\n' % (json.dumps({
		'target': 1, 
		'id': 'testuser3',
		'password': 'testuser3'
	})))

	while True:
		time.sleep(1)
		data = sock_client2.recv(MAX_LENGTH)
		if data:
			print_response('client2', data)


try:
	thread.start_new_thread(client1, ())
	thread.start_new_thread(client2, ())
except Exception as e:
	print 'exception : %s' % e
	pass


while 1:
	time.sleep(1)
	pass