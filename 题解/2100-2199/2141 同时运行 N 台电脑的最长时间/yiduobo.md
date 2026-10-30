---
title: "2141. 同时运行N台电脑的最长时间"
aliases: ["yiduobo的每日leetcode 2141.同时运行N台电脑的最长时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "leetcode/sorting", "题单/二分算法", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/528885700"
zhihu_id: "528885700"
zhihu_title: "yiduobo的每日leetcode 2141.同时运行N台电脑的最长时间"
question_id: "2141"
question: "同时运行 N 台电脑的最长时间"
problem_url: "https://leetcode.cn/problems/maximum-running-time-of-n-computers/"
difficulty: "Hard"
rating: 2265
created: "2022-06-14T23:25:11+08:00"
updated: "2022-06-14T23:25:11+08:00"
upvotes: 0
comments: 0
---

# 2141. 同时运行N台电脑的最长时间

> **[yiduobo的每日leetcode 2141.同时运行N台电脑的最长时间](https://zhuanlan.zhihu.com/p/528885700) · 知乎 · 2022-06-14 · 赞同 0**
> 力扣：[2141. 同时运行 N 台电脑的最长时间](https://leetcode.cn/problems/maximum-running-time-of-n-computers/) · Hard · 灵茶山艾府：[两种方法：二分答案 / 排序+贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2141.同时运行N太电脑的最长时间

[力扣](https://leetcode.cn/problems/maximum-running-time-of-n-computers/)

很有意思的题目。本题可以将电池电量视为若干个整数，那么问题就变成了给出若干正整数，每次将其中n个正整数减去1，问最多可以减多少轮。

对于这个问题，之前遇到过三个正数且n \= 2的版本，可以利用贪心法来处理。对于本题也可以使用贪心法。很明显，每一轮都应该让最大的n个数减去1，但是用于这里每个数的取值范围都很大，因此不能直接模拟。

不妨从第n大的数入手来考虑。方便起见，先将数组从大到小排序，记为a。

那么在a[n - 1] > a[n]时，所有的操作必然都是让a[0]到a[n - 1]这n个数减去1，直到a[n - 1]等于a[n]为止。

接下来的操作就需要按照 a[0]到a[n - 2]加上a[n - 1] 、a[0]到a[n - 2]加上a[n]这样轮流来执行。这样执行下去可能有两个结果：

1、a[n - 1]、a[n]在若干轮操作后都跌落到了a[n + 1]的水平。此时依然是按照上面的执行方式，不过最后是a[n - 1]、a[n]、a[n + 1]三个数轮流来执行

2、a[n - 2]在若干轮操作后跌落到了a[n]的水平，此时的情况会比较复杂，因为可能出现a[n - 2] \= a[n] \= a[n - 1] + 1的情况，也有可能出现a[n - 2] \= a[n] \= a[n - 1]的情况，后续的执行方式是有多不同的。更进一步的，如果最后相同的数的数量比较多的话，当前面某个数跌落下来之后的后续执行方式就会变得非常复杂。

总体来说，这是一个O(nlogn)的做法，但是具体分析会比较复杂。

除此之外，还有一种O(nlogC)的做法，具体思路就是二分最终答案res。

对于每一个数，若其大于等于res，那么在这res轮操作里面，其最多被消耗掉res。而对于小于res的数，其可能被全部消耗掉。

统计所有数被消耗掉的部分，若这个值大于等于res \* n，那么必然存在一种操作方式可以操作res轮，一个最简单的操作方式就是将这些数列在数组里面，首先把所有大于等于res的数单独分配掉，接下来对于数小于res的数，可以从后续的位置上的数借一些过来填补，这样就能保证完成res轮操作。

反之，若这个值小于res \* n，那么无论如何都没办法操作res轮操作。

我在这里采用的是二分的做法，最后附上python代码：

```python
class Solution(object):
    def maxRunTime(self, n, batteries):
        """
        :type n: int
        :type batteries: List[int]
        :rtype: int
        """

        l = 1
        r = sum(batteries) / n

        while l < r:
            mid = (l + r + 1) >> 1
            cnt = 0
            for b in batteries:
                if b >= mid:
                    cnt += mid
                else:
                    cnt += b
            
            if cnt < n * mid:
                r = mid - 1
            else:
                l = mid
        
        return l
```
