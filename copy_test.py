from win32comext.shell import shell, shellcon
import os
import subprocess

def copy():
    dir1 = r'D:\test\*.*'
    dir2 = r'C:\Users\fuchao\Desktop\test2'
    shell.SHFileOperation(
        (0, shellcon.FO_COPY, dir1, dir2, shellcon.FOF_NOCONFIRMATION | shellcon.FOF_NOCONFIRMMKDIR, None, None)
    )
    print("复制完毕")

def test_bat():
    cmd='D:\\test\\kill_android_tool.bat'
    #cmd = 'D:\\test\\kill_android_tool.bat'
    # 执行干掉AndroidTool的bat
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 输出批处理的结果
    line = p.stdout.readline()
    while line != b'':
        print(line)
        line = p.stdout.readline()
    print(p.returncode)
    #os.system(cmd)

if __name__ == "__main__":
    #copy()
    test_bat()
