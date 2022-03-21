class Task:
	def __init__(self, function_on_complete, *args, **kwargs):
		"""Represents a task"""
		self.function = function_on_complete
		self.args = args
		self.kwargs = kwargs

	def execute(self):
		"""Executes the task. Required if building from this function"""
		return self.function(*self.args, **self.kwargs)

class Taskinator:
	def __init__(self):
		"""Used to queue tasks for later"""
		self.queue = []

	@property
	def pending(self):
		"""Returns enqueued tasks"""
		return self.queue

	def enqueue(self, item: Task):
		"""Add a task to the queue"""
		self.queue.append(item)

	def dequeue(self, index):
		"""Remove a task from the queue"""
		self.queue.pop(index)

	def process(self, index: int = 0, remove: bool = True):
		"""Process a task using its execute method, defaults to the task at the front of the queue"""
		next = self.queue[index]
		if remove:
			self.queue.pop(index)

		next.execute()