####################################################################
# Original Source of Problem: Cracking the Coding Interview.
# Call Center Question. PG 127
# Objective: Imagine you want to make a call routing service
# There are three levels of employees: respondent, manager, and director
# if one of the employees is unable to respond to  call, escalate the call to the next higher level of employee
# if all employees are currently busy, place call in queue

class CallHandler:
    '''
    The main class. Handles the associating employees with calls, redirecting calls to a queue if employee is unavailable
    '''

    def __init__(self):
        self.employee_types = ["employee", "manager", "director"]
        self.call_queue = []
        self.employees = []

    def add_employee(self, employee):
        if isinstance(employee, Employee):
            self.employees.append(employee)
        else:
            raise TypeError, 'Must be a valid employee to be added to call handler'

    def locate_handler_for_call(self, rank):
        '''
        Get the first handler available who can handle the call of a specific rank
        '''

        if type(rank) is not int:
            raise TypeError, 'Rank must be an integer'

        ''' might want to rework this, it should stop after finding first available employee '''
        available_employees = filter(lambda x: x.is_free() and x.rank == rank, self.employees)
        if len(available_employees) > 0:
            return available_employees[0]

    def dispatch_call(self, call):
        '''
        routes the call to an available employee of appropriate rank, otherwise places call in a queue if no one is available
        '''

        if isinstance(call, Call):
            if call.resolved:
                return False
            emp = self.locate_handler_for_call(call.rank)
            if emp:
                emp.assign_new_call(call)
                return emp
            else:
                if call not in self.call_queue:
                    self.call_queue.append(call)
                    return False
        else:
            raise TypeError, 'Only valid calls can be dispatched'

    def request_call_from_queue(self, rank):
        '''
        return any available calls that are queued at the rank specified
        '''
        if type(rank) is not int:
            raise TypeError, 'rank must be an integer'

        queued_calls = filter(lambda x: x.rank == rank and x.resolved != True and x.being_helped() != True, self.call_queue)
        if len(queued_calls) > 0:
            return queued_calls[0]

    def remove_call_from_queue(self, call):
        if call.resolved:
            self.call_queue.remove(call)

class Call:
    '''
    rank - the minimum level of an employee who can handle the call
    employee - the employee handling the call
    resolved - has the issue been resolved by an employee?
    '''

    def __init__(self, call_handler):
        self.rank = 0
        self.employee_handler = None
        self.set_call_handler(call_handler)
        self.resolved = False

    def set_call_handler(self, call_handler):
        ''' associate with call handler queue return true if successful '''

        if isinstance(call_handler, CallHandler):
            self.call_handler = call_handler
            return True
        else:
            raise TypeError, 'call handler queue can only handle valid calls'

    def set_employee_handler(self, employee):
        '''
        associate with an employee of the call center
        if the employee is of rank below the rank of the call, raise error
        if the employee is of rank >= rank of call, return True
        '''
        if not self.being_helped():
            if isinstance(employee, Employee) and employee.is_free():
                if employee.rank >= self.rank:
                    self.employee_handler = employee
                    return True
                else:
                    raise TypeError, 'call must be handled by an employee of >= rank'
            else:
                raise TypeError, 'call must be handled by a free employee'
        else:
            raise StandardError, 'can only be handle by one employee at a time.'

    def assign_to_free_employee(self):
        '''
        make an attempt to associate call with any available call center employee.
        if none available, place in queue
        '''
        employee = self.call_handler.dispatch_call(self)
        if employee:
            return True

    def in_queue(self):
        '''  am I currently in a queue? '''
        if self in self.call_handler.call_queue:
            return True

    def being_helped(self):
        '''  am I currently being helped by a call center employee? '''
        if self.employee_handler is not None:
            return True

    def in_queue_or_being_helped(self):
        if self.in_queue() or self.being_helped():
            return True

    def increase_rank(self):
        self.rank += 1
        return self.rank

    def disconnect(self):
        self.resolved = True
        self.call_handler.remove_call_from_queue(self)


class Employee:
    def __init__(self, call_handler, employee_type='employee'):
        self.set_call_handler(call_handler)
        self.set_employee_type(employee_type)
        self.call = None

    def set_call_handler(self, call_handler):
        if isinstance(call_handler, CallHandler):
            self.call_handler = call_handler
            self.call_handler.add_employee(self)
        else:
            raise TypeError('must be associated with a valid call handler')

    def set_employee_type(self, employee_type):
        employee_types = ["employee", "manager", "director"]
        if employee_type in employee_types:
            for i, j in enumerate(employee_types):
                if j == employee_type:
                    self.rank = i
        else:
            raise ValueError('Rank of employee must in ["employee", "manager", "director"]')

    def recieve_call(self, call):
        if self.is_free():
            if isinstance(call, Call):
                self.call = call
                return True
            else:
                raise TypeError, 'recieve_call method only accepts instances of a Call class'
        else:
            raise StandardError, 'can only be on one call at a time'

    def complete_call(self):
        '''
        disconnect the current call, set current call to null
        if no current call if available, raise error
        '''
        if not self.is_free():
            self.call.disconnect()
            self.call = None
            return True
        else:
            raise NameError, 'Instance not currently associated with a valid call'

    def escalate_and_reassign(self):
        '''
            escalate the level of the current call, grab a new call from the queue
        '''
        if not self.is_free():
            self.call.increase_rank()
            self.call.assign_to_free_employee()
            self.call = None
            self.assign_new_call()
            return True
        else:
            raise NameError, 'Instance not currently associated with a valid call'

    def assign_new_call(self, call=None):
        '''
            grab a new call from the queue at my current level
        '''
        if self.is_free():
            if not call:
                call = self.call_handler.request_call_from_queue(self.rank)

            if call:
                self.call = call
                call.set_employee_handler(self)
        else:
            raise NameError, 'Instance is currently associated with a valid call'

    def is_free(self):
        if self.call is None:
            return True
