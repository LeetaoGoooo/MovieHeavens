# MovieHeavens

基于Pyqt4的电影天堂电影搜索工具

### 关于开发
最初为了避免找电影期间的各种广告,以及各种页面跳转

### 后续更新

使用过程中如果发现无法检索到结果,应该是网站发生了更新

1. 重新更新了电影天堂的搜索
2. 将 python 由 2 切换到 3

### 使用

命令行下

```python
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
pyinstaller -F -w ./movies.py ./helpUI.py ./movieSource/__init__.py  ./movieSource/MovieHeaven.py ./movieSource/SearchMovieParent.py 
```

然后会在当前文件夹生成俩个目录,其中<code>dist</code>目录有个可执行的程序


![](http://ww2.sinaimg.cn/large/d9e82fa4jw1f7nembhbr1g20dq09nna1.gif)

### 可执行程序

[Linux版本](https://pan.baidu.com/s/1Pd3NrJRmsPeZmJrIbCxJAA)

[Windows版本](https://pan.baidu.com/s/1xVwUSlA4mAp-YQjPSUirlw)

### 其他版本

[Electron版本](https://github.com/lt94/electron-searchMovies)

### 捐赠

如果我的项目对您有帮助，欢迎捐赠

<table>
  <tr>
    <th width="50%">支付宝</th>
    <th width="50%">微信</th>
  </tr>
  <tr></tr>
  <tr align="center">
    <td><img width="70%" src="http://ww1.sinaimg.cn/large/006wYWbGly1fm10itkjb6j30aj0a9t8w.jpg"></td>
    <td><img width="70%" src="http://ww1.sinaimg.cn/large/006wYWbGly1fm10jihygsj309r09tglw.jpg"></td>
  </tr>
</table>
