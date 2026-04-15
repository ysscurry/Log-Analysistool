# Log-Analysistool
• 这个工具的运行环境要求非常简单：

  1. Python 3.x

  • Windows 自带：如果你安装了 Python for Windows（官方安装包），通常默认就包含了所需的一切。
  • 推荐版本：Python 3.8 及以上版本均可。

  2. 无需安装任何第三方库

  工具只使用了 Python 内置标准库：

  • tkinter：用于绘制图形界面（Windows 官方 Python 安装包默认包含）
  • time、re、os、sys：都是标准库，无需 pip install

  3. Windows 兼容性

  • 在 Windows 10/11 上，标准 Python 安装 会自带 tkinter，直接双击 kernel_log_converter.py 或在 CMD/Power
    ell 中执行 python E:\personal\kernel_log_converter.py 即可运行。

如何快速检查你的环境是否满足？

  打开 PowerShell 或 CMD，依次输入：

  python --version
  python -c "import tkinter; print('tkinter OK')"

  如果输出类似下面这样，说明环境完全满足：

  Python 3.11.4
  tkinter OK


运行方式

  双击运行，或者在 PowerShell/CMD 里执行：

  python E:\personal\kernel_log_converter.py

  运行后会弹出一个窗口，点击 "选择 Log 文件" 上传你的 kernel log，再点 "开始转换" 即可。转换结果会自动保
  存为同目录下的 xxx_converted.txt。
