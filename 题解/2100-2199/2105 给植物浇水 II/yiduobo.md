---
title: "2105. 给植物浇水II"
aliases: ["yiduobo的每日leetcode 2105.给植物浇水II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/simulation", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/522806712"
zhihu_id: "522806712"
zhihu_title: "yiduobo的每日leetcode 2105.给植物浇水II"
question_id: "2105"
question: "给植物浇水 II"
problem_url: "https://leetcode.cn/problems/watering-plants-ii/"
difficulty: "Medium"
rating: 1507
created: "2022-06-01T00:08:42+08:00"
updated: "2022-06-01T00:08:42+08:00"
upvotes: 0
comments: 0
---

# 2105. 给植物浇水II

> **[yiduobo的每日leetcode 2105.给植物浇水II](https://zhuanlan.zhihu.com/p/522806712) · 知乎 · 2022-06-01 · 赞同 0**
> 力扣：[2105. 给植物浇水 II](https://leetcode.cn/problems/watering-plants-ii/) · Medium · 灵茶山艾府：[相向双指针模拟（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2105.给植物浇水II

[力扣](https://leetcode.cn/problems/watering-plants-ii/)

直接按照题目描述的过程，从两侧开始向中间模拟浇水即可。当alice或bob现有水量不够时，则将对应的水壶加满并更新答案。需要特别注意，若最后alice和bob相遇在同一个位置，需要优先判断二者谁剩下的水更多，然后再判断是否需要加水。

最后附上python代码：

```python
class Solution(object):
    def minimumRefill(self, plants, capacityA, capacityB):
        """
        :type plants: List[int]
        :type capacityA: int
        :type capacityB: int
        :rtype: int
        """

        l = 0
        r = len(plants) - 1
        now_a = capacityA
        now_b = capacityB
        res = 0
        while l < r:
            if now_a < plants[l]:
                now_a = capacityA
                res += 1
            now_a -= plants[l]

            if now_b < plants[r]:
                now_b = capacityB
                res += 1
            now_b -= plants[r]
        
            l += 1
            r -= 1

        if l == r:
            if now_a >= now_b:
                if now_a < plants[l]:
                    res += 1
            elif now_b < plants[l]:
                res += 1

        return res
```
