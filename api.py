#!/usr/bin/env python
#-*- coding: utf-8 -*-


from flask import Flask
from flask import request
from flask.ext import restful
from flask.ext.restful import reqparse

app = Flask(__name__)
api = restful.Api(app)
# '/register_user' arguments parser
reguser_parser = reqparse.RequestParser()
reguser_parser.add_argument('mac_id', type=str, required=True, location='form')
reguser_parser.add_argument('access_token', type=str, required=True, location='form')

# '/validate_token' arguments
token_parser = reqparse.RequestParser()
token_parser.add_argument('access_token', type=str, required=True, location='form')


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

class GetOpenFriends(restful.Resource):

    def get(self):
        """
        Returns the friends of the logged in user against whom he has
        taken no action yet on basis of the given skip and limit arguments.
        """

        args = opfrnds_parser.parse_args()

        args = opfrnds_parser.parse_args()
		
        # user object
        auth= request.authorization
        user= User(fb_user_id=auth.username, fb_access_token=auth.password, check_token_validity=False)

        # get oepn friends of the user
        try:
            open_friends = user.get_open_friends(skip=args['skip'], limit=args['limit'])
		
		# there are no open friends

        except NoMoreFriendsToFetchError as e:
            return {
                'error': True,
                'error_code': 2221,	
                'error_message': e.__str__(),
            }
        # the list of open friends was pulled successfully
        else:
            return {
                'error': False,
                'skip': args['skip'],
                'limit': args['limit'],
                'results': open_friends
                    }




api.add_resource(RegisterUser, '/v1/register_user')
api.add_resource(GetOpenFriends, '/v1/validate_user')



if __name__ == '__main__':
    app.run(port=8989, debug=True)

