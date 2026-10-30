---
title: "1116. 打印零与奇偶数"
aliases: ["yiduobo的每日leetcode 1116.打印零与奇偶数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/375568225"
zhihu_id: "375568225"
zhihu_title: "yiduobo的每日leetcode 1116.打印零与奇偶数"
question_id: "1116"
question: "打印零与奇偶数"
problem_url: "https://leetcode.cn/problems/print-zero-even-odd/"
created: "2021-05-26T23:28:27+08:00"
updated: "2021-05-26T23:28:27+08:00"
upvotes: 0
comments: 0
---

# 1116. 打印零与奇偶数

> **[yiduobo的每日leetcode 1116.打印零与奇偶数](https://zhuanlan.zhihu.com/p/375568225) · 知乎 · 2021-05-26 · 赞同 0**
> 力扣：[1116. 打印零与奇偶数](https://leetcode.cn/problems/print-zero-even-odd/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1116.打印零与奇偶数

[力扣](https://leetcode-cn.com/problems/print-zero-even-odd/)

还是利用信号量，同样的做法，使用信号量分别控制zero、odd以及even。由于题目的序列是01020304这种，因此semo_zero初始化为1，另外两个初始化为0。

zero中的print只能输出0，那么在print之前需要申请semo_zero，而print之后则需要根据当前是执行的第几次zero来决定后续执行什么，即应该释放semo_odd还是semo_even。

odd中的print只能输出奇数，那么在print之前需要申请semo_odd，而print之后因为要输出0，因此应当释放semo_zero。

even与odd类似，在print之前申请semo_even，在print之后也是释放semo_zero。

最后附上python代码：

```python
import threading

class ZeroEvenOdd(object):
    def __init__(self, n):
        self.n = n
        self.zero_s = threading.Semaphore(1)
        self.even_s = threading.Semaphore(0)
        self.odd_s = threading.Semaphore(0)
        
	# printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber):
        """
        :type printNumber: method
        :rtype: void
        """
        for index in range(1, self.n + 1):
            self.zero_s.acquire()
            printNumber(0)
            if index % 2 == 0:
                self.even_s.release()
            else:
                self.odd_s.release()

        
    def even(self, printNumber):
        """
        :type printNumber: method
        :rtype: void
        """
        for index in range(2, self.n + 1, 2):
            self.even_s.acquire()
            printNumber(index)
            self.zero_s.release()
        
        
    def odd(self, printNumber):
        """
        :type printNumber: method
        :rtype: void
        """
        for index in range(1, self.n + 1, 2):
            self.odd_s.acquire()
            printNumber(index)
            self.zero_s.release()
```
