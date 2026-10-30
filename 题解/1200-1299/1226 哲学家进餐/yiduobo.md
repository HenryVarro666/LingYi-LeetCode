---
title: "1226. 哲学家进餐"
aliases: ["yiduobo的每日leetcode 1226.哲学家进餐"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384044642"
zhihu_id: "384044642"
zhihu_title: "yiduobo的每日leetcode 1226.哲学家进餐"
question_id: "1226"
question: "哲学家进餐"
problem_url: "https://leetcode.cn/problems/the-dining-philosophers/"
created: "2021-06-25T21:39:10+08:00"
updated: "2021-06-25T21:39:10+08:00"
upvotes: 0
comments: 1
---

# 1226. 哲学家进餐

> **[yiduobo的每日leetcode 1226.哲学家进餐](https://zhuanlan.zhihu.com/p/384044642) · 知乎 · 2021-06-25 · 赞同 0**
> 力扣：[1226. 哲学家进餐](https://leetcode.cn/problems/the-dining-philosophers/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1226.哲学家进餐

[力扣](https://leetcode-cn.com/problems/the-dining-philosophers/)

经典的多线程问题，设计策略的时候可能碰到锁住的情况。例如所有哲学家都先拿左手的叉子，后拿右手的叉子，那么就可能出现所有哲学家都拿了左手的叉子，但拿不到右手的叉子的情况。

一个简单的思路是分奇偶来控制，偶数位上的哲学家优先拿左手边的叉子，奇数位上的哲学家则优先拿右手边的叉子，这样一来就可以避免锁住的情况了。

具体实现上，还是使用信号量。初始化5个信号量表示5把叉子，然后可以通过当前哲学家的编号计算出其左手边和右手边的叉子的编号，然后情况对应的信号量即可。

最后附上python代码：

```python
import threading

class DiningPhilosophers(object):

    def __init__(self):
        self.s_list = [threading.Semaphore(1) for _ in range(5)]

    # call the functions directly to execute, for example, eat()
    def wantsToEat(self, philosopher, pickLeftFork, pickRightFork, eat, putLeftFork, putRightFork):
        """
        :type philosopher: int
        :type pickLeftFork: method
        :type pickRightFork: method
        :type eat: method
        :type putLeftFork: method
        :type putRightFork: method
        :rtype: void
        """

        l_s = self.s_list[philosopher]
        r_s = self.s_list[(philosopher + 4) % 5]

        if philosopher % 2 == 0:
            l_s.acquire()
            pickLeftFork()
            r_s.acquire()
            pickRightFork()
            eat()
            putRightFork()
            r_s.release()
            putLeftFork()
            l_s.release()
        else:
            r_s.acquire()
            pickRightFork()
            l_s.acquire()
            pickLeftFork()
            eat()
            putLeftFork()
            l_s.release()
            putRightFork()
            r_s.release()
```
