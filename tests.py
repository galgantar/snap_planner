import unittest
import main

class Test(unittest.TestCase):
    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def tearDown(self):
        main.app.testing = False

    def testLoading(self):
        response = self.app.get("/")
        assert response.status_code == 302

    def testRegister(self):
        get_response = self.app.get("/register")
        assert get_response.status_code == 200

    def testLogin(self):
        get_response = self.app.get("/login")
        assert get_response.status_code == 200

        post_response = self.app.post("/login", data={"email" : "test.test@gmail.com", "password" : "a"})
        assert b"Wrong username or password" in post_response.data

    def testLogout(self):
        response = self.app.get("/")
        assert response.status_code == 302

    def testDatabaseList(self):
        response = self.app.get("/database")
        assert response.status_code == 302

    def testProfile(self):
        response = self.app.get("/profile")
        assert response.status_code == 302

        post_response = self.app.post("/profile")
        assert post_response.status_code == 302

    def testConfirmation(self):
        response = self.app.get("/confirmation")
        assert response.status_code == 302

        response = self.app.get("/confirmation/test")
        assert  response.status_code == 200

    def testResend(self):
        response = self.app.get("/resend")
        assert response.status_code == 302

    def testPassword(self):
        response = self.app.get("/password")
        assert response.status_code == 200

        post_response = self.app.post("/password", data={"email":"test.test@gmail.com"})
        assert post_response.status_code == 302

    def testPasswordCode(self):
        response = self.app.get("/password/test?email=test.test<at>gmail.com")
        assert response.status_code == 302

        post_response = self.app.post("/password/test?email=test.test<at>gmail.com", data={"password1":"123", "password2":"123"})
        assert response.status_code == 302

    def testTimetablesListing(self):
        response = self.app.get("/timetables")
        assert response.status_code == 302

    def testTimetableAdd(self):
        response = self.app.get("/timetables/new")
        assert response.status_code == 302

        post_response = self.app.post("/timetables/new", data={"name":"test", "day":"wed"})
        assert post_response.status_code == 302

    def testTimetable(self):
        response = self.app.get("/timetable/never_used_name")
        assert response.status_code == 302

        post_response = self.app.get("/timetable/never_used_name")
        assert post_response.status_code == 302

    def testMyDates(self):
        response = self.app.get("/mydates")
        assert response.status_code == 302

unittest.main()
