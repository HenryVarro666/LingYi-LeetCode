---
title: "4038. 计算单个区间中出现的整数数量"
aliases: ["yiduobo的每日leetcode 4038.计算单个区间中出现的整数数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2078639705562804371"
zhihu_id: "2078639705562804371"
zhihu_title: "yiduobo的每日leetcode 4038.计算单个区间中出现的整数数量"
question_id: "4038"
question: "计算单个区间中出现的整数数量"
problem_url: "https://leetcode.cn/problems/count-integers-appearing-in-a-single-block/"
difficulty: "Easy"
created: "2026-09-03T00:28:55+08:00"
updated: "2026-09-03T00:28:55+08:00"
upvotes: 0
comments: 0
---

# 4038. 计算单个区间中出现的整数数量

> **[yiduobo的每日leetcode 4038.计算单个区间中出现的整数数量](https://zhuanlan.zhihu.com/p/2078639705562804371) · 知乎 · 2026-09-03 · 赞同 0**
> 力扣：[4038. 计算单个区间中出现的整数数量](https://leetcode.cn/problems/count-integers-appearing-in-a-single-block/) · Easy · 灵茶山艾府：[简单题，简单做，两种 O(n) 方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4038.计算单个区间中出现的整数数量

<https://leetcode.cn/problems/count-integers-appearing-in-a-single-block/description/>

题目给出一个整数数组nums。

若整数x在nums中的所有位置都处于同一个连续区间内，则称x为特殊整数。

问nums中不同特殊整数的数量。

对于某个整数x，若其在nums中出现的位置连续，那么就意味着其首次出现的位置first[x]到最后一次出现的位置last[x]这一段，一共last[x] - first[x] + 1个元素必须都是x，因此在记录first和last的基础上，额外记录cnt表示x出现的次数，若cnt[x]与last[x] - first[x] + 1相等，就说明x确实是集中在这一段的，否则说明不是。

于是只需一趟遍历，对于nums中的每种元素，计算first、last以及cnt，然后遍历first中的每种整数，根据上面的结论判断其是否为特殊整数即可。

最后附上python代码：

```python
class Solution(object):
    def countSpecialIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        first = {}
        last = {}
        cnt = {}
        for index, v in enumerate(nums):
            if v not in first:
                first[v] = index
                cnt[v] = 0
            
            cnt[v] += 1
            last[v] = index
        
        res = 0
        for v in first:
            if last[v] - first[v] + 1 == cnt[v]:
                res += 1
        
        return res
```
