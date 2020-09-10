from threading import Thread, ThreadError


class Threads:

    """Threads management class"""

    def __init__(self):
        self.__threads = []

    def start(self, func, _args_: list = []) -> bool:
        """Create new thread and start it

        :param function: target function to start
        :type func: function
        :param _args_: func arguments (default => [])
        :type _args_: list (optional)
        :returns: True if thread started else False
        :rtype: bool
        """
        try:
            # create thread object
            process = Thread(target=func, args=_args_, daemon=True)
            # start the thread
            process.start()
            # append the thread to threads list
            self.__threads.append(process)
            return True
        except (ThreadError, RuntimeError) as threadStartEX:
            try:
                # stop the thread if it's running
                process.join()
            except RuntimeError:
                pass
            print(f"Thread start Error: {threadStartEX}")
            return False

    def stop(self) -> bool:
        """Stop all threads on the list

        :returns: True if threads is stopped else False:
        :rtype: bool
        """
        try:
            # iterate over self.__threads list
            for process in self.__threads:
                # stop the thread
                process.join(1)
            # clear the list
            self.__threads.clear()
            return True
        except (ThreadError, RuntimeError) as threadStopEX:
            print(f"Thread stop Error: {threadStopEX}")
            return False
