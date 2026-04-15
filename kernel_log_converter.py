import time
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os


def convert_kernel_log(content):
    """
    解析日志内容：
    1. 先扫描包含 'android time' 的基准行，提取 kernel time 与对应的 Android 绝对时间
    2. 其余行根据与基准 kernel time 的 delta，计算出对应的 Android 时间
    """
    lines = content.splitlines(keepends=True)

    # 正则：匹配 [  691.165602] android time 2017-06-19 17:47:59.765338
    base_pattern = re.compile(
        r'\[\s*([\d]+)\.([\d]+)\].*?android time\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+)'
    )
    # 正则：匹配任意行的 kernel time [  691.165602]
    time_pattern = re.compile(r'\[\s*([\d]+)\.([\d]+)\]')

    base_kernel_sec = None
    base_kernel_usec = None
    base_epoch = None

    # ---- 1. 查找基准时间 ----
    for line in lines:
        m = base_pattern.search(line)
        if m:
            base_kernel_sec = int(m.group(1))
            # 统一补齐/截断为 6 位微秒
            base_kernel_usec = int(m.group(2)[:6].ljust(6, '0'))

            date_str = m.group(3)  # e.g. 2017-06-19 17:47:59.765338
            date_part, us_part = date_str.split('.')
            us_part = us_part[:6].ljust(6, '0')

            # 使用 time 模块解析为 epoch 时间戳
            dt = time.strptime(date_part, "%Y-%m-%d %H:%M:%S")
            base_epoch = time.mktime(dt) + int(us_part) / 1_000_000.0
            break

    if base_epoch is None:
        raise ValueError("无法在日志中找到包含 'android time' 的基准行，请检查日志格式。")

    # ---- 2. 逐行转换 ----
    out_lines = []
    for line in lines:
        m = time_pattern.search(line)
        if m:
            cur_sec = int(m.group(1))
            cur_usec = int(m.group(2)[:6].ljust(6, '0'))

            delta_sec = cur_sec - base_kernel_sec
            delta_usec = cur_usec - base_kernel_usec

            # 处理微秒借位
            if delta_usec < 0:
                delta_sec -= 1
                delta_usec += 1_000_000

            new_epoch = base_epoch + delta_sec + delta_usec / 1_000_000.0

            # 格式化为 06-19 17:47:59.765338
            new_time_str = time.strftime("%m-%d %H:%M:%S", time.localtime(new_epoch))
            us = int((new_epoch % 1) * 1_000_000)
            new_time_str += f".{us:06d}"

            # 拼接：新 Android 时间 + 空格 + 原行内容
            out_lines.append(f"{new_time_str} {line}")
        else:
            out_lines.append(line)

    return "".join(out_lines)


class ConverterUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kernel Log Android Time 转换器")
        self.root.geometry("800x600")

        self.file_path = tk.StringVar()
        self.result_content = None
        self.output_path = None

        # 标题
        tk.Label(
            root,
            text="Kernel Log → Android Time 转换工具",
            font=("Microsoft YaHei", 18, "bold")
        ).pack(pady=20)

        # 文件选择区
        frame = tk.Frame(root)
        frame.pack(pady=10)
        tk.Entry(frame, textvariable=self.file_path, width=55, state="readonly").pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(frame, text="选择 Log 文件", command=self.select_file, width=15).pack(
            side=tk.LEFT
        )

        # 转换按钮
        tk.Button(
            root,
            text="开始转换",
            command=self.convert,
            bg="#4CAF50",
            fg="white",
            font=("Microsoft YaHei", 12),
            width=20,
            height=1,
        ).pack(pady=20)

        # 状态/预览
        tk.Label(root, text="转换预览 (前 30 行):", font=("Microsoft YaHei", 10)).pack(
            anchor="w", padx=20
        )
        self.preview = scrolledtext.ScrolledText(
            root, height=20, wrap=tk.WORD, font=("Consolas", 10)
        )
        self.preview.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # 底部说明
        tk.Label(
            root,
            text="说明: 工具会自动在日志中查找 'android time' 作为基准，并据此转换所有 kernel 时间戳。",
            font=("Microsoft YaHei", 9),
            fg="gray",
        ).pack(side=tk.BOTTOM, pady=5)

    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Log files", "*.log"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ]
        )
        if path:
            self.file_path.set(path)
            self.preview.delete(1.0, tk.END)
            self.preview.insert(tk.END, f"已选择文件: {path}\n\n点击上方【开始转换】按钮进行处理。")

    def convert(self):
        path = self.file_path.get()
        if not path:
            messagebox.showwarning("提示", "请先选择要转换的 log 文件")
            return

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            result = convert_kernel_log(content)
            self.result_content = result

            # 自动保存到同目录: xxx_converted.txt
            base, ext = os.path.splitext(path)
            self.output_path = f"{base}_converted{ext}"
            with open(self.output_path, "w", encoding="utf-8") as f:
                f.write(result)

            # 预览前 30 行
            preview_lines = result.splitlines()[:30]
            self.preview.delete(1.0, tk.END)
            self.preview.insert(tk.END, "\n".join(preview_lines))
            total_lines = len(result.splitlines())
            if total_lines > 30:
                self.preview.insert(tk.END, f"\n\n... (共 {total_lines} 行，完整结果已保存)")

            messagebox.showinfo(
                "转换完成", f"转换成功！\n结果已自动保存至:\n{self.output_path}"
            )

        except Exception as e:
            messagebox.showerror("转换失败", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterUI(root)
    root.mainloop()
