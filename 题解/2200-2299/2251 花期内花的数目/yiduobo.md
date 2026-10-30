---
title: "2251. 花期内花的数目"
aliases: ["yiduobo的每日leetcode 2251.花期内花的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-search", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/546927073"
zhihu_id: "546927073"
zhihu_title: "yiduobo的每日leetcode 2251.花期内花的数目"
question_id: "2251"
question: "花期内花的数目"
problem_url: "https://leetcode.cn/problems/number-of-flowers-in-full-bloom/"
difficulty: "Hard"
rating: 2022
created: "2022-07-27T22:03:31+08:00"
updated: "2022-07-27T22:03:31+08:00"
upvotes: 0
comments: 0
---

# 2251. 花期内花的数目

> **[yiduobo的每日leetcode 2251.花期内花的数目](https://zhuanlan.zhihu.com/p/546927073) · 知乎 · 2022-07-27 · 赞同 0**
> 力扣：[2251. 花期内花的数目](https://leetcode.cn/problems/number-of-flowers-in-full-bloom/) · Hard · 灵茶山艾府：[两种方法：二分/差分（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2251.花期内花的数目

[力扣](https://leetcode.cn/problems/number-of-flowers-in-full-bloom/)

注意到题目中各个时间点的取值范围都很大，因此不能直接模拟。由于看花的人并不关心看到了哪些花，而是只需要知道当前花开的数目，因此可以使用一个变量cnt统计每个人来的时候开花的数目。cnt只会在花开和花落时被更新，而对于其他的时间点来说是不需要关心cnt的，因此在这里只需要将花开、花落和看花人到达这三种时间点抽出来，然后从小到大排序之后一趟遍历。

对于当前遍历到的时间点：

1、如果是花开，那么将cnt加上1

2、如果是花落，那么将cnt减去1

3、如果是看花人到达，那么使用cnt更新这个人对应的答案

需要注意的是，按照题目的描述，若三种事件同时发生，那么优先级应该是花开 -> 看花人到达 -> 花落，因此在一开始排序的时候可以引入第二优先级，保证同一时间点的三种事件是按照上面描述的顺序排列的。

最后附上python代码：

```python
class Solution(object):
    def fullBloomFlowers(self, flowers, persons):
        """
        :type flowers: List[List[int]]
        :type persons: List[int]
        :rtype: List[int]
        """

        m = len(flowers)
        n = len(persons)

        res = [0] * n

        time_points = []
        for start, end in flowers:
            time_points.append([start, -1])
            time_points.append([end, n])
        
        for index, person in enumerate(persons):
            time_points.append([person, index])
        
        cnt = 0
        for t, index in sorted(time_points):
            if index == -1:
                cnt += 1
            elif index == n:
                cnt -= 1
            else:
                res[index] = cnt
        
        return res
```
