---
title: "3595. 一次或两次"
aliases: ["yiduobo的每日leetcode 3595.一次或两次"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1940568026870183139"
zhihu_id: "1940568026870183139"
zhihu_title: "yiduobo的每日leetcode 3595.一次或两次"
question_id: "3595"
question: "一次或两次"
problem_url: "https://leetcode.cn/problems/once-twice/"
created: "2025-08-18T02:33:44+08:00"
updated: "2025-08-18T02:33:44+08:00"
upvotes: 0
comments: 0
---

# 3595. 一次或两次

> **[yiduobo的每日leetcode 3595.一次或两次](https://zhuanlan.zhihu.com/p/1940568026870183139) · 知乎 · 2025-08-18 · 赞同 0**
> 力扣：[3595. 一次或两次](https://leetcode.cn/problems/once-twice/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3595.一次或两次

[3595. 一次或两次 - 力扣（LeetCode）](https://leetcode.cn/problems/once-twice/description/)

题目给出一个整数数组nums，在这个数组中，有一个元素仅出现一次，有一个元素恰好出现两次，其他所有的元素都出现了恰好三次。

现在要求找出其中出现一次和两次的这两个元素，必须在O(n)的时间以及O(1)的空间内完成。

之前137题的加强版，处理方法也是类似的。建议先看一看137题的处理方法，然后才能比较方便地看明白本题是怎么做的。

[yiduobo的每日leetcode 137.只出现一次的数字II](https://zhuanlan.zhihu.com/p/141889925)

与137题类似，本题依然是通过计算所有二进制位上1的数量对3的余数，来确定只出现一次和出现两次的元素特有的mask。需要注意的是，本题只能确定特有的mask，但是无法直接定位到这两个数，理由是一个出现一次的元素，配合上另一个出现两次的元素，可以让某些二进制位上刚好达到3次，这样一来这些原本为1的位就被模3消除掉了。基于这一点，在得到了这两个元素特有的mask之后，还需要进行一趟遍历，从nums中先选出契合这些mask的元素，然后再通过相同的方法，统计二进制位上1的数量对3的余数，从而找出最终答案。

最后附上python代码：

```python
class Solution(object):
    def onceTwice(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        def nxt(once, twice, num):
            return ~twice & (once ^ num), (once ^ twice) & (twice ^ num)

        once, twice = 0, 0
        for num in nums:
            once, twice = nxt(once, twice, num)

        hit_once_once, hit_once_twice = 0, 0
        hit_twice_once, hit_twice_twice = 0, 0
        for num in nums:
            if num & once == once and num & twice == 0:
                hit_once_once, hit_once_twice = nxt(hit_once_once, hit_once_twice, num)
            if num & twice == twice and num & once == 0:
                hit_twice_once, hit_twice_twice = nxt(hit_twice_once, hit_twice_twice, num)

        return hit_once_once, hit_twice_twice
```
