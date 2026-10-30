---
title: "349. 两个数组的交集 & 350. 两个数组的交集II"
aliases: ["yiduobo的每日leetcode 349.两个数组的交集 && 350.两个数组的交集II", "349. 两个数组的交集", "350. 两个数组的交集II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163660156"
zhihu_id: "163660156"
zhihu_title: "yiduobo的每日leetcode 349.两个数组的交集 && 350.两个数组的交集II"
question_id: ["349", "350"]
question: ["两个数组的交集", "两个数组的交集 II"]
problem_url: ["https://leetcode.cn/problems/intersection-of-two-arrays/", "https://leetcode.cn/problems/intersection-of-two-arrays-ii/"]
difficulty: "Easy"
created: "2020-07-25T16:50:44+08:00"
updated: "2020-07-25T16:50:44+08:00"
upvotes: 0
comments: 0
---

# 349. 两个数组的交集 & 350. 两个数组的交集II

> **[yiduobo的每日leetcode 349.两个数组的交集 && 350.两个数组的交集II](https://zhuanlan.zhihu.com/p/163660156) · 知乎 · 2020-07-25 · 赞同 0**
> 力扣：[349. 两个数组的交集](https://leetcode.cn/problems/intersection-of-two-arrays/) · Easy · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/Go/JS/Rust）](../0349%20两个数组的交集/灵茶山艾府.md)
> 力扣：[350. 两个数组的交集 II](https://leetcode.cn/problems/intersection-of-two-arrays-ii/) · Easy · 灵茶山艾府：[一次遍历，简洁写法，附进阶问题解答（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

349.两个数组的交集<https://leetcode-cn.com/problems/intersection-of-two-arrays/>

350.两个数组的交集II <https://leetcode-cn.com/problems/intersection-of-two-arrays-ii/>

都是比较基础的题目。

349不需要考虑出现的次数，因此使用set统计一下即可。350则需要使用dict来进行统计。

另外，在350中，如果两个数组已经排好序了，可以使用类似二路归并的做法来进行统计。

最后附上python代码：

349：

```python
class Solution(object):
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        num_set = set()
        for num in nums1:
            num_set.add(num)

        res = []
        for num in nums2:
            if num in num_set:
                res.append(num)
                num_set.remove(num)

        return res
```

350：

```python
class Solution(object):
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """

        num_dict1 = {}
        for num in nums1:
            num_dict1[num] = num_dict1.get(num, 0) + 1

        num_dict2 = {}
        for num in nums2:
            num_dict2[num] = num_dict2.get(num, 0) + 1
        
        res = []
        for num, weight in num_dict1.items():
            if num in num_dict2:
                res.extend([num] * min(weight, num_dict2[num]))

        return res
```
