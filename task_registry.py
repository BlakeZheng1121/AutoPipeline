import os
import importlib
import inspect
from pathlib import Path

TASK_REGISTRY = {}

tasks_dir = Path(__file__).parent / "tasks"

for file in tasks_dir.glob("*.py"):
    if file.name == "__init__.py":
        continue

    module_name = f"tasks.{file.stem}"
    try:
        module = importlib.import_module(module_name)
    except Exception as e:
        print(f"[task_registry] 載入模組失敗：{module_name} - {e}")
        continue

    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and hasattr(obj, "run") and callable(getattr(obj, "run")):
            TASK_REGISTRY[name] = obj
