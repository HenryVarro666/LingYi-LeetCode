---
title: "1436. 旅行终点站"
aliases: ["yiduobo的每日leetcode 1436.旅行终点站"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/graph", "leetcode/hash-table", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/409328216"
zhihu_id: "409328216"
zhihu_title: "yiduobo的每日leetcode 1436.旅行终点站"
question_id: "1436"
question: "旅行终点站"
problem_url: "https://leetcode.cn/problems/destination-city/"
difficulty: "Easy"
created: "2021-09-11T15:17:47+08:00"
updated: "2021-09-11T15:17:47+08:00"
upvotes: 0
comments: 0
---

# 1436. 旅行终点站

> **[yiduobo的每日leetcode 1436.旅行终点站](https://zhuanlan.zhihu.com/p/409328216) · 知乎 · 2021-09-11 · 赞同 0**
> 力扣：[1436. 旅行终点站](https://leetcode.cn/problems/destination-city/) · Easy · 灵茶山艾府：[两种方法：两次遍历/一次遍历（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1436.旅行终点站

[力扣](https://leetcode-cn.com/problems/destination-city/)

比价基础的题目，找出只进不出的那个城市即可。

最后附上python代码：

```python
class Solution(object):
    def destCity(self, paths):
        """
        :type paths: List[List[str]]
        :rtype: str
        """

        ind = {}
        for a, b in paths:
            if a not in ind:
                ind[a] = 0
            ind[a] += 1

            if b not in ind:
                ind[b] = 0
        
        for city in ind:
            if ind[city] == 0:
                return city
```
