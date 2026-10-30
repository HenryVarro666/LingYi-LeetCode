---
title: "3072. 将元素分配到两个数组中II"
aliases: ["yiduobo的每日leetcode 3072.将元素分配到两个数组中II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/697566177"
zhihu_id: "697566177"
zhihu_title: "yiduobo的每日leetcode 3072.将元素分配到两个数组中II"
question_id: "3072"
question: "将元素分配到两个数组中 II"
problem_url: "https://leetcode.cn/problems/distribute-elements-into-two-arrays-ii/"
difficulty: "Hard"
rating: 2053
created: "2024-05-13T22:41:31+08:00"
updated: "2024-05-13T22:41:31+08:00"
upvotes: 1
comments: 0
---

# 3072. 将元素分配到两个数组中II

> **[yiduobo的每日leetcode 3072.将元素分配到两个数组中II](https://zhuanlan.zhihu.com/p/697566177) · 知乎 · 2024-05-13 · 赞同 1**
> 力扣：[3072. 将元素分配到两个数组中 II](https://leetcode.cn/problems/distribute-elements-into-two-arrays-ii/) · Hard · 灵茶山艾府：[树状数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3072.将元素分配到两个数组中II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/distribute-elements-into-two-arrays-ii/)

本题中分配元素的方案取决于当前两个数组中分别又多少个元素严格大于待添加的元素val，可以先将其转化为当前数组的长度减去数组中小于等于待添加的元素的数量。

这个问题很适合使用树状数组求解，不过本题中的数值取值范围很大，不能直接使用。好在本题只需要关注数值的相对大小，于是可以先将数组排序，然后建立数字到序的映射，然后就可以在序上使用树状数组求解了。

最后附上python代码：

```python
class Solution(object):
    def resultArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        mapping = {}
        rank = 1
        for v in sorted(nums):
            if v not in mapping:
                mapping[v] = rank
                rank += 1
        
        def add(f, x):
            while x < rank:
                f[x] += 1
                x += x & -x
        
        def get(f, x):
            s = 0
            while x > 0:
                s += f[x]
                x -= x & -x
            return s
        
        arr1 = [nums[0]]
        f1 = [0] * rank
        add(f1, mapping[nums[0]])
        arr2 = [nums[1]]
        f2 = [0] * rank
        add(f2, mapping[nums[1]])
        for v in nums[2:]:
            cnt1 = len(arr1) - get(f1, mapping[v])
            cnt2 = len(arr2) - get(f2, mapping[v])
            if cnt1 > cnt2 or (cnt1 == cnt2 and len(arr1) <= len(arr2)):
                arr1.append(v)
                add(f1, mapping[v])
            else:
                arr2.append(v)
                add(f2, mapping[v])
        
        return arr1 + arr2
```
