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


app = Flask(__name__)
api = restful.Api(app)
# '/register_user' arguments parser
reguser_parser = reqparse.RequestParser()
reguser_parser.add_argument('mac_id', type=str, required=True, location='form')
reguser_parser.add_argument('auth_token', type=str, required=True, location='form')

# '/validate_token' arguments
zip_parser = reqparse.RequestParser()
zip_parser.add_argument('mac_id', type=str, required=True, location='form')
zip_parser.add_argument('auth_token', type=str, required=True, location='form')
zip_parser.add_argument('path', type=str, required=True, location='form')


class RegisterUser(restful.Resource):

    def post(self):
        """	
        Returns a success if the user already exists on the system or creates 
        a new user and then returns success. 

        Returns an error in the case of an invalid access token or in case there
        was a problem during the creation of a user.
        """

        args = reguser_parser.parse_args()

	"""
        # create the user instance
        try:
            user = User(args['fb_user_id'], args['fb_access_token'])
            user.updating_gcm(args['fb_user_id'], args['gcm_registration_id'])
        # fb access token is invalid
        except AccessTokenInvalidError as e:
            if e.code is 2:
				return {
					"error": True,
					"error_code": 1221,
					"error_message": "Facebook access token is not valid.",
					"success": False
						}
            if e.code is 1:
				return {
					"error": True,
					"error_code": 1222,
					"error_message": "Facebook User ID does not match with the given access token.",
					"success": False
						}

        # create a new user if it doesn't exist in the DB
        except UserDoesNotExistError:
            # TODO: Handle 'UserCreationError' later.
            User.create(args['fb_user_id'], args['fb_access_token'], args['gcm_registration_id'])
            return {
                "error": False,
                "success": True,
                "new_registration": True
                    }

        # the user exists and the access token & user id provided were valid
        return {
            "error": False,
            "success": True,
            "new_registration": False,
            }
	"""
	print args["mac_id"]
	return

class GetFile(restful.Resource):

    def get(self):
		"""
		Returns the friends of the logged in user against whom he has
		taken no action yet on basis of the given skip and limit arguments.
		"""
		args = zip_parser.parse_args()
		print args
		print args["path"]
		print args["mac_id"]
		users = collection("users")
		print users

		if not users.find_one({"key": args["auth_token"],}):
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


		if not users.find_one({"key": args["auth_token"], "mac_id": args["mac_id"]}):
			return {
					"error": True,
					"success": False,
					"error_code": 203,
					"messege": "Same key cannot be used on two Computers",}

		
		if args["path"]:
			return{
					"error": False,
					"success": True,
					"key": users.find_one({"key": "a637b99e8e"}, fields={"_id": 0, "hash": 1})["hash"]
				}
	
		file_name = "/home/k/Downloads/Atest/whole.zip"
		f = open(file_name, "r")
		response = make_response(f.read())
		response.headers["Content-Disposition"] = "attachment; filename=whole.zip"
		return response
		

api.add_resource(RegisterUser, '/v1/register_user')
api.add_resource(GetFile, '/v1/download')



if __name__ == '__main__':
    app.run(port=8989, debug=True)

