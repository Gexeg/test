from tkinter import *
from tkinter import messagebox
import roundrobin
import json


class RoundRobinInterface:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.settings = self.get_start_settings()
        self.is_settings_open = None
        self.settings_entries = None
        self.current_time = int(self.settings['timer_limit'])
        self.current_time_label = None
        self.timer_on_pause = True
        self.listboxes = {}
        # self.round_robin = roundrobin.RoundRobin(self.settings)
        self.create_main_window_widgets()

    def get_start_settings(self):
        with open('start_settings.json') as settings_file:
            data = json.load(settings_file)
            return data

    def create_main_window_widgets(self):
        Label(text='Исполнитель + текущая задача').place(x=80, y=30)
        current_exec_listbox = Listbox()
        self.listboxes['current_exec_listbox'] = current_exec_listbox
        current_exec_listbox.place(x=0, y=50, width=390, height=390)
        Label(text='Все задачи исполнителя').place(x=520, y=30)

        completed_tasks = Listbox()
        self.listboxes['completed_tasks'] = completed_tasks
        completed_tasks.place(x=400, y=50, width=390, height=390)

        Label(text='Лог выполненных задач').place(x=80, y=480)
        completed_tasks = Listbox()
        self.listboxes['completed_tasks'] = completed_tasks
        completed_tasks.place(x=0, y=500, width=390, height=390)

        new_button = Button(text='New')
        new_button.config(command=self.start_new_run)
        new_button.place(x=470, y=550, width=100, height=40)
        Label(text='until next round').place(x=600, y=550)
        self.current_time_label = Label(text=self.current_time)
        self.current_time_label.place(x=640, y=570)
        pause_button = Button(text='Pause')
        pause_button.config(command=self.set_timer_on_pause)
        pause_button.place(x=470, y=600, width=100, height=40)
        settings_button = Button(text='Settings')
        settings_button.config(command=self.open_settings)
        settings_button.place(x=470, y=650, width=100, height=40)

    def update_current_executor_listbox(self):
        pass

    def start_new_run(self):
        self.round_robin = roundrobin.RoundRobin(self.settings)
        self.current_time = self.settings['timer_limit']
        self.timer_on_pause = False

    def set_timer_on_pause(self):
        if self.timer_on_pause:
            self.timer_on_pause = False
            self.tick_tack()
        else:
            self.timer_on_pause = True

    def tick_tack(self):
        if self.timer_on_pause is False:
            if self.current_time == 0:
                self.round_robin.new_round()
                self.current_time = int(self.settings['timer_limit'])
                self.current_time_label.config(text=str(self.current_time + 1))
                self.update_current_executor_listbox()
                return self.tick_tack()
            self.current_time -= 1
            self.current_time_label.config(text=str(self.current_time + 1))
            self.root.after(1000, self.tick_tack)

    def open_settings(self):
        if self.is_settings_open is None:
            t = Toplevel(self.root)
            t.geometry('400x500')
            t.wm_title("Settings")
            self.is_settings_open = t
            self.create_settings_widgets()
            t.protocol("WM_DELETE_WINDOW", self.close_settings)

    def create_settings_widgets(self):
        t = self.is_settings_open
        label_x = 10
        entry_x = 250
        entry_label_y = 20
        self.settings_entries = {}
        for i in self.settings.keys():
            label = Label(t, text=i)
            label.place(x=label_x, y=entry_label_y)
            entry = Entry(t, width=10)
            entry.insert(0, self.settings[i])
            self.settings_entries[i] = entry
            entry.place(x=entry_x, y=entry_label_y)
            entry_label_y += 40

        change_settings_button = Button(t, text='Change settings')
        change_settings_button.config(command=self.change_settings)
        change_settings_button.place(x=40, y=400, width=150, height=40)

        exit_button = Button(t, text='Exit')
        exit_button.config(command=self.close_settings)
        exit_button.place(x=210, y=400, width=150, height=40)

    def change_settings(self):
        if self.is_settings_open:
            errors_counter = 0
            for setting in self.settings_entries.keys():
                try:
                    assert int(self.settings_entries[setting].get())
                    self.settings[setting] = self.settings_entries[setting].get()
                except:
                    errors_counter += 1
                    messagebox.showinfo("Настройка не изменена",
                                        "Пожалуйста, убедитесь, что вы ввели целое число в поле " + setting)
            if errors_counter == 0:
                messagebox.showinfo("Успешно", "Настройки успешно изменены")
            else:
                messagebox.showinfo("Не все настройки изменены",
                                    "Пожалйуста, убедитесь, что во все поля введены целые числа")

    def close_settings(self):
        if self.is_settings_open:
            self.is_settings_open.destroy()
            self.is_settings_open = None
            self.settings_entries = None


a = RoundRobinInterface()
a.root.mainloop()
