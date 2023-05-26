import keyboard
import pyperclip
import time
from ocr.api.PPOCR_api import GetOcrApi
import json
import ocr.api.tbpu
def info():
    print("就要复制粘贴!")
    print("用 Ctrl+Shift+V 模拟键盘输出剪贴板板的内容")
    print("用 Win+Shift+S 获取图片，再用 Ctrl+Shift+X 把剪贴板的图片转为纯文本")
    print("如果你想修改快捷键，直接修改本文件热键部分即可")
    print("用 Ctrl+Shift+E 退出程序，或者暴力地 Ctrl+C 退出程序")
    

def type_clipboard():
    # 键盘模拟输入剪切板的内容。
    clipboard_content = pyperclip.paste()
    print("模拟键盘输入：\n", clipboard_content)
    keyboard.release('ctrl+shift+v')
    time.sleep(0.2) # 等待 ctrl, shift 正确释放，否则会发生可怕的事情
    keyboard.write(clipboard_content)

ocr_backen = None  # 全局变量，用于存储 OCR 后端对象
def clipboard_img2text():
    # 用 win+shift+s 自行获取区域截图到剪贴板后再使用此功能
    # 将剪贴板的图片内容识别为文字
    global ocr_backen
    # 第一次调用函数时，创建 OCR 对象
    if ocr_backen is None:
        ocr_backen = GetOcrApi(r".\ocr\PaddleOCR_json.exe")

    res = ocr_backen.runClipboard() # 从剪切板识别图片
    if res["code"] != 100:
        print(res) # 识别失败，可能剪切板不是图片。
    else:
        tbList = res["data"]
        tbTexts = [tb['text'] for tb in tbList]  # 提取文字
        tbStr = '\n'.join(tbTexts)
        print("剪切板文字识别：\n", tbStr)
        pyperclip.copy(tbStr)
    

# 设置热键
keyboard.add_hotkey('ctrl+shift+v', type_clipboard)
keyboard.add_hotkey('ctrl+shift+x', clipboard_img2text) # ctrl+shift+c 容易强制终止命令行。故用x

info()
keyboard.wait('ctrl+shift+e')
print("Exiting...")
if ocr_backen is not None:
    ocr_backen.exit()
