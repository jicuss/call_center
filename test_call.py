import unittest
import mock

from call_center import *
import pdb

class CallTests(unittest.TestCase):
    def setUp(self):
        self.mock_call_handler = mock.create_autospec(CallHandler)
        self.mock_employee = mock.create_autospec(Employee)
        self.call_instance = Call(self.mock_call_handler)
        self.mock_employee.rank = 0

    def tearDown(self):
        """
        This method is called after each test
        """
        pass

    def test_set_employee_handler_of_current_rank_or_higher(self):
        self.assertTrue(self.call_instance.set_employee_handler(self.mock_employee),msg='must be able to be associated with a call handler')
        self.call_instance.employee_handler = None # reset call employee

        self.mock_employee.rank = 1
        self.assertTrue(self.call_instance.set_employee_handler(self.mock_employee),msg='must be able to be associated with a call handler greater than its own rank')
        return True

    def test_set_call_handler_below_rank(self):
        '''
            must be not able to be associated with a call handler of lower rank
        '''
        self.call_instance.rank = 1
        self.assertRaises(StandardError, lambda: self.call_instance.set_employee_handler(self.mock_employee))
        return True

    def test_set_call_busy_handler(self):
        '''  must be not able to be associated with a busy call handler '''
        self.mock_employee.is_free.return_value = False
        self.assertRaises(StandardError, lambda: self.call_instance.set_employee_handler(self.mock_employee))
        return True

    def test_assign_to_free_employee(self):
        self.mock_call_handler.dispatch_call.return_value = True
        self.assertTrue(self.call_instance.assign_to_free_employee(),msg='must be capable of being assigned to free employee')
        return True

    def test_assign_to_employee_when_already_assigned(self):
        '''  must be not able to be associated with a new employee if call is already being handled '''
        self.call_instance.set_employee_handler(self.mock_employee)
        self.assertRaises(StandardError, lambda: self.call_instance.set_employee_handler(self.mock_employee))
        return True

    def test_assign_to_free_employee_when_none_available(self):
        ''' when all employees are available, place call in queue '''
        self.mock_call_handler.dispatch_call.return_value = False
        self.assertFalse(self.call_instance.assign_to_free_employee(),msg='if no free employees are available, add call to queue')
        return True

    def test_in_queue(self):
        self.mock_call_handler.call_queue = [self.call_instance]
        self.assertTrue(self.call_instance.in_queue(),msg='must return true when call is in queue')
        self.mock_call_handler.call_queue = []
        self.assertFalse(self.call_instance.in_queue(),msg='must return false when call is not in queue')
        return True

    def test_being_helped(self):
        self.call_instance.employee_handler = None
        self.assertFalse(self.call_instance.being_helped(),msg='must return false when not being associated with employee')
        self.call_instance.employee_handler = self.mock_employee
        self.assertTrue(self.call_instance.being_helped(),msg='must return true when being associated with employee')
        return True

if __name__ == '__main__':
    unittest.main()


