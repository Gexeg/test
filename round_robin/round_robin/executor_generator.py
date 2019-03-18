import requests
from random import randint, getrandbits
import unittest


class Executor:
    def __init__(self, name, productivity, executor_hash):
        self.__executor_hash = executor_hash
        self.__name = name
        self.__productivity = productivity
        self.__task_queue = []

    def get_name(self):
        return self.__name

    def get_productivity(self):
        return self.__productivity

    def get_executor_hash(self):
        return self.__executor_hash

    def get_current_task(self):
        if self.__task_queue:
            return self.__task_queue[-1]

    def get_task_queue(self):
        return self.__task_queue

    def add_new_task(self, task):
        self.__task_queue.insert(0, task)

    def change_current_task(self, task):
        self.__task_queue.append(task)

    def complete_task(self):
        if self.__task_queue:
            self.__task_queue.pop()


class ExecutorGenerator:
    def __init__(self, min_productivity, max_productivity):
        self.__min_productivity = min_productivity
        self.__max_productivity = max_productivity
        self.__url_for_requests = 'http://names.drycodes.com/'
        self.__param_for_url_boy_names = '?nameOptions=boy_names'
        self.__param_for_url_girl_names = '?nameOptions=girl_names'

    def get_executors_roster(self, number_of_names):
        executor_names = self.__generate_names(number_of_names)
        executors = []
        for name in executor_names:
            new_executor_productivity = self.__generate_productivity()
            new_executor_hash = self.__generate_executor_hash(name)
            print(new_executor_hash)
            new_executor = Executor(name, new_executor_productivity, new_executor_hash)
            executors.append(new_executor)
        return executors

    def set_min_max_productivity(self, min_productivity, max_productivity):
        self.__min_productivity = min_productivity
        self.__max_productivity = max_productivity

    def __generate_executor_hash(self, value):
        return value + str(getrandbits(128))[:randint(6, 10)]

    def __generate_names(self, number_of_names):
        num_boy_names = randint(0, number_of_names)
        num_girl_names = number_of_names - num_boy_names
        all_names = self.__generate_boy_names(num_boy_names) + self.__generate_girl_names(num_girl_names)
        if len(all_names) > number_of_names:
            while len(all_names) > number_of_names:
                all_names.pop()
        return all_names

    def __generate_productivity(self):
        return randint(self.__min_productivity, self.__max_productivity)

    def __generate_boy_names(self, number_of_names):
        url_for_request = self.__url_for_requests + str(number_of_names) + self.__param_for_url_boy_names
        name_roster = requests.get(url_for_request)
        if name_roster.ok:
            return name_roster.json()
        else:
            name_roster = self.__offline_generate_boy_names(number_of_names)
            return name_roster

    def __offline_generate_boy_names(self, number_of_names):
        name_roster = ['boy_name' + str(i+1) for i in range(number_of_names)]
        return name_roster

    def __generate_girl_names(self, number_of_names):
        if number_of_names != 0:
            url_for_request = self.__url_for_requests + str(number_of_names) + self.__param_for_url_girl_names
            name_roster = requests.get(url_for_request)
            if name_roster.ok:
                return name_roster.json()
            else:
                name_roster = self.__offline_generate_girl_names(number_of_names)
                return name_roster
        else:
            return []

    def __offline_generate_girl_names(self, number_of_names):
        name_roster = ['girl_name' + str(i+1) for i in range(number_of_names)]
        return name_roster


class TestClass(unittest.TestCase):

    def setUp(self):
        pass

    def test_set_new_productivity(self):
        a = ExecutorGenerator(1, 10)
        a.set_min_max_productivity(5, 15)
        self.assertEqual(a._ExecutorGenerator__min_productivity, 5)
        self.assertEqual(a._ExecutorGenerator__max_productivity, 15)

    def test_create_executor(self):
        a = ExecutorGenerator(1, 10)
        exec_roster = a.get_executors_roster(10)
        self.assertEqual(len(exec_roster), 10)

    def test_generate_names(self):
        error_counter = 0
        for i in range(10):
            executor_gen = ExecutorGenerator(1, 10)
            new_executor_roster = executor_gen.get_executors_roster(2)
            if len(new_executor_roster) > 2:
                error_counter += 1
        self.assertEqual(error_counter, 0)
    
    def tearDown(self):
        pass
