---
title: "3080. 执行操作标记数组中的元素"
aliases: ["yiduobo的每日leetcode 3080.执行操作标记数组中的元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/698423190"
zhihu_id: "698423190"
zhihu_title: "yiduobo的每日leetcode 3080.执行操作标记数组中的元素"
question_id: "3080"
question: "执行操作标记数组中的元素"
problem_url: "https://leetcode.cn/problems/mark-elements-on-array-by-performing-queries/"
difficulty: "Medium"
created: "2024-05-18T00:22:48+08:00"
updated: "2024-05-18T00:22:48+08:00"
upvotes: 2
comments: 0
---

# 3080. 执行操作标记数组中的元素

> **[yiduobo的每日leetcode 3080.执行操作标记数组中的元素](https://zhuanlan.zhihu.com/p/698423190) · 知乎 · 2024-05-18 · 赞同 2**
> 力扣：[3080. 执行操作标记数组中的元素](https://leetcode.cn/problems/mark-elements-on-array-by-performing-queries/) · Medium · 灵茶山艾府：[对下标数组稳定排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3080.执行操作标记数组中的元素

[. - 力扣（LeetCode）](https://leetcode.cn/problems/mark-elements-on-array-by-performing-queries/description/)

题目中每一轮标记操作(index, k)都将标记下标index所在的数字以及k个数值最小且没有被标记过的数字，于是可以先将数组下标按照数值为第一关键字，下标值自身为第二关键字从小到大进行排序，得到数组sorted_index，那么k对应的标记操作就会按照sorted_index中的顺序进行，在这里可以使用一个变量p表示sorted_index中下一个被标记的下标。

又由于标记k个最小值这个操作不能进行重复标记，于是还需要使用一个集合marked记录已经被标记过的下标。另外由于题目要求的是每轮标记操作后未被标记的数值之和，那么还需要使用一个变量s记录未被标记的数值之和。接下来就只需要遍历queries，对于当前的标记操作(index, k)：

1、首先考虑index。若index没有被标记过，那么将其加入到marked，并从s中减去nums[index]。

2、接下来考虑k。从当前的p开始，找出sorted_index中下一个没有被标记过的下标，将其加入到marked中，并从s中将其减去，再将p加上1，k减去1。重复此过程直到p来到数组末尾或者k等于0位置。

每执行完一轮操作，都需要将当前的s加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def unmarkedSumArray(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        s = sum(nums)
        n = len(nums)
        sorted_index = sorted(range(n), key=lambda d:(nums[d], d))
        marked = set()

        p = 0
        res = []

        for index, k in queries:
            if index not in marked:
                marked.add(index)
                s -= nums[index]
            
            while k > 0 and p < n:
                if sorted_index[p] in marked:
                    p += 1
                    continue
                
                marked.add(sorted_index[p])
                s -= nums[sorted_index[p]]
                p += 1
                k -= 1

            res.append(s)

        return res
```
