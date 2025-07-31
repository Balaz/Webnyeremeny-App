import logging

logging.basicConfig(filename='debug.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='[ %(levelname)-6s ] %(asctime)s - %(filename)-20s ' +
                           '{ %(funcName)20s(): %(lineno)-3s >> %(message)s',
                    datefmt='%H:%M:%S')
