from IPython.utils.capture import capture_output
import time
import os

MAX_SIZE = 20000000
# If it is not directly accessible from
LOG_FILE = './code_history' 
LOG_FILE = None 

def update_record(cell, id, result, dire = './code_history'):
    if not os.path.isdir(dire):
        os.mkdir(dire)
    file_dire = get_index(dire)
    with open(file_dire, 'a') as f:
        f.write('new run: {} \n'.format(id,))
        f.write('format error: {} \n'.format(result.error_before_exec))
        f.write('execution error: {} \n'.format(result.error_in_exec))
        f.write(cell)
        
def get_index(dire):
    index_dire = os.path.join(dire, 'current_index.txt')
    if os.path.isfile(index_dire):
        with open(index_dire, 'r') as f:
            index = int(f.readline())
    else:
        index = 0
        with open(index_dire, 'w') as f:
            f.write(str(index))
    file_dire = os.path.join(dire, 'runs_{}.txt'.format(self.index))
    if os.path.isfile(file_dire):
        fsize = os.path.getsize(file_dire)
    else:
        fsize = 0

    if fsize >= MAX_SIZE:
        index += 1
        index_dire = os.path.join(dire, 'current_index.txt')
        with open(index_dire, 'w') as f:
            f.write(str(index))

    file_dire = os.path.join(dire, 'runs_{}.txt'.format(index))
    return file_dire

def store_log(ipython):
    cell_content = ipython.history_manager.input_hist_parsed[-1]
    print(f"After execution:\n{cell_content}\n")
    if ipython._last_traceback:
        error_message = "".join(ipython._last_traceback)
        error_type = ipython._last_traceback[0].strip() 
        print(f"{error_type}:\n{error_message}\n")

def load_ipython_extension(ipython):
    ipython.events.register('post_execute', store_log)

def unload_ipython_extension(ipython):
    ipython.events.unregister('post_execute', store_log)