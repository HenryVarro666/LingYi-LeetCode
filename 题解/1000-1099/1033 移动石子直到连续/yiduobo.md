---
title: "1033. 移动石子直到连续"
aliases: ["yiduobo的每日leetcode 1033.移动石子直到连续"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/369787931"
zhihu_id: "369787931"
zhihu_title: "yiduobo的每日leetcode 1033.移动石子直到连续"
question_id: "1033"
question: "移动石子直到连续"
problem_url: "https://leetcode.cn/problems/moving-stones-until-consecutive/"
difficulty: "Medium"
rating: 1421
created: "2021-05-05T00:23:09+08:00"
updated: "2021-05-05T00:23:09+08:00"
upvotes: 0
comments: 0
---

# 1033. 移动石子直到连续

> **[yiduobo的每日leetcode 1033.移动石子直到连续](https://zhuanlan.zhihu.com/p/369787931) · 知乎 · 2021-05-05 · 赞同 0**
> 力扣：[1033. 移动石子直到连续](https://leetcode.cn/problems/moving-stones-until-consecutive/) · Medium · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1033.移动石子直到连续

[力扣](https://leetcode-cn.com/problems/moving-stones-until-consecutive/)

我们分别讨论最多和最少的情况。由于石子的名称并不影响最终结果，那么为了方便起见，我们不妨规定a \< b \< c，若不满足这个条件，则交换a、b、c。

首先讨论最多可以移动多少次：

每一次移动，a到c之间的距离至少要减少1。那么初始情况下，a到c之间的距离为c - a + 1，另外还需要去除a、b、c这三个位置，因此实际上空闲的距离就是c - a - 2，那么按照每次减少1来移动，最多可以移动c - a - 2次。

接下来讨论最少需要移动多少次：

1、若一开始就有a \= b - 1，且b \= c - 1

那么说明无需移动，答案为0

2、若满足a \= b - 1但不满足b \= c - 1

那么我们就需要将c移动到b + 1，因此答案为1

3、若满足b \= c - 1但不满足a \= b - 1

与情况2类似，我们就需要将a移动到b - 1，因此答案为1

4、若满足a \= b - 2且不满足b \= c - 1

那么我们可以将c移动到b - 1，因此答案为1

5、若满足b \= c - 2且不满足a \= b - 1

那么我们可以将a移动到c - 1，因此答案为1

6、其他情况

此时a到b以及b到c之间的距离都至少需要一次移动才能填上，因此我们可以将a移动到b - 1，将c移动到b + 1，那么答案就是2

最后附上python代码：

```python
class Solution(object):
    def numMovesStones(self, a, b, c):
        """
        :type a: int
        :type b: int
        :type c: int
        :rtype: List[int]
        """

        if a > b:
            a, b = b, a
        if a > c:
            a, c = c, a
        if b > c:
            b, c = c, b
        
        ma = c - a - 2
        if a == b - 1:
            if c == b + 1:
                mi = 0
            else:
                mi = 1
        elif c == b + 1:
            mi = 1
        elif a == b - 2 or c == b + 2:
            mi = 1
        else:
            mi = 2
        
        return [mi, ma]
```
