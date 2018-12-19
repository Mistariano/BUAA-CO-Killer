from .task import Task


class Tester:
    def __init__(self):
        self._tasks = []

    def run(self):
        for task in self._tasks:
            task.run()

    def add(self, task: Task):
        if isinstance(task, list):
            for t in task:
                assert isinstance(t, Task)
            self._tasks += task
        elif isinstance(task, Task):
            self._tasks.append(task)
        else:
            raise TypeError()


tester = Tester()
