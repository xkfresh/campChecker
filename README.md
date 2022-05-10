# campChecker
自动监视camp场有没有空位


1.安装selenium<br>
/usr/local/opt/python@3.9/bin/python3.9 -m pip install --upgrade pip <br>
pip install selenium <br>
pip install requests<br>
2.安装selenium的浏览器驱动，不同浏览器的驱动不一样

3.安装chromedriver<br>
  brew install chromedriver

4.Mac的安全控制中许可chromedriver

5.在checkPage.py里面设好监视网址和模拟点击的元素(文字或者id)

6.使用webhook 进行通知（例如slack）



