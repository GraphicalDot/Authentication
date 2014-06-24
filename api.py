#!/usr/bin/env python
#-*- coding: utf-8 -*-


from flask import Flask
from flask import request
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



# '/validate_token' arguments
zip_parser = reqparse.RequestParser()
zip_parser.add_argument('mac_id', type=str, required=True, location='form')
zip_parser.add_argument('key', type=str, required=True, location='form')
zip_parser.add_argument('path', type=str, required=True, location='form')
zip_parser.add_argument('check_module', type=str, required=False, location='form')



test_parser = reqparse.RequestParser()
test_parser.add_argument('password', type=str, required=True, location='form')


class RegisterUser(restful.Resource):

    def post(self):
		"""
		When a new user register to our website or form. He submits his/her detail throught this method
		Then this method calcualtes the hash of user_email, user_name, mac_id 
		
		the key which will be provided to the user will be the last 10 alphabets of the function.
		The hash function will be used to encrypt the zip file sent to the user

		"""
		args = reguser_parser.parse_args()
		print args
		users = collection("users")

		if not users.find_one({"email_id": args["email_id"], "mac_id": args["mac_id"], "modules": args["modules"]}):
		        args = reguser_parser.parse_args()
			users = collection("users")
			string = args.get("email_id").lower() + args.get("mac_id").lower() + args.get("first_name").lower() + args.get("modules")
			hash = hashlib.md5(string).hexdigest()
			key = hash[-10:]

			args["hash"] = hash
			args["key"] = key
			users.insert(args, safe=True)

			##TODO: send an email through ses
			return {
				"error": False,
				"success": True,
				"messege": "Registration has been completed",}
		
		return {
				"error": False,
				"success": True,
				"messege": "Registration has already been done"
				}



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
			if users.find_one({"key": args["key"], "mac_id": args["mac_id"]}):
				return {
					"success": True,
					"error": False,
					"module_name": users.find_one({"key": args["key"], "mac_id": args["mac_id"]})["modules"],
					"hash": users.find_one({"key": args["key"], "mac_id": args["mac_id"]})["hash"],}

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
		user_data = find_one({"key": args["key"]}, fields={"_id": 0})


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
		data_location = "/home/k/Downloads/Data/%s/%s_%s.zip"%(module_name, user_os[:3], module_name)


		#This creates a temporary folder 
		temporary_dir_path = tempfile.mkdtemp() 

		

		#This is the whole path of the ebcrypted xip file in the temporary directory
		temporary_zip_file = "%s/%s_%s.zip"%(temporary_dir_path,  user_os[:3], module_name)

		#This creates the encrypted zip file on the location mentioned above
		subprocess.call(["7z", "a",  temporary_zip_file,  "-P%s"%password , data_location])
	
		#This reads the data from the temporary location present above
		f = open(temporary_zip_file, "r")
	
		response = make_response(f.read())
		response.headers['Cache-Control'] = 'no-cache'
		response.headers["Content-Disposition"] = "attachment; filename=%s_%s.zip"%(user_os[:3], module_name)
		response.headers['content-length'] = str(os.path.getsize(temporary_zip_file))               
		#This deletes the temporary encrypted zip file
		shutil.rmtree(dirpath)

		return response

class TestDownload(restful.Resource):

	def get(self):
		args = test_parser.parse_args()

		#for localhost
		data_location = "/root/Cyclone2/Data/%s/%s_%s.zip"%(module_name, user_os[:3], module_name)


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
		response.headers['X-Accel-Redirect'] = temporary_zip_file
		#This deletes the temporary encrypted zip file
		shutil.rmtree(dirpath)


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



if __name__ == '__main__':
    app.run(port=8989, debug=True)

