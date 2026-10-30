---
title: "2295. 替换数组中的元素"
aliases: ["yiduobo的每日leetcode 2295.替换数组中的元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/553762425"
zhihu_id: "553762425"
zhihu_title: "yiduobo的每日leetcode 2295.替换数组中的元素"
question_id: "2295"
question: "替换数组中的元素"
problem_url: "https://leetcode.cn/problems/replace-elements-in-an-array/"
difficulty: "Medium"
created: "2022-08-15T00:12:54+08:00"
updated: "2022-08-15T00:13:11+08:00"
upvotes: 0
comments: 0
---

# 2295. 替换数组中的元素

> **[yiduobo的每日leetcode 2295.替换数组中的元素](https://zhuanlan.zhihu.com/p/553762425) · 知乎 · 2022-08-15 · 赞同 0**
> 力扣：[2295. 替换数组中的元素](https://leetcode.cn/problems/replace-elements-in-an-array/) · Medium · 灵茶山艾府：[两种做法：正序（利用特殊条件） or 逆序（更加通用）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2295.替换数组中的元素

[力扣](https://leetcode.cn/problems/replace-elements-in-an-array/)

注意到题目保证了每次操作时，被替换的数必然存在，且替换后的数不存在，又由于初始的数组中没有重复的元素，那么就可以得出结论，数组在任意时刻都不包含重复的元素。

那么就可以使用一个哈希表pos记录每个数值在数组中的位置，当一次替换操作出现时，不妨设当前需要将x替换成y。此时的pos[x]就是x在数组中的下标，替换完成后这个下标的值将变为y，那么就有pos[y] \= pos[x]。同时，x被替换掉之后数组中不再有x存在，因此需要将x从哈希表中去除。

按照题目给出的替换顺序逐个操作，然后根据pos重新构造出最终的答案数组即可。

最后附上python代码：

```python
class Solution(object):
    def arrayChange(self, nums, operations):
        """
        :type nums: List[int]
        :type operations: List[List[int]]
        :rtype: List[int]
        """

        pos_dict = {}
        for index, num in enumerate(nums):
            pos_dict[num] = index
        
        for x, y in operations:
            if x in pos_dict:
                pos_dict[y] = pos_dict[x]
                pos_dict.pop(x)
        
        res = nums[:]
        for num, index in pos_dict.items():
            res[index] = num
        
        return res
```
