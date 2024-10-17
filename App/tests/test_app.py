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
        course1 = Course(name="Math101")
        course2 = Course(name="Physics101")
        mock_query.all.return_value = [
            course1, course2
        ]

        courses = list_courses()
        self.assertEqual(course1.name, "Math101")
        self.assertEqual(course2.name, "Physics101")

    @patch('builtins.input', side_effect=['Math101']) 
    @patch('App.Course.query')  
    @patch('App.Staff.query') 
    def test_view_course_staff(self, mock_staff_query, mock_course_query, mock_input):
        
        course_name = "Math101"
        staff_members = [
            Staff(id=1, name="Alice Johnson", role="Professor"),
            Staff(id=2, name="Bob Smith", role="TA"),
        ]

        mock_course = Course(name=course_name)
        mock_course_query.filter_by.return_value.first.return_value = mock_course

        mock_assignments = [
            Assignment(course_name=course_name, staff_id=staff.id) for staff in staff_members
        ]
        mock_course.assignments = mock_assignments
        
        def side_effect_get(staff_id):
            return next((staff for staff in staff_members if staff.id == staff_id), None)

        mock_staff_query.get.side_effect = side_effect_get

        with patch('builtins.print') as mock_print: 
            view_course_staff()

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
        user = create_user("rick", "bobpass")
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

class CourseIntegrationTests(unittest.TestCase):

    @patch('builtins.input', side_effect=['Math101', 'Math101'])
    def test_create_course(self, mock_input):
        course = create_course()
        courseGet = get_course()
        self.assertEqual(courseGet.name, "Math101")

    @patch('builtins.input', side_effect=['MATH101', 'Raul Menendez', 'Head Lecturer', 'PHYS101', 'MATH101', '1'])
    def test_assign_staff(self, mock_input):
        course = create_course()
        staff = create_staff()
        newStaff = assign_staff()
        self.assertEqual(newStaff.course_name, 'MATH101')
        self.assertEqual(newStaff.staff_id, 1)