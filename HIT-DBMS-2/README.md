# 实验二

该实验我们班是需要从两个实验中选取一个，我选取的是邹兆年老师班使用的project2。该实验非常简单，虽然不需要提交实验报告，不过还是在这里记录一下实验中需要注意的地方，供有需要的人参考。

## 实验环境

此实验使用的语言为c++。如果对c++语法不熟悉的话需要了解下基本语法。（只需要了解很基本的即可）

推荐在linux环境下进行实验，我是使用的虚拟机加vim，对于此实验的完成更方便一些，因为该项目包中有makefile等文件，可直接通过终端执行编译和运行的命令（命令已在实验指导书及doc文档中给出）

## 如何进行实验

实验需要编写的文件只有`buffer.cpp`这一个文件，填写其中的几个函数，通过`main.cpp`给出的测试用例即可。

因此需要详细阅读代码的只有这两个文件，其他如有需求，可自行查看代码或doc。

各函数的编写方式在实验指导书中已经说明的非常详细了，照着写就可以。

## 如何执行

具体执行指令在docs/index.html中。下面是具体的执行方法：

写完`buffer.cpp`中的函数后，将`main.cpp`中的test函数的注释去掉。然后回到主目录下（即有`Makefile`文件的那个目录下），依次执行

`make`

`./src/badgerdb_main`

## 测试用例

关于测试用例是什么意思，最好要读懂（其实很多人都是直接在网上找了源码，只读懂了源码就作罢，然而答辩的时候会提问的，很容易就会暴露了不是自己写的）

下面是对几个测试用例的简单解释。

首先，**6个测试用例是连在一起的，是对用一个bufpool进行操作的，因此在上一个测试用例执行完毕后，bufpool中残留的状态会影响到下一个测试用例的执行，部分测试用例是用到了这一点的。**

### test1

向文件中添加数据，并从缓存中读取刚刚添加的数据，以检查是否添加数据成功

检查allocPage(),allocBuf(),unPinPage()三个函数是否编写成功

test1结束后，bufMgr中的所有frame都有数据，且全部为dirty，pinCnt=0（处在这种状态下的frame可被回收并赋给新的page）

### test2

向多文件中添加数据

每次循环时，首先向缓存添加test.2的数据，由于test1()结束时所有frame都有dirty的数据，因此再次添加数据时，需将数据frame中的数据写回文件，然后再填入test.2的page

之后随机的抽查test1的数据，如果仍在缓存中，直接读取，如果被test2覆盖而写回文件，则从文件中读取，并插入缓存，再返回

test3插入的时候，由于刚才的read page1数据的时候，会对其pin加一（此时该test1的pin由零变为1（除了那些刚被读进的test1的数据））所以test3不能对这些test1覆盖，从而会跳过这个test1的page

最后的循环是刚才readpage2和page3的时候，没有unPinPage()，所以在这里集中unPinPage()。

总之这个test考察page之间是否能正确处理冲突，正确的情况（可通过在main.cpp中对应的test()后添加`bufMgr->printSelf();`的语句来查看bufpool中情况）应该是一开始是连续的232323，之后就变成有一些1夹杂在其中

导致这种情况的原因是，随机读page1时，调用readPage函数，如果内存中没有该page,，会去从内存中读出来，再放在buf中，而新从内存中的这个page1，由于没有立即执行unPinPage()，其pinCnt>0，因此是不可以被接下来读入page3替换的

此外如果读取的page1的编号正好与当前的clockhand相等，即使这个page1在bufpool中，由于readPage会使其pinCnt的值加一，仍然会因为没有立即unPinPage()而使接下来插入page3时不可替换。

### test3

这个异常的抛出已经直接被File.readPage实现了

### test4

考察unPinPage()函数中是否有对pinCnt=0的处理

### test5

考察当内存满的情况，需要对allocBuf()函数进行修改

### test6

考察剩余的两个回收函数的编写




