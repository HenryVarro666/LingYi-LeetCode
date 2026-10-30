---
title: "2615. 等值距离和"
aliases: ["yiduobo的每日leetcode 2615.等值距离和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645927768"
zhihu_id: "645927768"
zhihu_title: "yiduobo的每日leetcode 2615.等值距离和"
question_id: "2615"
question: "等值距离和"
problem_url: "https://leetcode.cn/problems/sum-of-distances/"
difficulty: "Medium"
rating: 1793
created: "2023-07-26T00:42:18+08:00"
updated: "2023-07-26T00:42:18+08:00"
upvotes: 0
comments: 0
---

# 2615. 等值距离和

> **[yiduobo的每日leetcode 2615.等值距离和](https://zhuanlan.zhihu.com/p/645927768) · 知乎 · 2023-07-26 · 赞同 0**
> 力扣：[2615. 等值距离和](https://leetcode.cn/problems/sum-of-distances/) · Medium · 灵茶山艾府：[两种 O(n) 方法：照搬 2602 / 考虑距离之和的增量](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2615.等值距离和

[力扣](https://leetcode.cn/problems/sum-of-distances/)

题目只考虑值相等的位置之间的下标差之和，因此在这里可以先将所有位置按照其位置上的值分别收集起来，然后再各自进行处理。

对于所有值为v的位置，不妨设将这些位置的下标按顺序排好后得到的数组为p，那么对于其中的某个位置p[i]，其对应的计算方法就是abs(p[0] - p[i]) + abs(p[1] - p[i]) + ... + abs(p[m - 1] - p[i])，这里的m为数组p的长度。

由于p是按顺序排好的，那么对于前面的这些项，拆掉绝对值之后就是

p[i] - p[0] + p[i] - p[1] + ... + p[i] - p[i] \= p[i] \* (i + 1) - sum(p[0: i + 1])

即一个乘法与一个前缀和之差

而对于后面的项，拆掉绝对值之后则是

p[i + 1] - p[i] + p[i + 2] - p[i] + ... + p[m - 1] - p[i] \= sum(p[i + 1:]) - p[i] \* (m - 1 - i)

即一个后缀和与一个乘法之差

由于后缀和与前缀和组合起来刚好是数组p的总和，因此可以先一趟遍历，计算数组的总和以及长度，接下来再从头开始遍历，一边计算前缀和，一边套用上面的式子计算其对应的结果。

最后附上python代码：

```python
class Solution(object):
    def distance(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        s = {}
        tot = {}
        for index, v in enumerate(nums):
            s[v] = s.get(v, 0) + index
            tot[v] = tot.get(v, 0) + 1
        
        res = []
        p = {}
        cnt = {}
        for index, v in enumerate(nums):
            p[v] = p.get(v, 0) + index
            cnt[v] = cnt.get(v, 0) + 1
            res.append(cnt[v] * index - p[v] + (s[v] - p[v]) - (tot[v] - cnt[v]) * index)

        return res
```
