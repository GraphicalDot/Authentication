#!/usr/bin/env python
#-*- coding: utf-8 -*-


from flask import Flask
from flask import request, jsonify
from flask.ext import restful
from flask.ext.restful import reqparse
from flask import make_response
from flask import Response
import zipfile
from database import collection
import hashlib
import tempfile
import subprocess
import shutil
import json
import os
from bson.json_util import dumps
import boto
import boto.ses
import cStringIO
from PIL import Image
import base64


URL = "23.239.29.14"

aws_access_key="AKIAJJRSIUBZEYECNSLQ"                                                                                                                  
aws_secret_key="ExOqpv3x32ElwliQWNHo6x+s0mxg22gux8r39GAn"
connection = boto.ses.SESConnection(aws_access_key, aws_secret_key)

#PATH = "/home/k/Downloads/Data"
PATH = "/root/Cyclone2/Data"

#The deFAULT PATH WHERE THE IMAGE WILL BE SAVED
IMAGE_PATH = "/usr/share/nginx/html/Images"
#IMAGE_PATH = "/home/k/Desktop"

app = Flask(__name__)
api = restful.Api(app)
# '/register_user' arguments parser
reguser_parser = reqparse.RequestParser()

reguser_parser.add_argument('mac_id', type=str, required=True, location='form')
reguser_parser.add_argument('first_name', type=str, required=True, location='form')
reguser_parser.add_argument('second_name', type=str, required=False, location='form')
reguser_parser.add_argument('email_id', type=str, required=True, location='form')
reguser_parser.add_argument('platform', type=str, required=True, location='form')
reguser_parser.add_argument('modules', type=str, required=True, location='form')
reguser_parser.add_argument('country', type=str, required=True, location='form')
reguser_parser.add_argument('payment_receipt_image', type=str, required=True, location='form')



# '/validate_token' arguments
zip_parser = reqparse.RequestParser()
zip_parser.add_argument('mac_id', type=str, required=True, location='args')
zip_parser.add_argument('key', type=str, required=True, location='args')
zip_parser.add_argument('path', type=str, required=True, location='args')
zip_parser.add_argument('check_module', type=str, required=False, location='args')



test_parser = reqparse.RequestParser()
test_parser.add_argument('password', type=str, required=True, location='form')



approved_users = reqparse.RequestParser()
approved_users.add_argument("key", type=str, required="args")




class RegisterUser(restful.Resource):

    def post(self):
		"""
		When a new user register to our website or form. He submits his/her detail throught this method
		Then this method calcualtes the hash of user_email, user_name, mac_id 
		
		the key which will be provided to the user will be the last 10 alphabets of the function.
		The hash function will be used to encrypt the zip file sent to the user

		"""
		args = reguser_parser.parse_args()
		users = collection("users")
		
		
		if users.find_one({"email_id": args["email_id"], "mac_id": args["mac_id"], "modules": args["modules"]}):
			return {
				"error": False,
				"success": True,
				"messege": "Registration has already been done"
				}
		
		try:	
			if args["email_id"] not in connection.list_verified_email_addresses()['ListVerifiedEmailAddressesResponse']['ListVerifiedEmailAddressesResult']['VerifiedEmailAddresses']:
				connection.verify_email_address(args["email_id"])
		
		except boto.exception.BotoServerError:
			return {
				"error": False,
				"success": True,
				"messege": "The email provided is not valid, Please provide a valid email address"
				}


		string = args.get("email_id").lower() + args.get("mac_id").lower() + args.get("first_name").lower() + args.get("modules")
		hash = hashlib.md5(string).hexdigest()
		key = hash[-10:]
		args["hash"] = hash
		args["key"] = key
		args["approved"] = False
		args["key_email_sent"] = False	
		
		if not users.find_one({"email_id": args["email_id"], "mac_id": args["mac_id"], "modules": args["modules"]}):
			try:
				image_output = cStringIO.StringIO()
				image_output.write(base64.decodestring(args["payment_receipt_image"]))
				image_output.seek(0)	
				im = Image.open(image_output)
				payment_receipt_path = "%s/%s.%s"%(IMAGE_PATH, key, im.format)
				im.save(payment_receipt_path)
			except IOError:
				return {
					"error": False,
					"success": True,
					"messege": "The image uploaded is not a valid image file, please upload correct image file",
					}


			args["payment_receipt_path"]  = ("%s/")%URL + "/".join(payment_receipt_path.split("/")[-2:])
			#args["payment_receipt_path"] = payment_receipt_path
			users.insert(args, safe=True)
		
			#sending an email for verification
			
			##TODO: send an email through ses
			return {
				"error": False,
				"success": True,
				"messege": "Registration has been completed, A mail has been sent to the email you mentioned and your key is %s"%key,}




