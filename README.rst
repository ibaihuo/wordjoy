=========
 WordJoy
=========


介绍
~~~~

WordJoy是一个用pygtk编写的英文背单词软件, 运行平台为Linux。


WordJoy基于TualatriX大侠的MyWord改写而成，而MyWord又是继承于Stardict作者HuZheng（功德藏菩萨）的reciteword背单词软件而来。具体请参看这两款软件的信息。


本程序的特色
~~~~~~~~~~~~

本程序的特色:

    1. 采用全部的书本格式，争取做到更加简洁、明了、实用。
    2. 每个单词配以三个例句，让你在句子中学习单词的意思与用法。
	3. 支持使用WyabdcRealPeopleTTS真人语音包发音。
	4. 支持单词测试，随时掌握自己的学习情况。
	5. 支持背诵的遗忘曲线，采用记录的方式提醒你，今天该背诵的单词。
	6. 支持自定义词库，自己制作背诵的书本（只需要给出单词列表，即可自动生成）。

更多特色由你来扩展,本项目現在进行当中，期待你的参与……

有关词库，请参照books/里面的词库说明。


安装
~~~~

请参考doc/INSTALL文件。


语音库的安装
~~~~~~~~~~~~

1. 下载真人语音库：

本程序利用的是stardict的真人发音库包。

自己去网上找WyabdcRealPeopleTTS.tar.bz2这个包，有81M左右。

2. 进入语音库的下载目录：然后执行解压命令::

   $ sudo tar -jxvf WyabdcRealPeopleTTS.tar.bz2 -C /usr/share/
