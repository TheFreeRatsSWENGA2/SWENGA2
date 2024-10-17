import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from unittest.mock import patch, MagicMock

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class CourseUnitTests(unittest.TestCase):

    @patch('builtins.input', side_effect=["Math101"])
    def test_create_course(self, mock_input):
        course = create_course()
        self.assertEqual(course.name, "Math101")

    @patch('App.Course.query')
    def test_list_courses(self, mock_query):

        mock_query.all.return_value = [
            Course(name="Math101"),
            Course(name="Physics202"),
        ]

        courses = list_courses()

        self.assertEqual(len(courses), 2)
        self.assertEqual(courses[0].name, "Math101")
        self.assertEqual(courses[1].name, "Physics202")

    @patch('App.models.Course.query.filter_by')  # Adjusted to mock filter_by
    @patch('App.models.Staff.query.get')
    @patch('builtins.input', side_effect=['Math101'])
    def test_view_course_staff(self, mock_input, mock_staff_get, mock_course_filter_by):
        # Mock Course object with assignments
        mock_course = MagicMock(name="Math101")
        mock_course.assignments = [MagicMock(staff_id=1), MagicMock(staff_id=2)]
        mock_course_filter_by.return_value.first.return_value = mock_course

        # Mock Staff objects
        mock_staff_get.side_effect = [
            MagicMock(name="John Doe", role="Lecturer"),
            MagicMock(name="Jane Smith", role="TA")
        ]

        # Mock print
        with patch('builtins.print') as mock_print:
            view_course_staff()

        # Assertions
        mock_course_filter_by.assert_called_once_with(name='Math101')
        mock_staff_get.assert_any_call(1)
        mock_staff_get.assert_any_call(2)

        # Check print output
        mock_print.assert_any_call('Staff for Course Math101: ')
        mock_print.assert_any_call('John Doe - Lecturer')
        mock_print.assert_any_call('Jane Smith - TA')



'''
    Integration Tests
'''
# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

