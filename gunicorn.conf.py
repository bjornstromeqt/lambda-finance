import multiprocessing

workers = multiprocessing.cpu_count() * 3 + 1
worker_class = 'gevent'
timeout = 45
