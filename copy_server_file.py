#复制服务器上编译好的文件到本地
import os
import shutil
import subprocess
import win32.win32file
from win32comext.shell import shellcon,shell

IMAGE_PATH = r"Z:\svn\Android_628\system_rk3128_jy\images\rockdev-rk312x\image";#服务器上编译好的镜像地址
LOCAL_PATH = r"D:\tools\rockdev\Image";#本地保存镜像的地址
BAT_PATH = r'D:\tools\rockdev'#makeup.bat所在的目录
BAT_NAME = r'mkupdate2.bat' #生成update.img的批处理
EXE_PATH = r'D:\tools\AndroidTool_Release_v2.35\AndroidTool.exe'
KILL_BAT_PATH = "D:\\tools\\kill_android_tool.bat" #干掉AndroidTool的bat地址

#把服务器上编译的img镜像复制到本地
def copy():
    print("开始复制....%s....到...%s" % (IMAGE_PATH,LOCAL_PATH))
    files = os.listdir(IMAGE_PATH)
    #遍历文件
    for index,file in enumerate(files):
        fileSource = os.path.join(IMAGE_PATH,file);
        fileDes = os.path.join(LOCAL_PATH,file)
        if os.path.exists(fileDes):
            print("目标文件存在，删除: %s" % fileDes)
            os.remove(fileDes)
        print("[%d] 正在复制文件 %s ..."  % (index,fileSource))
        shutil.copy(fileSource,fileDes)
    print("复制完毕")

#干掉AndroidTool程序
def kill_android_tool():
    cmd = KILL_BAT_PATH
    # 执行干掉AndroidTool的bat
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # 输出批处理的结果
    line = p.stdout.readline()
    while line != b'':
        print(line)
        line = p.stdout.readline()
    print(p.returncode)


#调用BAT文件生成update.img
def create_update_image():
    #先切换到BAT所在的目录，否则BAT中用到的命令将无法识别
    os.chdir(BAT_PATH)
    cmd = os.path.join(BAT_PATH,BAT_NAME)
    #执行生成update.img是批处理文件
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    #输出批处理的结果
    line = p.stdout.readline()
    while line != b'':
        print(line)
        line = p.stdout.readline()
    print(p.returncode)

#再次启动AndroidTool
def start_android_tool():
    os.startfile(EXE_PATH)

#改用带对话框的win32 api，速度更快
def copy2():
    dir1 = os.path.join(IMAGE_PATH,"*.*")
    dir2 = LOCAL_PATH
    shell.SHFileOperation(
        (0, shellcon.FO_COPY, dir1, dir2, shellcon.FOF_NOCONFIRMATION | shellcon.FOF_NOCONFIRMMKDIR, None, None)
    )
    print("复制完毕")

if  __name__ =="__main__":
    print("开始复制文件")
    copy2()
    print("干掉AndroidTool进程")
    kill_android_tool()
    print("创建update.img")
    create_update_image()
    print("重新启动AndroidTool")
    start_android_tool()
    print("全部操作结束")
    os.system("pause")