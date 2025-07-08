class TaskRunner:
    def __init__(self, tasks, log_widget=None):
        self.tasks = tasks
        self.context = {}
        self.log_widget = log_widget

    def log(self, message):
        print(message)
        if self.log_widget:
            self.log_widget.insert('end', message + "\n")
            self.log_widget.see('end')

    def run_all(self):
        for i, task in enumerate(self.tasks):
            task_name = task.__class__.__name__
            self.log(f"\n🟡 執行任務 {i+1}: {task_name}")
            try:
                success = task.run(self.context)
                if success:
                    self.log(f"🟢 任務成功: {task_name}")
                else:
                    self.log(f"🔴 任務失敗: {task_name}，流程中止")
                    break
            except Exception as e:
                self.log(f"❌ 任務異常: {task_name} - {e}")
                break
