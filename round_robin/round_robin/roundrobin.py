import executor_generator
import task_generator
import random
import unittest


class RoundRobin:
    def __init__(self, settings):
        self.__settings = settings
        self.__executors_roster = self.__get_executors_roster()
        self.__task_roster = self.__get_tasks_roster()
        self.__distribute_tasks()
        self.__current_round = 0

    def new_round(self):
        for current_executor in self.__executors_roster:
            current_task = current_executor.get_current_task()
            if current_task:
                current_task.reduce_complexity(current_executor.get_productivity())
                if current_task.get_complexity() <= 0:
                    current_executor.complete_task()
        if random.randint(0, 1) == 1:
            self.__swap_tasks()
        self.__current_round += 1

    def get_executors(self):
        return self.__executors_roster

    def get_current_round(self):
        return self.__current_round

    def __swap_tasks(self):
        stack1 = []
        for current_executor in self.__executors_roster:
            stack2 = [current_executor.get_current_task()]
            current_executor.complete_task()
            if stack1:
                current_executor.change_current_task(stack1.pop())
            stack1.append(stack2.pop())
        self.__executors_roster[0].change_current_task(stack1.pop())

    def __get_executors_roster(self):
        ex_generator = executor_generator.ExecutorGenerator(int(self.__settings['min_executor_productivity']),
                                                            int(self.__settings['max_executor_productivity']))
        number_of_exec = random.randint(int(self.__settings['min_num_of_executors']),
                                        int(self.__settings['max_num_of_executors']))
        return ex_generator.get_executors_roster(number_of_exec)

    def __get_tasks_roster(self):
        task_gen = task_generator.TaskGenerator(int(self.__settings['min_task_complexity']),
                                                int(self.__settings['max_task_complexity']))
        number_of_tasks = random.randint(int(self.__settings['min_num_of_tasks']),
                                         int(self.__settings['max_num_of_tasks']))
        return task_gen.generate_tasks(number_of_tasks)

    def __distribute_tasks(self):
        while len(self.__task_roster) > 0:
            current_task = self.__task_roster.pop(0)
            exec_index = 0
            while True:
                if exec_index >= len(self.__executors_roster):
                    exec_index = 0
                self.__executors_roster[exec_index].add_new_task(current_task)
                exec_index += 1
                if len(self.__task_roster) == 0:
                    break
                else:
                    current_task = self.__task_roster.pop(0)


class TestClass(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
