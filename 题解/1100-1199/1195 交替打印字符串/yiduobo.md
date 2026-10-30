---
title: "1195. 交替打印字符串"
aliases: ["yiduobo的每日leetcode 1195.交替打印字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/381335568"
zhihu_id: "381335568"
zhihu_title: "yiduobo的每日leetcode 1195.交替打印字符串"
question_id: "1195"
question: "交替打印字符串"
problem_url: "https://leetcode.cn/problems/fizz-buzz-multithreaded/"
created: "2021-06-16T23:42:37+08:00"
updated: "2021-06-16T23:42:37+08:00"
upvotes: 0
comments: 0
---

# 1195. 交替打印字符串

> **[yiduobo的每日leetcode 1195.交替打印字符串](https://zhuanlan.zhihu.com/p/381335568) · 知乎 · 2021-06-16 · 赞同 0**
> 力扣：[1195. 交替打印字符串](https://leetcode.cn/problems/fizz-buzz-multithreaded/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1195.交替打印字符串

[力扣](https://leetcode-cn.com/problems/fizz-buzz-multithreaded/)

又是多线程相关的问题，还是使用信号量来解决。

由于我们需要从1到n都输出字符串，因此一个自然的想法就是所有打印任务都经过number，由number控制当前应该直接打印数字，还是唤起打印字符串的线程，那么可以使用三个信号量分别控制fizz、buzz以及fizzbuzz的输出，然后使用另一个信号量负责控制number。

初始化为可以执行number，然后在number中先尝试获取信号量，然后根据当前的数值判断应该选择打印字符串还是输出数字。若打印字符串，则release掉对应的信号量，若输出数字，则release掉number自身的信号量。

对于输出字符串的线程，则一直尝试获取信号量，若获取成功，则打印对应的字符串，然后release掉number的信号量为下一个数字做准备。

最后附上python代码：

```python
import threading

class FizzBuzz(object):
    def __init__(self, n):
        self.n = n
        self.f_s = threading.Semaphore(0)
        self.b_s = threading.Semaphore(0)
        self.fb_s = threading.Semaphore(0)
        self.num_s = threading.Semaphore(1)

    # printFizz() outputs "fizz"
    def fizz(self, printFizz):
        """
        :type printFizz: method
        :rtype: void
        """
    	for index in range(3, self.n + 1, 3):
            if index % 5 != 0:
                self.f_s.acquire()
                printFizz()
                self.num_s.release()

    # printBuzz() outputs "buzz"
    def buzz(self, printBuzz):
        """
        :type printBuzz: method
        :rtype: void
        """
    	for index in range(5, self.n + 1, 5):
            if index % 3 != 0:
                self.b_s.acquire()
                printBuzz()
                self.num_s.release()

    # printFizzBuzz() outputs "fizzbuzz"
    def fizzbuzz(self, printFizzBuzz):
        """
        :type printFizzBuzz: method
        :rtype: void
        """
        for index in range(15, self.n + 1, 15):
            self.fb_s.acquire()
            printFizzBuzz()
            self.num_s.release()

    # printNumber(x) outputs "x", where x is an integer.
    def number(self, printNumber):
        """
        :type printNumber: method
        :rtype: void
        """
        for index in range(1, self.n + 1):
            self.num_s.acquire()
            if index % 3 == 0:
                if index % 5 == 0:
                    self.fb_s.release()
                else:
                    self.f_s.release()
            elif index % 5 == 0:
                self.b_s.release()
            else:
                printNumber(index)
                self.num_s.release()
```
