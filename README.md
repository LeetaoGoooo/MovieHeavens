# MovieHeavens

基于Pyqt5的电影天堂电影搜索工具,为了避免找电影期间的各种广告,以及各种页面跳转

### 使用

命令行下

```python
pip install -r requirements.txt
python3 movies.py
```

### 打包

Linux下

```shell
sudo apt-get install python3-pip
pip3 install pyinstaller
bash build.sh
```

Windows下

```shell
# only python3 is supported
pip install pyinstaller
# -w 不能省略,不然会运行过程中会控制台界面
pyinstaller -F -w ./movies.py ./movieSource/MovieHeaven.py ./movieSource/fake_user_agent.py
```

然后会在当前文件夹生成俩个目录,其中**dist**目录有个可执行的程序

![](http://ww2.sinaimg.cn/large/d9e82fa4jw1f7nembhbr1g20dq09nna1.gif)


### 常见问题

打包之后不能正常执行,尝试将打包参数 `-w` 移除,然后在命令行下启动程序,看一下控制台输出错误信息

```ModuleNotFoundError: No module named 'PyQt5.sip'```

**解决办法**

使用下述命令打包

```
pyinstaller -F -w ./movies.py ./movieSource/MovieHeaven.py ./movieSource/fake_user_agent.py --hidden-import PyQt5.sip 
```

### 交流

![](./resources/qcode.jpg)
