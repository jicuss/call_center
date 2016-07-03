import unittest
import mock

from call_center import *
import pdb

''' TODO: Add some comments to this '''

class EmployeeTests(unittest.TestCase):
    def setUp(self):
        self.mock_call_handler = mock.create_autospec(CallHandler)
        self.mock_call = mock.create_autospec(Call)
        self.employee = Employee(self.mock_call_handler,'employee')

    def tearDown(self):
        """
        This method is called after each test
        """
        pass

    def test_set_employee_type_verify_rank(self):
        self.employee.set_employee_type('employee')
        self.assertEqual(self.employee.rank,0,'Base Employee should have rank 0')
        self.employee.set_employee_type('manager')
        self.assertEqual(self.employee.rank,1,'Manager should have rank 1')
        self.employee.set_employee_type('director')
        self.assertEqual(self.employee.rank,2,'Director should have rank 2')
        return True

    def test_set_employee_type_verify_type_validity(self):
        ''' If an invalid employee type is passed to set_employee_type should raise error '''
        self.assertRaises(ValueError,lambda: self.employee.set_employee_type('bogus'))
        return True

    def test_recieve_call_when_free(self):
        self.assertTrue(self.employee.recieve_call(self.mock_call))
        return True

    def test_recieve_call_when_not_free(self):
        self.employee.recieve_call(self.mock_call)
        self.assertRaises(StandardError,lambda: self.employee.recieve_call(self.mock_call))
        return True

    def test_complete_call_when_not_free(self):
        self.employee.recieve_call(self.mock_call)
        self.assertTrue(self.employee.complete_call())
        return True

    def test_complete_call_when_free(self):
        self.assertRaises(NameError,lambda: self.employee.complete_call())
        return True

    def test_escalate_and_reassign(self):
        self.employee.recieve_call(self.mock_call)
        self.mock_call_handler.request_call_from_queue.return_value = self.mock_call
        self.assertTrue(self.employee.escalate_and_reassign())
        self.assertEqual(self.employee.call,self.mock_call)
        self.mock_call.increase_rank.assert_called_with()
        self.mock_call.assign_to_free_employee.assert_called_with()
        return True

    def test_assign_new_call(self):
        self.mock_call_handler.request_call_from_queue.return_value = self.mock_call
        self.employee.assign_new_call()
        self.mock_call_handler.request_call_from_queue.assert_called_with(self.employee.rank)
        self.mock_call.set_employee_handler.assert_called_with(self.employee)
        return True

    def test_is_free(self):
        self.assertTrue(self.employee.is_free())
        self.employee.assign_new_call(self.mock_call)
        self.assertFalse(self.employee.is_free())
        return True



if __name__ == '__main__':
    unittest.main()

