# -*- coding: utf-8 -*-
import sys
import inspect

class ModuleDescriber():
   def __init__(self, module_name, mod_dyrectory_path=None):
      if mod_dyrectory_path:
         sys.path.append(mod_dyrectory_path + '/' + module_name)
      self.mod = __import__(module_name.replace('.py',''))
      
   def describe_module(self):
      ''' метод начинает с общего описания модуля. Собирает все классы и отдельные функции
      сначала выводится общая информация по модулю, затем следует более подробное описание каждого 
      класса, а затем независимые функции модуля  '''
      class_collector = []
      func_collector = []

      for name in dir(self.mod):
         obj = getattr(self.mod, name)
         if inspect.isclass(obj):
            class_collector.append(obj)
         if inspect.isfunction(obj):
            func_collector.append(obj)

      print(f'Модуль: {self.mod.__name__}')
      code_lines = self.count_code_lines(self.mod)
      print(f'Количество строк кода в модуле: {code_lines}')

      if not class_collector:
         print('Модуль не содержит классов')
      else:
         print(f'Содержит классов: {len(class_collector)}')
         print()
         for element in class_collector:
            print(f'Класс модуля: {self.mod.__name__}')
            self.describe_class(element)
            print()
      if not func_collector:
         print('Модуль не содержит независимых функций')
      else:
         print(f'Содержит функций: {len(func_collector)}')
         for element in func_collector:
            print(f'Функция модуля: {self.mod.__name__}')
            self.describe_func(element)
            print()
      return

   def describe_class(self, obj):
      ''' метод описания класса сначала проверяет все атрибуты класса на наличие методов 
      затем описывает каждый отдельный метод '''
      method_collector = []
      for name in obj.__dict__:
         item = getattr(obj, name)
         if inspect.isfunction(item):
            method_collector.append(item)
      print(f'Класс: {obj.__name__}')
      code_lines = self.count_code_lines(obj)
      print(f'Количество строк кода в классе: {code_lines}')
      
      if not method_collector:
         print('Класс не содержит методов')
      else:
         print(f'Содержит методов: {len(method_collector)}')
         print()
         for element in method_collector:
            print(f'Метод класса: {obj.__name__}')
            self.describe_func(element)
            print()
      return

   def describe_func(self, obj):
      ''' Метод используется для описания функций и модулей. Подсчитывает количество строк кода
      Объявление метод это или независимая функция происходит до вызова этого метода '''
      print(f'Имя: {obj.__name__}')
      code_lines = self.count_code_lines(obj)
      print(f'Количество строк кода: {code_lines}')
      return

   def count_code_lines(self, obj):
      ''' Метод подсчета строк кода.
      Получаем текст модуля/класса/функции
      Не считаем пустые строки и комменты
      Если начинается docstring не считаем, пока не увидим завершения многострочного комментария '''
      lines = inspect.getsourcelines(obj)
      line_counter = 0
      stopper = False
      for line in lines[0]:
         code_line = line.strip().replace('\n','')
         if stopper:
            if code_line.endswith('"""') or code_line.endswith("'''"):
               stopper = False
               continue
            continue
         if not code_line:
            continue
         if code_line.startswith('#'):
            continue
         if code_line.startswith('"""') or code_line.startswith("'''"):
            if code_line.endswith('"""') or code_line.endswith("'''"):
               continue
            stopper = True
            continue       
         line_counter += 1
      return line_counter

mod_name = 'count_module_content.py'

test = ModuleDescriber(mod_name)
test.describe_module()