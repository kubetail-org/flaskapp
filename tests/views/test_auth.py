import re

from flaskapp.meta import mail
from flaskapp.models import User

from . import WebsiteTestCase, users


class AuthTests(WebsiteTestCase):
    def test_create_account(self):
        # test form page
        resp = self.client.get(self.url_for('auth.create_account'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<legend>Create a new account</legend>' \
                            in resp.data)
            
        email = users['userA']['email']
        passwd = users['userA']['password']
            
        # test bad email
        resp = self.create_account('barack', passwd)

        # test bad password confirmation
        resp = self.create_account(email, passwd, 'a')
        self.assertTrue('Passwords must match' in resp.data)

        # test good data
        resp = self.create_account(email, passwd, passwd)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers['Location'],
                         self.url_for('content.home'))
                
        resp = self.client.get(self.url_for('content.home'))
        self.assertTrue(email in resp.data)

    def test_logout(self):
        email = users['userA']['email']
        passwd = users['userA']['password']
        self.create_account(email, passwd, passwd)
                
        resp = self.client.get(self.url_for('content.home'))
        self.assertTrue(email in resp.data)

        resp = self.logout()
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(self.url_for('content.home'))
        self.assertFalse(email in resp.data)

    def test_login(self):
        # test form page
        resp = self.client.get(self.url_for('auth.login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('<legend>Log in to your account</legend>' \
                            in resp.data)

        email = users['userA']['email']
        passwd = users['userA']['password']

        # test invalid login
        resp = self.login(email, passwd)
        self.assertTrue('Email and password must match' in resp.data)

        # create account
        self.create_account(email, passwd)
        resp = self.client.get(self.url_for('content.home'))
        self.assertTrue(email in resp.data)

        self.logout()

        # test valid login
        resp = self.login(email, passwd)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers['Location'],
                         self.url_for('content.home'))

        resp = self.client.get(self.url_for('content.home'))
        self.assertTrue(email in resp.data)

    def test_forgot(self):
        email = users['userA']['email']
        passwd = users['userA']['password']
        self.create_account(email, passwd)
        self.logout()

        # test forgot form
        resp = self.client.get(self.url_for('auth.forgot'))
        self.assertTrue('<legend>Reset your password</legend>' in resp.data)

        # test bad submission
        data = dict(email='doesntexist@example.com')
        resp = self.client.post(self.url_for('auth.forgot'), data=data)
        self.assertTrue('not registered' in resp.data)

        # test good submission
        with mail.record_messages() as outbox:
            data = dict(email=email)
            resp = self.client.post(self.url_for('auth.forgot'), data=data)
            self.assertTrue('Success' in resp.data)
            self.assertEqual(len(outbox), 1)
            self.assertEqual(outbox[0].subject, 'Password Reset Request')

        # get reset url
        m = re.search('/auth/reset-password.*$', outbox[0].body)
        reset_url = m.group(0)

        # test that key works
        resp = self.client.get(reset_url)
        print resp.data
        self.assertTrue('Choose a new password' in resp.data)

    def test_reset_password(self):
        email = users['userA']['email']
        passwd = users['userA']['password']
        self.create_account(email, passwd)
        self.logout()

        # get reset url
        with mail.record_messages() as outbox:
            data = dict(email=email)
            resp = self.client.post(self.url_for('auth.forgot'), data=data)
            self.assertTrue('Success' in resp.data)
            self.assertEqual(len(outbox), 1)
            self.assertEqual(outbox[0].subject, 'Password Reset Request')

            m = re.search('/auth/reset-password.*$', outbox[0].body)
            reset_url = m.group(0)

        # test bad request
        resp = self.client.get(self.url_for('auth.reset_password'))
        self.assertTrue('Error' in resp.data)
        self.assertEqual(resp.status_code, 400)

        # test bad key
        u = self.url_for('auth.reset_password', key='badkey')
        resp = self.client.get(u)
        self.assertTrue('Error' in resp.data)

        # test good key, bad email
        u = re.sub('email=.*?&|$', '', reset_url) + '&email=bademail'
        resp = self.client.get(u)
        self.assertTrue('Error' in resp.data)

        # test good request
        resp = self.client.get(reset_url)        
        self.assertEqual(resp.status_code, 200)

        # test submission
        data = dict(password='newpasswd', password_confirm='newpasswd')
        resp = self.client.post(reset_url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('Success' in resp.data)

        # check that user is logged in
        resp = self.client.get('/')
        self.assertTrue(email in resp.data)

        # check that new password works
        self.logout()
        self.login(email, data['password'])
        resp = self.client.get('/')
        self.assertTrue(email in resp.data)

    def test_email_verification_request(self):
        email = users['userA']['email']
        passwd = users['userA']['password']
        self.create_account(email, passwd)

        # check user
        with self.app.app_context():
            u = User.query.filter(User.email == email).first()
            self.assertEqual(u.is_verified, False)

        # test form
        resp = self.client.get(self.url_for('auth.email_verification_request'))
        self.assertTrue('<legend>Send verification request</legend>' \
                            in resp.data)

        # test submission
        with mail.record_messages() as outbox:
            url = self.url_for('auth.email_verification_request')
            resp = self.client.post(url)
            self.assertTrue('Success' in resp.data)
            self.assertEqual(len(outbox), 1)
            self.assertEqual(outbox[0].subject,
                             'Flaskapp Account: Please Confirm Email')

        # get reset url
        m = re.search('/auth/verify-email.*$', outbox[0].body)
        verify_url = m.group(0)

        # test bad request
        resp = self.client.get(self.url_for('auth.verify_email'))
        self.assertTrue('Error' in resp.data)
        self.assertEqual(resp.status_code, 400)

        # test bad key
        u = self.url_for('auth.verify_email', key='badkey')
        resp = self.client.get(u)
        self.assertTrue('Error' in resp.data)

        # test good key, bad email
        verify_url2 = re.sub('email=.*?&', 'email=bademail&', verify_url)
        resp = self.client.get(verify_url2)
        self.assertTrue('Error' in resp.data)

        # test good request
        resp = self.client.get(verify_url)
        self.assertTrue('Your email has been verified' in resp.data)

        # check user
        with self.app.app_context():
            u = User.query.filter(User.email == email).first()
            self.assertEqual(u.is_verified, True)
