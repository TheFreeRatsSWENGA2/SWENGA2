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

    @patch('builtins.input', side_effect=['Math101'])  # Mock input to simulate user entering "Math101"
    @patch('App.Course.query')  # Mock the Course query
    @patch('App.Staff.query')  # Mock the Staff query
    def test_view_course_staff_any(self, mock_staff_query, mock_course_query, mock_input):
        # Define the course name and staff members directly in the test method
        course_name = "Math101"
        staff_members = [
            Staff(id=1, name="Alice Johnson", role="Professor"),
            Staff(id=2, name="Bob Smith", role="Lecturer"),
        ]

        # Create a mock course for the specified course name
        mock_course = Course(name=course_name)

        # Mock the return value for Course.query.filter_by
        mock_course_query.filter_by.return_value.first.return_value = mock_course

        # Create mock assignments for the specified staff members
        mock_assignments = [
            Assignment(course_name=course_name, staff_id=staff.id) for staff in staff_members
        ]
        # Assigning mock assignments to the course
        mock_course.assignments = mock_assignments
        
        # Mock Staff.query.get to return the appropriate staff members
        def side_effect_get(staff_id):
            return next((staff for staff in staff_members if staff.id == staff_id), None)

        mock_staff_query.get.side_effect = side_effect_get

        # Call the function for the specified course
        with patch('builtins.print') as mock_print:  # Mock print to capture output
            view_course_staff()

        # Assert that the output is as expected for the specified course
        mock_print.assert_any_call(f'Staff for Course {course_name}: ')
        for staff in staff_members:
            mock_print.assert_any_call(f'{staff.name} - {staff.role}')

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