class GetFile(restful.Resource):

	def get(self):
		"""
		If path is not present then it returns the new zip encrypted with the hash
		"""
		import json
		args = zip_parser.parse_args()
		print args["path"]
		print args["mac_id"]
		users = collection("users")

		print json.dumps(args)

		if args["check_module"]:#When user has paid the expenses and bought the module
			user = users.find_one({"key": args["key"], "mac_id": args["mac_id"]})

			if user:

				if not user["key_email_sent"]:
					try:
						connection.send_email("jindal.vikram@gmail.com", "eMetc Notification email", "This is the key you need to play metc modules %s"%user["key"], user["email_id"])
						users.update({"key": user.get("key")}, {"$set": {"key_email_sent": True}})
					except Exception:
						return {
							"error": True,
							"success": False,
							"error_code": 208,
							"messege": " Email address is not verified yet, Please verify your email address.",}
					
				if users.find_one({"key": args["key"], "mac_id": args["mac_id"]})["approved"]:
					return {
						"success": True,
						"error": False,
						"module_name": users.find_one({"key": args["key"], "mac_id": args["mac_id"]})["modules"],
						"hash": users.find_one({"key": args["key"], "mac_id": args["mac_id"]})["hash"],}


				else:
					return {
						"success": False,
						"error": True,
						"error_code": 205,
						"messege": "Your request for approval of your payment is still pending",}


		if not users.find_one({"key": args["key"],}): #when the key is wrong
			if users.find_one({"mac_id": args["mac_id"]}):
				return {
					"error": True,
					"success": False,
					"error_code": 201,
					"messege": "The Key Entered is not valid",}
			else: 					#When the user has not registered for may module
				return {
					"error": True,
					"success": False,
					"error_code": 202,
					"messege": "Please register for this file to run",}


		if users.find_one({"key": args["key"]})["mac_id"] != args["mac_id"]:
			return {
					"error": True,
					"success": False,
					"error_code": 1203,
					"messege": "Same key cannot be used on two Computers",}

		
		if args["path"] == "True":
			return{
					"error": False,
					"success": True,
					"hash": users.find_one({"key": args["key"]}, fields={"_id": 0, "hash": 1})["hash"]}

		print "\n\n Now the file is being transffered"
		
		###
		#The below code only exceutes when users exists and path doesnt exists
		###
		user_data = users.find_one({"key": args["key"]}, fields={"_id": 0})


		password = user_data["hash"]
		module_name = user_data["modules"]
		user_os = user_data["platform"]

	
		#This gets the location where the data is present 
		#The data location will be selected on the basis of the modules the user bought and the platform
		#directory structure for data:
		# 	Data:
		# 		Economics 				Accounting  		 	etc	
		#			:win_Economics.zip				:win_Accounting.zip
		# 			:dar_Economics.zip 				:dar_Accounting.zip
		#for remote server
		#data_location = "/root/Cyclone2/Data/%s/%s_%s.zip"%(module_name, user_os[:3], module_name)

		#for localhost
		data_location = "%s/%s/%s_%s.zip"%(PATH, module_name, user_os[:3], module_name)

		
		try:
			open(data_location, "rb")
		except IOError as e:
			return{
					"error": True,
					"success": False,
					"error_code": 1216,
					"messege": "Unfortunately, This module has not been uploaded yet",}


		#This creates a temporary folder 
		temporary_dir_path = tempfile.mkdtemp() 

		

		#This is the whole path of the ebcrypted xip file in the temporary directory
		temporary_zip_file = "%s/%s_%s.zip"%(temporary_dir_path,  user_os[:3], module_name)

		#This creates the encrypted zip file on the location mentioned above
		subprocess.call(["7z", "a",  temporary_zip_file,  "-P%s"%password , data_location])
	
		#This reads the data from the temporary location present above
		f = open(temporary_zip_file, "r")

		print str(os.path.getsize(data_location))

		response = make_response(f.read())
		response.headers['Cache-Control'] = 'no-cache'
		response.headers["Content-Disposition"] = "attachment; filename=%s_%s.zip"%(user_os[:3], module_name)
		response.headers['data-length'] = str(os.path.getsize(temporary_zip_file))               
		#response.headers['X-Accel-Redirect'] = temporary_zip_file
		#This deletes the temporary encrypted zip file
		print str(os.path.getsize(temporary_zip_file))
		shutil.rmtree(temporary_dir_path)
		return response

