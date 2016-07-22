import unittest
import mock

from call_center import *
import pdb

class CallCallHandler(unittest.TestCase):
    def setUp(self):
        self.call_handler = CallHandler()
        self.mock_employee = mock.create_autospec(Employee)
        self.mock_call = mock.create_autospec(Call)

        self.mock_employee.rank = 0
        self.mock_call.rank = 0
        self.mock_call.resolved = False

    def tearDown(self):
        """
        This method is called after each test
        """
        pass

    def test_add_employee(self):
        self.call_handler.add_employee(self.mock_employee)
        self.assertEqual(self.call_handler.employees,[self.mock_employee])
        return True

    def test_locate_handler_for_call(self):
        self.call_handler.add_employee(self.mock_employee)
        self.assertEqual(self.call_handler.locate_handler_for_call(0), self.mock_employee,msg='must be able to find employee if available')
        return True

    def test_locate_handler_for_call_when_no_employees_of_low_rank_available(self):
        ''' increase the rank of the only available employee, the locate_handler_for_call should not return an employee '''
        self.call_handler.add_employee(self.mock_employee)
        self.mock_employee.rank = 1
        self.assertFalse(self.call_handler.locate_handler_for_call(0),msg='must be able to find employee none available at current rank')
        ''' the locate_handler_for_call should return an employee if the rank of the call is 1 '''
        self.assertEqual(self.call_handler.locate_handler_for_call(1),self.mock_employee,msg='must be able to find employee when available')
        return True

    def test_locate_handler_for_call_when_none_available(self):
        self.call_handler.add_employee(self.mock_employee)
        self.mock_employee.is_free.return_value = False
        self.assertFalse(self.call_handler.locate_handler_for_call(1),msg='must be able to find employee none available at current rank')
        return True

    def test_dispatch_call_when_employee_available(self):
        self.call_handler.add_employee(self.mock_employee)
        self.assertEqual(self.call_handler.dispatch_call(self.mock_call),self.mock_employee)
        return True

    def test_dispatch_call_when_no_employee_available(self):
        self.assertFalse(self.call_handler.dispatch_call(self.mock_call))
        self.assertEqual(self.call_handler.call_queue,[self.mock_call])
        return True

    def test_request_call_from_queue(self):
        '''
        should not return a disconnected call, a call being handled, or a call above the rank
        '''
        self.call_handler.call_queue = [self.mock_call]
        self.mock_call.being_helped.return_value = False
        self.assertEqual(self.call_handler.request_call_from_queue(0),self.mock_call)
        return True

    def test_request_call_from_queue_when_none_available(self):
        self.call_handler.call_queue = [self.mock_call]
        self.mock_call.rank = 1
        self.assertFalse(self.call_handler.request_call_from_queue(0))
        return True

    def test_request_call_from_queue_when_call_disconnected(self):
        self.call_handler.call_queue = [self.mock_call]
        self.mock_call.resolved = True
        self.assertFalse(self.call_handler.request_call_from_queue(0))
        return True

    def test_request_call_from_queue_when_all_calls_being_handled(self):
        self.call_handler.call_queue = [self.mock_call]
        self.mock_call.being_helped.return_value = True
        self.assertFalse(self.call_handler.request_call_from_queue(0))
        return True

    def test_remove_call_from_queue(self):
        self.call_handler.call_queue = [self.mock_call]

        self.mock_call.resolved = False
        self.call_handler.remove_call_from_queue(self.mock_call)
        self.assertEquals(self.call_handler.call_queue,[self.mock_call],msg = 'Must not be able to remove an unresolved call from queue')

        self.mock_call.resolved = True
        self.call_handler.remove_call_from_queue(self.mock_call)
        self.assertEquals(self.call_handler.call_queue,[],msg = 'Must be able to remove resolved call from queue')

if __name__ == '__main__':
    unittest.main()

