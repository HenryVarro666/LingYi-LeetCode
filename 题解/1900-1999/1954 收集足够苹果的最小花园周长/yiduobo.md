---
title: "1954. 收集足够苹果的最小花园周长"
aliases: ["yiduobo的每日leetcode 1954.收集足够苹果的最小花园周长"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/492259107"
zhihu_id: "492259107"
zhihu_title: "yiduobo的每日leetcode 1954.收集足够苹果的最小花园周长"
question_id: "1954"
question: "收集足够苹果的最小花园周长"
problem_url: "https://leetcode.cn/problems/minimum-garden-perimeter-to-collect-enough-apples/"
difficulty: "Medium"
rating: 1759
created: "2022-04-02T18:28:15+08:00"
updated: "2022-04-02T18:28:15+08:00"
upvotes: 0
comments: 0
---

# 1954. 收集足够苹果的最小花园周长

> **[yiduobo的每日leetcode 1954.收集足够苹果的最小花园周长](https://zhuanlan.zhihu.com/p/492259107) · 知乎 · 2022-04-02 · 赞同 0**
> 力扣：[1954. 收集足够苹果的最小花园周长](https://leetcode.cn/problems/minimum-garden-perimeter-to-collect-enough-apples/) · Medium · 灵茶山艾府：[【图解】O(1) 做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1954.收集足够苹果的最小花园周长

[力扣](https://leetcode-cn.com/problems/minimum-garden-perimeter-to-collect-enough-apples/)

题目保证了花园是以(0, 0)为中心的正方形，那么不妨将边长从2开始一层一层把每个正方形的边框拎出来，计算边框上苹果的总数，然后每个边框上苹果数之后就是花园里的总苹果数。

对于边长为2l的正方形框，其上方边框的坐标序列为

(-l, -l)，(-l + 1, -l)，...，(0, -l)，(1, -l)，...，(l - 1, -l)，(l, -l)

苹果总数为

2l + (2l - 1) + ... + (l + 1) + l + (l + 1) + ... + (2l - 1) + 2l

可以视为两个等差数列求和，和为

(3l + 2) \* l

对于右侧，可以认为是上侧横纵坐标互换，因此最终也是(3l + 2) \* l个苹果

而对于左侧，则可以认为是右侧横坐标取反；对于下侧，则是上侧纵坐标取反

因此单条边上的苹果总数就是(3l + 2) \* l个，而对于整个边框，则是(3l + 2) \* l \* 4 - 8l \= 12 \* l^2。这里减去8l的理由是四个角上的苹果都计算了两次。

单个边框上的苹果数是12 \* l^2，那么边长为2l的正方形里面一共就有

12 \* (1^2 + 2^2 + ... + l^2)

后面是平方和公式，有(1^2 + 2^2 + ... + l^2) \= l \* (l + 1) \* (2l + 1) / 6

因此正方形里苹果的总和就是2 \* l \* (l + 1) \* (2l + 1)

接下来为了找到边长最小的花园，只需要二分l的长度，根据上面公式计算苹果总数，与neededApples进行比较得到l的最小值。最终答案就是2l \* 4 \= 8l

最后附上python代码：

```python
class Solution(object):
    def minimumPerimeter(self, neededApples):
        """
        :type neededApples: int
        :rtype: int
        """
        
        l = 1
        r = neededApples

        while l < r:
            mid = (l + r) >> 1
            if 2 * mid * (mid + 1) * (2 * mid + 1) < neededApples:
                l = mid + 1
            else:
                r = mid
        
        return l * 8
```
