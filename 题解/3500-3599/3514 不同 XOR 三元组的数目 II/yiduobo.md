---
title: "3514. 不同XOR三元组的数目II"
aliases: ["yiduobo的每日leetcode 3514.不同XOR三元组的数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/math", "leetcode/enumeration", "题单/位运算", "题单/数学算法", "题单/位运算/九-其他", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902530757118923526"
zhihu_id: "1902530757118923526"
zhihu_title: "yiduobo的每日leetcode 3514.不同XOR三元组的数目II"
question_id: "3514"
question: "不同 XOR 三元组的数目 II"
problem_url: "https://leetcode.cn/problems/number-of-unique-xor-triplets-ii/"
difficulty: "Medium"
created: "2025-05-06T23:19:17+08:00"
updated: "2025-05-06T23:19:17+08:00"
upvotes: 0
comments: 0
---

# 3514. 不同XOR三元组的数目II

> **[yiduobo的每日leetcode 3514.不同XOR三元组的数目II](https://zhuanlan.zhihu.com/p/1902530757118923526) · 知乎 · 2025-05-06 · 赞同 0**
> 力扣：[3514. 不同 XOR 三元组的数目 II](https://leetcode.cn/problems/number-of-unique-xor-triplets-ii/) · Medium · 灵茶山艾府：[循环优化，附 O(UlogU) FWT 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3514.不同XOR三元组的数目II

[3514. 不同 XOR 三元组的数目 II - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-unique-xor-triplets-ii/description/)

题目给出一个整数数组nums，nums的长度不超过1500以及其中的元素值都不超过1500。

XOR三元组的定义为三个元素(nums[i], nums[j], nums[k])的异或值nums[i] XOR nums[j] XOR nums[k]，其中i \<\= j \<\= k。

问所有可能的不同XOR值的数量。

本题与上题略有不同，nums不再是1到n的某个排列，那么上一题类似构造的处理方法就行不通了。不过好在本题的数据规模较小，可以直接暴力计算。

使用三个集合one、two、three记录从当前前缀中取出1、2、3个元素异或后可以得到的所有结果，接下来只需对nums进行一趟遍历，对于当前遍历到的v，先将v加入到one，然后对于one中的所有元素pre，将pre ^ v加入到two中，最后对于two中的所有元素pre，将pre ^ v加入到three中即可。

计算完成后，three的长度即为最终答案。

值得一提的是，上面算法成立的前提是nums中元素值都不超过1500，这也就意味着所有的异或结果都在0到2047之间，因此即使暴力遍历two中的所有异或结果也不会有时间复杂度方面的问题。

最后附上python代码：

```python
class Solution(object):
    def uniqueXorTriplets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        one = set()
        two = set()
        three = set()
        for v in list(set(nums)):
            one.add(v)
            
            for pre in one:
                two.add(pre ^ v)
            
            for pre in two:
                three.add(pre ^ v)
        
        return len(three)
```
