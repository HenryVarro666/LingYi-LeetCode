---
title: "3379. 转换数组"
aliases: ["yiduobo的每日leetcode 3379.转换数组"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/29044893802"
zhihu_id: "29044893802"
zhihu_title: "yiduobo的每日leetcode 3379.转换数组"
question_id: "3379"
question: "转换数组"
problem_url: "https://leetcode.cn/problems/transformed-array/"
difficulty: "Easy"
created: "2025-03-09T23:37:05+08:00"
updated: "2025-03-09T23:37:05+08:00"
upvotes: 1
comments: 0
---

# 3379. 转换数组

> **[yiduobo的每日leetcode 3379.转换数组](https://zhuanlan.zhihu.com/p/29044893802) · 知乎 · 2025-03-09 · 赞同 1**
> 力扣：[3379. 转换数组](https://leetcode.cn/problems/transformed-array/) · Easy · 灵茶山艾府：[简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3379.转换数组

[3379. 转换数组 - 力扣（LeetCode）](https://leetcode.cn/problems/transformed-array/description/)

题目给出一个整数数组nums，这是一个循环数组。接下来需要根据一下规则创建一个大小相同的新数组。

对于从0到len(nums) - 1之间的每个下标i：

1、若nums[i] > 0，那么将循环数组中，从下标i开始向右移动nums[i]步之后对应下标的元素值赋给result[i]

2、若nums[i] \< 0，那么将循环数组中，从下标i开始向左移动abs(nums[i])步之后对应下标的元素值赋给result[i]

3、若nums[i] \= 0，那么将nums[i]的值赋result[i]

问最后得到的result是什么

对于题目中的三类操作：

1、当nums[i] > 0时，新的下标是i + nums[i]

2、当nums[i] \< 0时，新的下标是i - abs(nums[i])，去掉abs之后实际上就是i + nums[i]

3、当nums[i] \= 0时，新的下标是i，同样可以认为是i + nums[i]

综合起来可以发现，实际上就可以认为每一轮都是把nums中下标i + nums[i]的元素赋值给result[i]，直接一趟遍历进行赋值操作即可。另外需要注意除以越界时循环的情况，不过在python的实现中，直接对数组长度取模就行了，无需特别处理负数的取模。

最后附上python代码：

```python
class Solution(object):
    def constructTransformedArray(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        res = []
        for index in range(len(nums)):
            res.append(nums[(index + nums[index]) % len(nums)])
        
        return res
```
