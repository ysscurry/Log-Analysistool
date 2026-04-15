# Kernel Log Android Time 转换工具

一个基于 Python + tkinter 的桌面小工具，用于将 kernel log 中的相对时间戳转换为 Android 绝对时间。

---

## 运行环境

- **Python 3.8 及以上版本**
- **零第三方依赖**，仅使用 Python 内置标准库：
  - `tkinter`：图形界面（Windows 官方 Python 安装包默认自带）
  - `time`、`re`、`os`：时间转换与文件操作

---

## 环境自检

打开 **PowerShell** 或 **CMD**，依次执行：

```powershell
python --version
python -c "import tkinter; print('tkinter OK')"
```

正常输出示例：

```text
Python 3.11.4
tkinter OK
```

> 若提示 `'python' 不是内部或外部命令`，请先安装 [官方 Python](https://www.python.org/downloads/)，**安装时务必勾选 "Add Python to PATH"**。

---

## 如何使用

### 启动工具

```powershell
python E:\personal\kernel_log_converter.py
```

或直接双击 `kernel_log_converter.py` 运行。

### 操作步骤

1. 点击 **"选择 Log 文件"** 上传需要转换的 kernel log
2. 点击 **"开始转换"**
3. 工具会自动在日志中查找包含 `android time` 的基准行，并据此计算所有 kernel 时间戳对应的 Android 绝对时间
4. 转换结果自动保存为同目录下的 `xxx_converted.txt`

---

## 转换示例

**输入（kernel log）：**

```text
#06-19 17:47:59.765338 [  691.165602] android time 2017-06-19 17:47:59.765338
[  692.123456] Some kernel message
```

**输出：**

```text
06-19 17:47:59.765338 #06-19 17:47:59.765338 [  691.165602] android time 2017-06-19 17:47:59.765338
06-19 17:48:00.623192 [  692.123456] Some kernel message
```

---

## 注意事项

- 日志中必须包含至少一行带有 `android time` 的基准记录，否则转换将失败
- 工具支持 `.log`、`.txt` 及任意文本格式的日志文件
- 转换后的文件默认与原文件位于同一目录
