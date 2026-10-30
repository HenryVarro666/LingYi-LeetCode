---
title: "1865. 找出和为指定值的下标对"
aliases: ["yiduobo的每日leetcode 1865.找出和为指定值的下标对"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/473880128"
zhihu_id: "473880128"
zhihu_title: "yiduobo的每日leetcode 1865.找出和为指定值的下标对"
question_id: "1865"
question: "找出和为指定值的下标对"
problem_url: "https://leetcode.cn/problems/finding-pairs-with-a-certain-sum/"
difficulty: "Medium"
created: "2022-02-28T23:28:35+08:00"
updated: "2022-02-28T23:28:35+08:00"
upvotes: 0
comments: 0
---

# 1865. 找出和为指定值的下标对

> **[yiduobo的每日leetcode 1865.找出和为指定值的下标对](https://zhuanlan.zhihu.com/p/473880128) · 知乎 · 2022-02-28 · 赞同 0**
> 力扣：[1865. 找出和为指定值的下标对](https://leetcode.cn/problems/finding-pairs-with-a-certain-sum/) · Medium · 灵茶山艾府：[维护每个元素的出现次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1865.找出和为指定值的下标对

[力扣](https://leetcode-cn.com/problems/finding-pairs-with-a-certain-sum/)

第一题两数之和的online版，在这里如果想继续利用单调性使用双指针来求解，就需要动态保持nums2的有序性，可能需要用到平衡二叉树这类东西来维护nums2的序，是比较麻烦的。除此之外，则还可以使用哈希表来储存nums2中每个数出现的次数，然后在计算时枚举nums1中每个数num，去哈希表中查找nums2中有多少个数等于tot - num，在这里显然是更合适的做法。

当然，一个数一旦进了哈希表就丢失了这个数在nums2中的下标信息，但是由于更新时基于数组下标更新的，因此也仍然需要维护nums2本身，并在修改到来更新nums2本身以及哈希表。

最后附上python代码：

```python
class FindSumPairs(object):

    def __init__(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        """
        self.nums1 = nums1[:]
        self.nums2 = nums2[:]
        self.num_dict = {}
        for num in self.nums2:
            self.num_dict[num] = self.num_dict.get(num, 0) + 1

    def add(self, index, val):
        """
        :type index: int
        :type val: int
        :rtype: None
        """
        self.num_dict[self.nums2[index]] -= 1
        self.nums2[index] += val
        self.num_dict[self.nums2[index]] = self.num_dict.get(self.nums2[index], 0) + 1

    def count(self, tot):
        """
        :type tot: int
        :rtype: int
        """
        res = 0 
        for num in self.nums1:
            res += self.num_dict.get(tot - num, 0)
        
        return res

# Your FindSumPairs object will be instantiated and called as such:
# obj = FindSumPairs(nums1, nums2)
# obj.add(index,val)
# param_2 = obj.count(tot)
```
