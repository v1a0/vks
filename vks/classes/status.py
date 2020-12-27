from classes.database import Database
from flex_loger import logger
from typing import AnyStr


class StatusCodes:
    @logger.catch
    def __init__(self):
        self.undefended = 100
        self.finished = 200
        self.success = 201
        self.processing = 300
        self.looped = 301
        self.restarting = 302
        self.failed = 400
        self.fatal_error = 401
        self.forced_stopped = 402


class Status:
    @logger.catch
    def __init__(self, module_name: AnyStr):
        self.all_codes = StatusCodes()
        self.code = self.all_codes.undefended
        self.module_name = module_name
        self.__db__ = Database(path='db/modules_stat.db')
        self.__stat__ = 'Undefended'
        self.__db__.create_table(
            table_name='statuses',
            rows={
                'module': 'TEXT PRIMARY KEY UNIQUE',
                'status': 'TEXT',
                'code': 'INTEGER DEFAULT 0',
            })
        self.undefended()

    @logger.catch
    def __bool__(self) -> bool:
        return self.code // 100 != 4

    @logger.catch
    def __save_status__(self):
        self.__db__.insert_or_replace(
            table_name='statuses',
            rows={
                'module': self.module_name,
                'status': self.__stat__,
                'code': self.code,
            })

    @logger.catch
    def undefended(self):
        self.__stat__ = 'Undefended'
        self.code = self.all_codes.undefended
        self.__save_status__()

    @logger.catch
    def finished(self):
        self.__stat__ = 'Finished'
        self.code = self.all_codes.finished
        self.__save_status__()

    @logger.catch
    def success(self):
        self.__stat__ = 'Success'
        self.code = self.all_codes.success
        self.__save_status__()

    @logger.catch
    def processing(self):
        self.__stat__ = 'Processing'
        self.code = self.all_codes.processing
        self.__save_status__()

    @logger.catch
    def looped(self):
        self.__stat__ = 'Looped'
        self.code = self.all_codes.looped
        self.__save_status__()

    @logger.catch
    def restarting(self):
        self.__stat__ = 'Restarting'
        self.code = self.all_codes.restarting
        self.__save_status__()

    @logger.catch
    def failed(self):
        self.__stat__ = 'Failed'
        self.code = self.all_codes.failed
        self.__save_status__()

    @logger.catch
    def fatal_error(self):
        self.__stat__ = 'Fatal error'
        self.code = self.all_codes.fatal_error
        self.__save_status__()

    @logger.catch
    def forced_stopped(self):
        self.__stat__ = 'Forced stopped'
        self.code = self.all_codes.forced_stopped
        self.__save_status__()
