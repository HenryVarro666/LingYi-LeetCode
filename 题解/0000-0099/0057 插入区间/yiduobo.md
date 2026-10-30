---
title: "57. 插入区间"
aliases: ["yiduobo的每日leetcode 57.插入区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/128129517"
zhihu_id: "128129517"
zhihu_title: "yiduobo的每日leetcode 57.插入区间"
question_id: "57"
question: "插入区间"
problem_url: "https://leetcode.cn/problems/insert-interval/"
created: "2020-04-09T23:12:54+08:00"
updated: "2020-04-09T23:12:54+08:00"
upvotes: 0
comments: 0
---

# 57. 插入区间

> **[yiduobo的每日leetcode 57.插入区间](https://zhuanlan.zhihu.com/p/128129517) · 知乎 · 2020-04-09 · 赞同 0**
> 力扣：[57. 插入区间](https://leetcode.cn/problems/insert-interval/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

57.插入区间<https://leetcode-cn.com/problems/insert-interval/>

依然是区间判断的题目，不过这里暂时需要插入的区间和现有区间之间哪个靠左，因此需要新的判断方式。

由于题目要求对于重叠的区间进行合并，那么对于待插入区间a与现有区间b，在先后顺序和是否重叠上有三种情况需要处理：

1、a与b不重叠，且a在b的左侧。此时就有a.right \< b.left。

2、a与b不重叠，且a在b的右侧。同样的，此时有a.left > b.right。

3、a与b部分重叠。此时需要执行合并区间，那么就有a.left \= min(a.left, b.left)以及a.right \= max(a.right, b.right)。

于是我们可以从左往右扫描每个区间b：

1、如果a已经插入完毕，那么无需进行任何操作，直接将b加入答案即可。

2、如果a未插入完毕，且a在b的左侧，那么说明a最终的位置就是在b的左侧，此时将a与b加入答案即可。

3、如果a未插入完毕，且a在b的右侧，说明此时b对a无影响，将b加入答案，但是a还需要与后续的b继续进行比较。

4、如果a未插入完毕，且a与b部分重叠，那么合并a与b即可。

需要注意的是，如果a始终都未插入进来，那么说明a应该加入到答案的末尾。

最后附上python代码，其中finish_flag表示a是否已经插入进来了：

```python
class Solution(object):
    def insert(self, intervals, newInterval):
        """
        :type intervals: List[List[int]]
        :type newInterval: List[int]
        :rtype: List[List[int]]
        """

        res = []
        finish_flag = False
        for index, interval in enumerate(intervals):
            if finish_flag:
                res.append(interval)
            elif newInterval[1] < interval[0]:
                res.append(newInterval)
                res.append(interval)
                finish_flag = True
            elif newInterval[0] > interval[1]:
                res.append(interval)
            else:
                newInterval[0] = min(newInterval[0], interval[0])
                newInterval[1] = max(newInterval[1], interval[1])

        if not finish_flag:
            res.append(newInterval)

        return res
```
