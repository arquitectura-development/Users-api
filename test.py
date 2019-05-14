import json
import unittest
from application import application

class FlaskTestCase(unittest.TestCase):
    #Checking if the application is alive and status_code=200
    def test_upload(self):
        tester = application.test_client(self)
        response = tester.get('/', content_type='html/text')
        assert response.status_code == 200

    #Sign Up-Email already exist: User must not be created and status_code=409
    def test_signup_email_inuse(self):
        tester = application.test_client(self)
        data = {'email':'admin@admin.com', 'name':'Admin'}
        response = tester.post('/users/signup', data= json.dumps(data),content_type='application/json',
                              follow_redirects=True)
        assert response.status_code == 409

    #Sign Up-Email is not defined in post: User must not be created and status_code=400
    def test_signup_incompletepost_1(self):
        tester = application.test_client(self)
        data = {'name':'Admin'}
        response = tester.post('/users/signup', data=json.dumps(data), content_type='application/json',
                                        follow_redirects=True)
        assert response.status_code == 400

    #Sign Up-Name is not defined in post: User must not be created and status_code=400
    def test_signup_incompletepost_2(self):
        tester = application.test_client(self)
        data = {'email':'joyce8787@gmail.com'}
        response = tester.post('/users/signup', data=json.dumps(data), content_type='application/json',
            follow_redirects=True)
        assert response.status_code == 400

    #Sign Up-Email field exist but is empty: User must not be created and status_code=400
    def test_signup_incompletepost_3(self):
        tester = application.test_client(self)
        data = {'email':'', 'name':'Joyce'}
        response = tester.post('/users/signup', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 400

    #Sign Up-Name field exist but is empty: User must not be created and status_code=400
    def test_signup_incompletepost_4(self):
        tester = application.test_client(self)
        data = {'email':'joyce8787@gmail.com', 'name':''}
        response = tester.post('/users/signup', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 400

    #Sign Up-API doesn't receive a JSON: User must not be created and status_code=400
    def test_signup_incompletepost_5(self):
        tester = application.test_client(self)
        response = tester.post('/users/signup',data=dict(email="joyce8787@gmail.com", name="Joyce"),
                follow_redirects=True)
        assert response.status_code == 400

    #Sign Up-For a success event and status_code=200
    def test_signup_success(self):
        tester = application.test_client(self)
        data = {'email':'edgar25@gmail.com', 'name':'Edgar'}
        response = tester.post('/users/signup', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 201

    #Login-Email doesn't exist in the database: No login and status_code= 404
    def test_signin_emailnoindb(self):
        tester = application.test_client(self)
        data = {'email':'joyce8787@gmail.com'}
        response = tester.post('/users/login', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 404

    #Login-Email is not defined in Json: No login and status_code= 404
    def test_signin_noemail(self):
        tester = application.test_client(self)
        data = {'email':'joyce8787@gmail.com'}
        response = tester.post('/users/login', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 404

    #Login-Email is empty in the Json post: No login and status_code= 404
    def test_signin_emptyemail(self):
        tester = application.test_client(self)
        data = {'email':''}
        response = tester.post('/users/login', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 400

    #Login-For a success event and status_code=200
    def test_signin_success(self):
        tester = application.test_client(self)
        data = {'email':'admin@admin.com'}
        response = tester.post('/users/login', data=json.dumps(data), content_type='application/json',
                follow_redirects=True)
        assert response.status_code == 200

    #Search a user by id from not Admin: status_code=401
    def test_adminsearch_notadmin(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?userId=1&searchUserId=1', content_type='html/text')
        assert response.status_code == 401

    #Search a non existent user by id from Admin: status_code=404
    def test_adminsearch_notuserindb(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?userId=0&searchUserId=40', content_type='html/text')
        assert response.status_code == 404

    #Search a user without Admin id defined: status_code=401
    def test_adminsearch_notadmin_1(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?searchUserId=40', content_type='html/text')
        assert response.status_code == 401

    #Search a user with empty Admin id: status_code=401
    def test_adminsearch_notadmin_2(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?userId=&searchUserId=40', content_type='html/text')
        assert response.status_code == 401

    #Search a user without User id defined: status_code=404
    def test_adminsearch_notuser_1(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?userId=0', content_type='html/text')
        assert response.status_code == 404

    #Search a user with empty User id: status_code=404
    def test_adminsearch_notuser_2(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?userId=0&searchUser=', content_type='html/text')
        assert response.status_code == 404

    #Search a user by id from being Admin: status_code= 200
    def test_adminsearch(self):
        tester = application.test_client(self)
        response = tester.get('/admin/users/name?userId=0&searchUserId=1', content_type='html/text')
        assert response.status_code == 200

    #Search if a user exists and the user is not defined: status_code=404
    def test_usersearch1(self):
        tester = application.test_client(self)
        response = tester.get('/users/auth', content_type='html/text')
        assert response.status_code == 404

    #Search if a user exists and the user is empty: status_code=404
    def test_usersearch2(self):
        tester = application.test_client(self)
        response = tester.get('/users/auth?userId=', content_type='html/text')
        assert response.status_code == 404

    #Search if a user exists and the user don't exist: status_code=404
    def test_usersearch3(self):
        tester = application.test_client(self)
        response = tester.get('/users/auth?userId=509', content_type='html/text')
        assert response.status_code == 404

    #Search if a user exists and the user exists:status_code=200
    def test_usersearch(self):
        tester = application.test_client(self)
        response = tester.get('/users/auth?userId=0', content_type='html/text')
        assert response.status_code == 200

    #Delete a user that doesn't exists: status_code=404
    def test_userdelete1(self):
        tester = application.test_client(self)
        response = tester.delete('/users/delete?userId=900', content_type='html/text')
        assert response.status_code == 404

    #Delete a non specified user: status_code = 400
    def test_userdelete2(self):
        tester = application.test_client(self)
        response = tester.delete('/users/delete', content_type='html/text')
        assert response.status_code == 404

    #Delete an empty user: status_code = 400
    def test_userdelete3(self):
        tester = application.test_client(self)
        response = tester.delete('/users/delete?userId=', content_type='html/text')
        assert response.status_code == 404

    #Delete the admin: status_code = 403
    def test_userdelete4(self):
        tester = application.test_client(self)
        response = tester.delete('/users/delete?userId=0', content_type='html/text')
        assert response.status_code == 403

    #Delete a user that exists in the database: status_code=200
    def test_userdelete(self):
        tester = application.test_client(self)
        response = tester.delete('/users/delete?userId=1', content_type='html/text')
        assert response.status_code == 200





if __name__ == '__main__':
    unittest.main()
