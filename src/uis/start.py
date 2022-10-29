import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.uis.gtools import *


class Start(ttk.Window):
    def __init__(self, alpha: float = 1, **kwargs):
        super().__init__(**kwargs)
        self.pos = (0, 0)
        self.task_bar_size = get_task_bar_size()
        self.ui_size = self.task_bar_size
        self.ui_size = (round(self.ui_size[0] * 0.4), round(self.ui_size[1] * 2.5))

        self.src_size = self.winfo_screenwidth(), self.winfo_screenheight()

        self.set_pos()

        self.overrideredirect(True)  # 无边框窗口

        self.attributes('-topmost', 1)  # 置顶
        self.attributes("-alpha", alpha)  # 设置透明度

        self.text_box = ttk.Entry()
        self.text_box.insert(0, "test")
        # self.text_box.configure(state="readonly")
        self.text_box.pack(fill="both", expand=1)

    def set_pos(self):
        self.pos = (self.src_size[0] - self.ui_size[0], self.src_size[1] - self.ui_size[1] - self.task_bar_size[1])
        self.geometry("{}x{}+{}+{}".format(*self.ui_size, *self.pos))
