import psutil
from collections import namedtuple
from sys import argv
from psutil._common import bytes2human

help = """\
    Usage:
    <script name> [options]

    Options:
    -b, --bytes         show output in bytes
    -k, --kilo          show output in kilobytes
    -m, --mega          show output in megabytes    
    -h, --human         show human-readable output
    """

def get_mem_stats():
    result_ntuple = namedtuple("result","memory swap")
    memory = psutil.virtual_memory()    
    swap = psutil.swap_memory()    
    result = result_ntuple(memory,swap)    
    return result

def in_bytes(data):       
    mem = [data.memory.total, data.memory.used, data.memory.free, data.memory.shared, data.memory.buffers + data.memory.cached, data.memory.available]    
    swap = [data.swap.total, data.swap.used, data.swap.free]    
    return mem,swap
    
def in_kilo(data):
    mem, swap = in_bytes(data)
    mem_kb = list(map(lambda x: x // 1024, mem))
    swap_kb = list(map(lambda x: x // 1024, swap))
    return mem_kb, swap_kb  

def in_mega(data):
    mem, swap = in_bytes(data)
    mem_mb = list(map(lambda x: x // (1024 **2), mem))
    swap_mb = list(map(lambda x: x // (1024 **2), swap))
    return mem_mb, swap_mb            

def in_human(data):
    mem, swap = in_bytes(data)
    mem_h = list(map(bytes2human,mem))        
    swap_h = list(map(bytes2human,swap))    
    return mem_h, swap_h

def format_out(mem,swap):
    template = "{:<8} {:>10} {:>10} {:>10} {:>10} {:>10} {:>10}"
    print(template.format("","total","used","free","shared","buff/cache","available"))
    print(template.format("Mem: ",*mem))
    print(template.format("Swap: ",*swap,"","",""))

if __name__ == "__main__":
    stats = get_mem_stats()
    #print(stats)
    if len(argv) == 1 or argv[1] == "-k" or argv[1] == "--kilo":
        mem, swap = in_kilo(stats)
        format_out(mem,swap)
    elif len(argv) == 1 or argv[1] == "-m" or argv[1] == "--mega":
        mem, swap = in_mega(stats)
        format_out(mem,swap)
    elif len(argv) == 1 or argv[1] == "-h" or argv[1] == "--human":
        mem, swap = in_human(stats)
        format_out(mem,swap)
    else:
        print(help)
    
        
