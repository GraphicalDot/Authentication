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

app = Flask(__name__)
api = restful.Api(app)
# '/register_user' arguments parser
reguser_parser = reqparse.RequestParser()

reguser_parser.add_argument('mac_id', type=str, required=True, location='form')
reguser_parser.add_argument('user_name', type=str, required=True, location='form')
reguser_parser.add_argument('user_email', type=str, required=True, location='form')



reguser_parser.add_argument('auth_token', type=str, required=True, location='form')

# '/validate_token' arguments
zip_parser = reqparse.RequestParser()
zip_parser.add_argument('mac_id', type=str, required=True, location='form')
zip_parser.add_argument('key', type=str, required=True, location='form')
zip_parser.add_argument('path', type=str, required=True, location='form')


class RegisterUser(restful.Resource):

    def post(self):
		"""
		When a new user register to our website or form. He submits his/her detail throught this method
		Then this method calcualtes the hash of user_email, user_name, mac_id 
		
		the key which will be provided to the user will be the last 10 alphabets of the function.
		The hash function will be used to encrypt the zip file sent to the user

		"""

		if not users.find_one({"user_email": args["user_email"], "mac_id": args["mac_id"]}):
		        args = reguser_parser.parse_args()
			users = collection("users")
			string = "".join(args.keys())
			hash = hashlib.md5(string).hexdigest()
			key = hash[-10:]

			args["hash"] = hash
			args["key"] = key
			#collection.update(args. upsert= True)
			#send an email to the user with the key
			
			return {
					"error": False,
					"success": True}
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
		args = zip_parser.parse_args()
		print args
		print args["path"]
		print args["mac_id"]
		users = collection("users")
		print users

		if not users.find_one({"key": args["key"],}):
			if users.find_one({"mac_id": args["mac_id"]}):
				return {
					"error": True,
					"success": False,
					"error_code": 201,
					"messege": "The Key Entered is not valid",}
			else:
				return {
					"error": True,
					"success": False,
					"error_code": 202,
					"messege": "Please register for this file to run",}


		if not users.find_one({"key": args["key"], "mac_id": args["mac_id"]}):
			return {
					"error": True,
					"success": False,
					"error_code": 203,
					"messege": "Same key cannot be used on two Computers",}

		
		if args["path"]:
			return{
					"error": False,
					"success": True,
					"hash": users.find_one({"key": args["key"]}, fields={"_id": 0, "hash": 1})["hash"]
				}


		print "\n\n Now the file is being transfffered"
		password = users.find_one({"key": "a637b99e8e"}, fields={"_id": 0, "hash": 1})["hash"]
		#This creates a temporary folder 
		dirpath = tempfile.mkdtemp() 

		#This gets the location where the data is present 
		
		#for remote server
		#data_location = "/root/Cyclone2/CycloneData/Whole.zip"

		#for localhost
		data_location = "/home/k/Downloads/Atest/Whole.zip"

		#This is the whole path of the ebcrypted xip file in the temporary directory
		temporary_zip_file = "%s/temporary.zip"%dirpath

		#This creates the encrypted zip file on the location mentioned above
		subprocess.call(["7z", "a",  temporary_zip_file,  "-P%s"%password , data_location])
	
		#This reads the data from the temporary location present above
		f = open(temporary_zip_file, "r")
	
		response = make_response(f.read())
		response.headers["Content-Disposition"] = "attachment; filename=whole.zip"
                
		#This deletes the temporary encrypted zip file
		#shutil.rmtree(dirpath)

		return response


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



if __name__ == '__main__':
    app.run(port=8989, debug=True)

