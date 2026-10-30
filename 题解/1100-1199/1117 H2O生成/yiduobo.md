---
title: "1117. H2O生成"
aliases: ["yiduobo的每日leetcode 1117.H2O生成"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/375861974"
zhihu_id: "375861974"
zhihu_title: "yiduobo的每日leetcode 1117.H2O生成"
question_id: "1117"
question: "H2O生成"
problem_url: "https://leetcode.cn/problems/building-h2o/"
created: "2021-05-27T22:43:30+08:00"
updated: "2021-05-27T22:43:30+08:00"
upvotes: 0
comments: 0
---

# 1117. H2O生成

> **[yiduobo的每日leetcode 1117.H2O生成](https://zhuanlan.zhihu.com/p/375861974) · 知乎 · 2021-05-27 · 赞同 0**
> 力扣：[1117. H2O生成](https://leetcode.cn/problems/building-h2o/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1117.H2O生成

[力扣](https://leetcode-cn.com/problems/building-h2o/)

依然是使用信号量来解决，不过这里是两个H之后一个O，因此H的计数器应该设为2，而O的计数器则设为0。当执行完某次releaseHydrogen之后，若当前的semo_H的计数器为0，那么才能释放掉semo_O。而执行完releaseOxygen之后，则需要将semo_H的计数器加上2。

python这里的信号量似乎不支持直接查看计数器以及单次操作释放多个计数器，因此我在这里使用一个全局变量来判断当前semo_H的计数器是否为0，感觉不是很优美。

最后附上python代码：

```python
import threading

class H2O(object):
    def __init__(self):
        self.h_s = threading.Semaphore(2)
        self.o_s = threading.Semaphore(0)
        self.h_cnt = 0

    def hydrogen(self, releaseHydrogen):
        """
        :type releaseHydrogen: method
        :rtype: void
        """
        self.h_s.acquire()
        # releaseHydrogen() outputs "H". Do not change or remove this line.
        releaseHydrogen()
        self.h_cnt += 1
        if self.h_cnt == 2:
            self.h_cnt = 0
            self.o_s.release()

    def oxygen(self, releaseOxygen):
        """
        :type releaseOxygen: method
        :rtype: void
        """
        self.o_s.acquire(2)
        # releaseOxygen() outputs "O". Do not change or remove this line.
        releaseOxygen()
        self.h_s.release()
        self.h_s.release()
```
