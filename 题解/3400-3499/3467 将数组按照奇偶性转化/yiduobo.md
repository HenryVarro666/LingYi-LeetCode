---
title: "3467. 将数组按照奇偶性转化"
aliases: ["yiduobo的每日leetcode 3467.将数组按照奇偶性转化"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1895961148630729591"
zhihu_id: "1895961148630729591"
zhihu_title: "yiduobo的每日leetcode 3467.将数组按照奇偶性转化"
question_id: "3467"
question: "将数组按照奇偶性转化"
problem_url: "https://leetcode.cn/problems/transform-array-by-parity/"
difficulty: "Easy"
created: "2025-04-16T22:10:35+08:00"
updated: "2025-04-16T22:10:35+08:00"
upvotes: 0
comments: 0
---

# 3467. 将数组按照奇偶性转化

> **[yiduobo的每日leetcode 3467.将数组按照奇偶性转化](https://zhuanlan.zhihu.com/p/1895961148630729591) · 知乎 · 2025-04-16 · 赞同 0**
> 力扣：[3467. 将数组按照奇偶性转化](https://leetcode.cn/problems/transform-array-by-parity/) · Easy · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3467.将数组按照奇偶性转化

[3467. 将数组按照奇偶性转化 - 力扣（LeetCode）](https://leetcode.cn/problems/transform-array-by-parity/description/)

题目给出一个整数数组nums，需要将其中每个偶数替换为0，将奇数替换为1，然后按非递减的顺序排序。

题目要求最后的数组按照非递减的顺序排序，又由于题目中的每个数都被替换成了0或者1，那么最后得到的数组必然由左侧若干个0和右侧若干个1组成，其中0的数目为nums中偶数的数目，而1的数组则为剩下奇数的数目，于是只需一趟遍历，计算nums中偶数的数目，然后构造最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def transformArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        even = 0
        for v in nums:
            if v % 2 == 0:
                even += 1
        
        return [0] * even + [1] * (len(nums) - even)
```
