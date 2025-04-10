# from redis import Redis
# from rq import Worker, Queue

# redis_conn = Redis()
# queue = Queue(connection=redis_conn)

# if __name__ == '__main__':
#     worker = Worker(queues=[queue], connection=redis_conn)
#     worker.work()



# from redis import Redis
# from rq import Queue
# from rq.worker import SimpleWorker  # Импорт из нового места в RQ 2.x

# redis_conn = Redis()
# queue = Queue(connection=redis_conn)

# if __name__ == '__main__':
#     worker = SimpleWorker([queue], connection=redis_conn)
#     worker.work()




# from redis import Redis
# from rq import Queue
# from rq.worker import SimpleWorker  # ← это работает в 1.10.1

# redis_conn = Redis()
# queue = Queue(connection=redis_conn)

# if __name__ == '__main__':
#     worker = SimpleWorker([queue], connection=redis_conn)
#     worker.work()
