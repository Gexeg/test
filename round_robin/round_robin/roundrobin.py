import executor_generator, task_generator
import random, json
import unittest


class RoundRobin:
    def __init__(self, settings):
        self.settings = settings
        self.executors = self.get_executors_roster()
        #self.tasks = self.get_tasks_roster()
        #self.distribute_tasks

    def get_executors_roster(self):
        ex_generator = executor_generator.ExecutorGenerator(int(self.settings['min_executor_productivity']),int(self.settings['max_executor_productivity']))
        number_of_exec = random.randint(int(self.settings['min_num_of_executors']),int(self.settings['max_num_of_executors']))
        return ex_generator.get_executors_roster(number_of_exec)

def set_start_settings():
    with open('start_settings.json') as settings_file:
        data = json.load(settings_file)
        return data

a = RoundRobin(set_start_settings())
print(a.executors)

class ls2_test(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass

