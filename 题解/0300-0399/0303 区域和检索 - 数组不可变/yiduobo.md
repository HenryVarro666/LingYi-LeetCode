---
title: "303. 区域和检索"
aliases: ["yiduobo的每日leetcode 303.区域和检索"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/design", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/157892436"
zhihu_id: "157892436"
zhihu_title: "yiduobo的每日leetcode 303.区域和检索"
question_id: "303"
question: "区域和检索 - 数组不可变"
problem_url: "https://leetcode.cn/problems/range-sum-query-immutable/"
difficulty: "Easy"
created: "2020-07-08T21:21:24+08:00"
updated: "2020-07-08T21:21:24+08:00"
upvotes: 0
comments: 0
---

# 303. 区域和检索

> **[yiduobo的每日leetcode 303.区域和检索](https://zhuanlan.zhihu.com/p/157892436) · 知乎 · 2020-07-08 · 赞同 0**
> 力扣：[303. 区域和检索 - 数组不可变](https://leetcode.cn/problems/range-sum-query-immutable/) · Easy · 灵茶山艾府：[前缀和，附扩展问题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

303.区域和检索<https://leetcode-cn.com/problems/range-sum-query-immutable/>

很经典的题目，做法是维护前缀和，即

sum_list[index] \= nums[0] + nums[1] + ... + nums[index]

那么对于求解sumRange(x, y)，我们就可以使用sum_list[y] - sum_list[x-1]来得出答案了，理由是

sum_list[x - 1] \= nums[0] + nums[1] + ... + nums[x - 1]

sum_list[y] \= nums[0] + nums[1] + ... + nums[x - 1] + nums[x] + ... + nums[y]

两式相减，0到x - 1的部分抵消掉之后剩下的就是x到y的和了

需要特别注意x \= 0的情况，此时直接返回sum_list[y]即可

最后附上python代码：

```python
class NumArray(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.sum_list = nums[:]
        for index in range(1, len(nums)):
            self.sum_list[index] += self.sum_list[index - 1]

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        if i == 0:
            return self.sum_list[j]
        else:
            return self.sum_list[j] - self.sum_list[i - 1]

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(i,j)
```
