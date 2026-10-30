---
title: "264. 丑数II"
aliases: ["yiduobo的每日leetcode 264.丑数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/151845284"
zhihu_id: "151845284"
zhihu_title: "yiduobo的每日leetcode 264.丑数II"
question_id: "264"
question: "丑数II"
problem_url: "https://leetcode.cn/problems/ugly-number-ii/"
created: "2020-06-29T22:21:36+08:00"
updated: "2020-06-29T22:21:36+08:00"
upvotes: 0
comments: 0
---

# 264. 丑数II

> **[yiduobo的每日leetcode 264.丑数II](https://zhuanlan.zhihu.com/p/151845284) · 知乎 · 2020-06-29 · 赞同 0**
> 力扣：[264. 丑数II](https://leetcode.cn/problems/ugly-number-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

264.丑数II <https://leetcode-cn.com/problems/ugly-number-ii/>

这一题要求我们按照从小到大的顺序生成丑数，那么难点就在于不好确定每个丑数生成的丑数的大小。

对于两个丑数A和B，排除掉重复的情况后最多可以生成A\*2，A\*3，A\*5，B\*2，B\*3，B\*5这6个丑数。

不妨设A\<B，那么此时我们只能确定下列几组大小关系：

A\*2 \< A\*3 \< A\*5

B\*2 \< B\*3 \< B\*5

A\*2 \< B\*2

A\*3 \< B\*3

A\*5 \< B\*5

于是一个很自然的想法就是使用三个队列，分别将乘2，乘3以及乘5的结果保存起来。如果我们是按照从小到大的顺序使用丑数生成新的丑数，那么这三个队列一定是单调递增的。

当需要选取当前最小的丑数时，我们就可以对比这三个队列的队首元素，选取其中最小的那个，这个数必然是此时最小的丑数，然后用这个丑数分别乘2、乘3、乘5并加入到这三个队列中即可。

需要注意的是，若当前丑数乘出来的结果已经在这三个队列中，那么就不应该再次将这个结果加入队列中了，于是还需要一个set来进行这个判断。

由于每个丑数至多只会被加入队列一次，也至多只会进行三次乘法，而处理到第n个丑数时就得到了答案，因此最终的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def nthUglyNumber(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1:
            return 1

        num_list = [[], [], []]
        pos = [0, 0, 0]
        num_set = set()

        now = 1
        for index in range(1, n):
            for index, multi in enumerate([2, 3, 5]):
                if now * multi not in num_set:
                    num_set.add(now * multi)
                    num_list[index].append(now * multi)

            now = None
            next_pos = None
            for index in range(3):
                if now is None or now > num_list[index][pos[index]]:
                    now = num_list[index][pos[index]]
                    next_pos = index

            pos[next_pos] += 1

        return now
```
