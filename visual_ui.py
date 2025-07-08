import tkinter as tk
from task_registry import TASK_REGISTRY
from task_runner import TaskRunner

class TaskCard(tk.Frame):
    def __init__(self, master, task_name, remove_callback, move_callback, **kwargs):
        super().__init__(master, relief=tk.RAISED, bd=2, bg="#f0f0f0", padx=10, pady=5, **kwargs)
        self.task_name = task_name
        self.remove_callback = remove_callback
        self.move_callback = move_callback
        self.label = tk.Label(self, text=task_name, bg="#f0f0f0", font=("Arial", 12, "bold"))
        self.label.pack(side=tk.LEFT)
        self.remove_btn = tk.Button(self, text="❌", command=self.on_remove, bg="#f0f0f0", relief=tk.FLAT)
        self.remove_btn.pack(side=tk.RIGHT)

        self.bind("<Button-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_drop)
        self.start_y = None

    def on_remove(self):
        self.remove_callback(self)

    def on_start_drag(self, event):
        self.start_y = event.y_root

    def on_drag(self, event):
        self.lift()
        self.place_configure(y=event.y_root - self.master.winfo_rooty() - 20)

    def on_drop(self, event):
        self.move_callback(self, event.y_root - self.master.winfo_rooty())
        self.place_forget()

class VisualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("視覺化流程狀態機（可拖曳排序）")
        self.root.geometry("850x600")

        self.task_frame = tk.Frame(root, bg="#ffffff")
        self.task_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(self.task_frame, text="🧩 可用任務", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=5)

        self.task_buttons = []
        for task_name in TASK_REGISTRY:
            btn = tk.Button(self.task_frame, text=task_name, width=20, command=lambda name=task_name: self.add_task(name))
            btn.pack(pady=2)
            self.task_buttons.append(btn)

        self.pipeline_frame = tk.Frame(root, bg="#e0e0ff", relief=tk.GROOVE, bd=2)
        self.pipeline_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.pipeline_frame, text="🛠 流程順序（可拖曳排序）", font=("Arial", 12, "bold"), bg="#e0e0ff").pack(anchor="w", padx=10, pady=5)
        self.card_container = tk.Frame(self.pipeline_frame, bg="#e0e0ff")
        self.card_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        tk.Button(self.control_frame, text="▶ 執行流程", command=self.run_pipeline).pack(side=tk.LEFT, padx=5)
        tk.Button(self.control_frame, text="❌ 清除流程", command=self.clear_pipeline).pack(side=tk.LEFT, padx=5)

        self.log_text = tk.Text(root, height=8)
        self.log_text.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0,10))

        self.pipeline = []

    def add_task(self, task_name):
        card = TaskCard(self.card_container, task_name, self.remove_task, self.reorder_task)
        card.pack(fill=tk.X, pady=5)
        self.pipeline.append(card)

    def remove_task(self, card):
        card.destroy()
        self.pipeline.remove(card)

    def reorder_task(self, dragged_card, drop_y):
        dragged_card.pack_forget()
        index = 0
        for i, card in enumerate(self.pipeline):
            y = card.winfo_y() + card.winfo_height() // 2
            if drop_y > y:
                index = i + 1
        self.pipeline.remove(dragged_card)
        self.pipeline.insert(index, dragged_card)
        for card in self.pipeline:
            card.pack(fill=tk.X, pady=5)

    def clear_pipeline(self):
        for card in self.pipeline:
            card.destroy()
        self.pipeline.clear()

    def run_pipeline(self):
        self.log_text.delete(1.0, tk.END)
        tasks = []
        for card in self.pipeline:
            cls = TASK_REGISTRY.get(card.task_name)
            if cls:
                tasks.append(cls())
        runner = TaskRunner(tasks, self.log_text)
        runner.run_all()

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()
