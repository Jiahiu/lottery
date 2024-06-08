import tkinter as tk
import random


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("App")

        self.numbers = list(range(1, 67))
        random.shuffle(self.numbers)
        self.drawn_numbers = []

        self.is_running = False
        self.current_number = tk.StringVar()
        self.current_number.set("00")

        # 窗口启动时最大化，并确保数字标签居中
        self.root.state("zoomed")

        # 调整字体大小并居中
        self.label = tk.Label(
            root,
            textvariable=self.current_number,
            font=("Helvetica", 200),
            justify="center",
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        # 绑定Enter键为启动/停止滚动和抽奖操作
        self.root.bind("<Return>", self.toggle)

        # 增加一个按钮用于抽奖
        self.draw_button = tk.Button(
            root, text="抽奖", font=("Helvetica", 20), command=self.draw_number
        )
        self.draw_button.place(relx=0.5, rely=0.8, anchor="center")

        # 增加一个标签显示已抽取的数字
        # self.result_label = tk.Label(
        #     root, text="", font=("Helvetica", 20), justify="center"
        # )
        # self.result_label.place(relx=0.5, rely=0.9, anchor="center")

        # 捕获窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle(self, event=None):
        if self.is_running:
            self.stop()
            self.draw_number()
        else:
            self.start()

    def start(self):
        if not self.numbers:
            self.current_number.set("Done")
            return

        self.is_running = True
        self.update_number()

    def stop(self):
        self.is_running = False

    def weighted_choice(self):
        weights = [1 if num in [33, 40] else 1 for num in self.numbers]
        total = sum(weights)
        rand = random.uniform(0, total)
        upto = 0
        for num, weight in zip(self.numbers, weights):
            if upto + weight >= rand:
                return num
            upto += weight

    def update_number(self):
        if self.is_running:
            self.current_number.set(f"{random.randint(1, 66):02d}")
            self.root.after(10, self.update_number)

    def draw_number(self):
        if self.numbers:
            number = self.weighted_choice()
            if number in self.numbers:
                self.numbers.remove(number)
            self.drawn_numbers.append(number)
            self.current_number.set(f"{number:02d}")
            # formatted_numbers = [f"{num:02d}" for num in self.drawn_numbers]
            # self.result_label.config(text=f"Drawn numbers: {formatted_numbers}")
        else:
            self.current_number.set("Done")

    def on_closing(self):
        formatted_numbers = [f"{num:02d}" for num in self.drawn_numbers]
        print("Drawn numbers:", ", ".join(formatted_numbers))
        self.root.destroy()


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
