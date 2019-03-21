from random import choice, randint


class Task:
    def __init__(self, name, complexity):
        self.__name = name
        self.__complexity = complexity

    def get_name(self):
        return self.__name

    def get_complexity(self):
        return self.__complexity

    def reduce_complexity(self, executor_productivity):
        self.__complexity = self.__complexity - executor_productivity

    def check_is_complete(self):
        return self.__complexity <= 0


class TaskGenerator:
    def __init__(self, min_complexity, max_complexity):
        self.__min_complexity = min_complexity
        self.__max_complexity = max_complexity
        self.__task_adverb = ['Быстро ', 'Феерично ', 'Дорого ', 'Эффектно ', 'Похрюкивая ',
                              'Дешево ', 'К заходу солнца ', 'В течение недели ', 'В течение суток ', 'Завтра ']
        self.__task_verb = ['починить ', 'сломать ', 'взломать ', 'вскрыть ', 'найти ', 'арендовать ']
        self.__task_noun = ['сервер', 'сарай', 'сейф', 'шкаф', 'скрипт', 'склад', 'смартфон', 'лэптоп']

    def generate_tasks(self, number_of_tasks):
        task_name_roster = self.__generate_task_names(number_of_tasks)
        tasks = []
        for name in task_name_roster:
            new_task_complexity = self.__generate_task_complexity()
            new_task = Task(name, new_task_complexity)
            tasks.append(new_task)
        return tasks

    def set_min_max_complexity(self, min_complexity, max_complexity):
        self.__min_complexity = min_complexity
        self.__max_complexity = max_complexity

    def __generate_task_names(self, number_of_tasks):
        task_name_roster = []
        for i in range(number_of_tasks):
            task_name = choice(self.__task_adverb) + choice(self.__task_verb) + choice(self.__task_noun)
            if task_name not in task_name_roster:
                task_name_roster.append(task_name)
            else:
                task_counter = 2
                task_name_with_counter = task_name + '_' + str(task_counter)
                while task_name_with_counter in task_name_roster:
                    task_counter += 1
                    task_name_with_counter = task_name + '_' + str(task_counter)
                task_name_roster.append(task_name_with_counter)
        return task_name_roster

    def __generate_task_complexity(self):
        return randint(self.__min_complexity, self.__max_complexity)
