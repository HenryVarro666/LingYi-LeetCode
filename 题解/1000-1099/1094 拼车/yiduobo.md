---
title: "1094. 拼车"
aliases: ["yiduobo的每日leetcode 1094.拼车"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/373970721"
zhihu_id: "373970721"
zhihu_title: "yiduobo的每日leetcode 1094.拼车"
question_id: "1094"
question: "拼车"
problem_url: "https://leetcode.cn/problems/car-pooling/"
difficulty: "Medium"
rating: 1441
created: "2021-05-20T22:16:33+08:00"
updated: "2021-05-20T22:16:33+08:00"
upvotes: 0
comments: 0
---

# 1094. 拼车

> **[yiduobo的每日leetcode 1094.拼车](https://zhuanlan.zhihu.com/p/373970721) · 知乎 · 2021-05-20 · 赞同 0**
> 力扣：[1094. 拼车](https://leetcode.cn/problems/car-pooling/) · Medium · 灵茶山艾府：[【算法小课堂】差分数组（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1094.拼车

[力扣](https://leetcode-cn.com/problems/car-pooling/)

题目需要我们判断是否在某一时刻车上的人数大于capacity，那么我们可以将所有区间的起点和终点从小到大进行排序，然后一趟扫描，使用一个变量now表示当前状态下车上有多少人。若当前处理到的是某个起点，那么将now加上对应的num，否则将now减去对应的num，然后对比now与capacity的大小即可。

需要注意的是，由于这里可以先下后上，因此这里若某个起点和另一个终点相同，那么在排序时终点的优先级是高于起点的。为了处理这种情况，在排序时可以使用一个小技巧，将起点乘以2，将终点乘以2然后减去1，这样排序的时候就无须分辨起点和终点了。

最后附上python代码：

```python
class Solution(object):
    def carPooling(self, trips, capacity):
        """
        :type trips: List[List[int]]
        :type capacity: int
        :rtype: bool
        """

        info = []
        for num, start, end in trips:
            info.append([num, start * 2])
            info.append([num, end * 2 - 1])
        
        now = 0
        for num, pos in sorted(info, key=lambda d:d[1]):
            if pos % 2 == 0:
                now += num
                if now > capacity:
                    return False
            else:
                now -= num
        
        return True
```
