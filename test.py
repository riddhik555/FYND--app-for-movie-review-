from app import app
import unittest


class FlaskTest (unittest.TestCase):
    
    #check for response 500
    def test_index(self):
        tester=app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode , 200)

    def test2_login_check(self):
        tester=app.test_client(self)
        response = tester.post('/login' ,data=dict(username ="admin" , password = "admin"),
        follow_redirects=True)
        self.assertTrue(b'Welcome' in response.data)

    def test3_incorrect_login(self):
        tester=app.test_client(self)
        response = tester.post('/login' ,data=dict(username ="wrong" , password = "admin"),
        follow_redirects=True)
        self.assertTrue(b'Invalid User' in response.data)

    def test4_admin_access(self):
        tester=app.test_client(self)
        response = tester.post('/login' ,data=dict(username ="admin" , password = "admin"),
        follow_redirects=True)
        self.assertTrue(b'Edit' in response.data)
        self.assertTrue(b'Delete' in response.data)
        self.assertTrue(b'Add Review' in response.data)

    def test5_user_access(self):
        tester=app.test_client(self)
        response = tester.post('/login' ,data=dict(username ="akash" , password = "akash"),
        follow_redirects=True)
        self.assertFalse(b'Edit' in response.data)
        self.assertFalse(b'Delete' in response.data)
        self.assertFalse(b'Add Review' in response.data)

    def test6_detail_view(self):
        tester=app.test_client(self)
        response = tester.post('/login' ,data=dict(username ="akash" , password = "akash"),
        follow_redirects=True)
        response1 = tester.get('/1' ,content_type='html/text')
        self.assertTrue(b'Details' in response1.data)

    def test7_add_new_review(self):
        tester=app.test_client(self)
        response = tester.post('/login' ,data=dict(username ="admin" , password = "admin"),
        follow_redirects=True)
        response1 = tester.get('/new' ,content_type='html/text')
        self.assertTrue(b'new review' in response1.data)

    def test8_logout(self):
        tester=app.test_client(self)
        response1 = tester.get('/dropsession' ,content_type='html/text')
        self.assertTrue(b'New User' in response1.data)

    def test9_new_user(self):
        tester=app.test_client(self)
        response = tester.get('/register' ,content_type='html/text')
        self.assertTrue(b'Personal Information' in response.data)
        self.assertTrue(b'First Name' in response.data)
        self.assertTrue(b'Last Name' in response.data)
        self.assertTrue(b'Email' in response.data)

    
if __name__==  "__main__":
    unittest.main()
