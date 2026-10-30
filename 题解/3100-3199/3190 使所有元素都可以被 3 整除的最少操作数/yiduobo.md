---
title: "3190. 使所有元素都可以被3整除的最少操作数"
aliases: ["yiduobo的每日leetcode 3190.使所有元素都可以被3整除的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706509895"
zhihu_id: "706509895"
zhihu_title: "yiduobo的每日leetcode 3190.使所有元素都可以被3整除的最少操作数"
question_id: "3190"
question: "使所有元素都可以被 3 整除的最少操作数"
problem_url: "https://leetcode.cn/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/"
difficulty: "Easy"
created: "2024-07-02T03:49:38+08:00"
updated: "2024-07-02T03:49:38+08:00"
upvotes: 2
comments: 0
---

# 3190. 使所有元素都可以被3整除的最少操作数

> **[yiduobo的每日leetcode 3190.使所有元素都可以被3整除的最少操作数](https://zhuanlan.zhihu.com/p/706509895) · 知乎 · 2024-07-02 · 赞同 2**
> 力扣：[3190. 使所有元素都可以被 3 整除的最少操作数](https://leetcode.cn/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/) · Easy · 灵茶山艾府：[不是 3 的倍数的元素个数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3190.使所有元素都可以被3整除的最少操作数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-minimum-operations-to-make-all-elements-divisible-by-three/description/)

题目给出一个整数数组nums，每次操作可以将其中某个元素加上1或者减去1，问最少使用多少次操作可以使得数组中的所有元素都可以被3整除。

对于任意整数，其可能是3的倍数，也可能模3余1或者模3余2。对于模3余1这种情况，将这个数减去1就行了，而对于模3余2这种情况，则只需要将这个数加上1。换言之，若当前的整数是3的倍数，就不需要操作，否则需要进行一次操作，于是只需遍历nums，判断其中每个数是否为3的倍数，如果不是就将答案加上1。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for v in nums:
            if v % 3 != 0:
                res += 1
        
        return res
```
