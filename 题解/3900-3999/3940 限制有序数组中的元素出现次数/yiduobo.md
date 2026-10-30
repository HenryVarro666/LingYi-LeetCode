---
title: "3940. 限制有序数组中的元素出现次数"
aliases: ["yiduobo的每日leetcode 3940.限制有序数组中的元素出现次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/stack", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2043456466254811250"
zhihu_id: "2043456466254811250"
zhihu_title: "yiduobo的每日leetcode 3940.限制有序数组中的元素出现次数"
question_id: "3940"
question: "限制有序数组中的元素出现次数"
problem_url: "https://leetcode.cn/problems/limit-occurrences-in-sorted-array/"
difficulty: "Easy"
created: "2026-05-30T02:09:07+08:00"
updated: "2026-05-30T02:09:08+08:00"
upvotes: 3
comments: 0
---

# 3940. 限制有序数组中的元素出现次数

> **[yiduobo的每日leetcode 3940.限制有序数组中的元素出现次数](https://zhuanlan.zhihu.com/p/2043456466254811250) · 知乎 · 2026-05-30 · 赞同 3**
> 力扣：[3940. 限制有序数组中的元素出现次数](https://leetcode.cn/problems/limit-occurrences-in-sorted-array/) · Easy · 灵茶山艾府：[双指针原地做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3940.限制有序数组中的元素出现次数

<https://leetcode.cn/problems/limit-occurrences-in-sorted-array/>

题目给出一个按升序排序的整数数组nums，以及一个整数k。

要求返回一个数组，使得每个不同元素最多出现k次，同时保持nums中元素的相对顺序不变。如果可能，尽量使用原地算法解决问题。

题目中的nums是按升序排序的，这也就意味着相同的元素在nums中是连续出现的，以此可以从左到右对nums进行一趟遍历，同时使用一个变量cnt记录当前元素出现的次数。

若当前元素与前一个元素不同，那么就将cnt置为1，否则将cnt加上1。

接下来，若cnt小于等于k，那么说明当前元素应该保留，否则说明应该删去。由于需要使用原地算法解决问题，在这里就可以使用另一个变量p记录最终的nums中已经确认保留的元素数目，当cnt小于等于k时，就将当前元素填充到nums[p]然后将p加上1。

遍历完成后，nums[:p]就是最终保留下来的元素形成的数组，此时将后续所有的元素从nums中移除掉就行了。

最后附上python代码：

```python
class Solution(object):
    def limitOccurrences(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        p = 0
        cnt = 0
        pre = None
        for v in nums:
            if v == pre:
                cnt += 1
            else:
                cnt = 1
            
            if cnt <= k:
                nums[p] = v
                p += 1
            
            pre = v
        
        while len(nums) > p:
            nums.pop()
        
        return nums
```