class FakeDownload(restful.Resource):
	def get(self):
		data_location = "/home/k/Downloads/Data/Economics/win_Economics.zip"
		f = open(data_location, "rb") 
		response = make_response(f.read())
		response.headers['Cache-Control'] = 'no-cache'
		response.headers["Content-Disposition"] = "attachment; filename=fake.zip"
		response.headers['content-length'] = str(os.path.getsize(data_location))               
		return response

class TestDownload(restful.Resource):

	def get(self):
		args = test_parser.parse_args()

		#for localhost
		data_location = "%s/%s/%s_%s.zip"%(PATH, module_name, user_os[:3], module_name)


		#This creates a temporary folder 
		temporary_dir_path = tempfile.mkdtemp() 

		

		#This is the whole path of the ebcrypted xip file in the temporary directory
		temporary_zip_file = "%s/%s_%s.zip"%(temporary_dir_path,  user_os[:3], module_name)

		#This creates the encrypted zip file on the location mentioned above
		subprocess.call(["7z", "a",  temporary_zip_file,  "-P%s"%args["password"] , data_location])
	
		#This reads the data from the temporary location present above
		f = open(temporary_zip_file, "r")
	
		response = make_response(f.read())
		response.headers['Cache-Control'] = 'no-cache'
		response.headers["Content-Disposition"] = "attachment; filename=%s_%s.zip"%(user_os[:3], module_name)
		response.headers['content-length'] = str(os.path.getsize(temporary_zip_file))               
		#This deletes the temporary encrypted zip file
		shutil.rmtree(dirpath)
		return response


class Unapproved(restful.Resource):
	def get(self):
		users = collection("users") 
		return jsonify({"result": [user for user in users.find({"approved": False}, fields={"_id": 0, "hash": 0, "mac_id": 0, "payment_receipt_image": 0})],
				"success": True,		
				"error": False,
				})


class ApproveUsers(restful.Resource):
	def get(self):
		users_collection = collection("users") 
		
		args = approved_users.parse_args()

		user_key = args["key"]

		print user_key
		
		if not users_collection.find_one({"key": user_key}):
				return 	{"error": True,
					"success": False,
					"error_code": 302,
					"messege": "The following users with key %s doesnt exists"%user_key,}

		try:
			users_collection.update({"key": user_key}, {"$set": {"approved": True}})
			user = users_collection.find_one({"key": user_key})
			connection.send_email("jindal.vikram@gmail.com", "eMetc Notification email", "Congratulations, Your request has been approved to use emetc %s module"%user["modules"], user["email_id"])
		except Exception as e:
			return 	{"error": True,
				"success": False,
				"error_code": 303,
				"messege": "The following error occurred  %s while processing user %s "%(e.__str__, user_key), }


		return 	{"error": False,
			"success": True,}
class cd:
        """Context manager for changing the current working directory"""
        def __init__(self, newPath):
                self.newPath = newPath

        def __enter__(self):
                self.savedPath = os.getcwd()
                os.chdir(self.newPath)

        def __exit__(self, etype, value, traceback):
                os.chdir(self.savedPath)
		

api.add_resource(RegisterUser, '/v1/register_user')
api.add_resource(GetFile, '/v1/download')
api.add_resource(TestDownload, '/v1/testdownload')
api.add_resource(ApproveUsers, '/v1/approved')
api.add_resource(Unapproved, '/v1/unapproved')
api.add_resource(FakeDownload, '/v1/fake')



if __name__ == '__main__':
    app.run(port=8000, debug=True)

