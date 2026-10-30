---
title: "2454. 下一个更大元素IV"
aliases: ["yiduobo的每日leetcode 2454.下一个更大元素IV"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/585844487"
zhihu_id: "585844487"
zhihu_title: "yiduobo的每日leetcode 2454.下一个更大元素IV"
question_id: "2454"
question: "下一个更大元素 IV"
problem_url: "https://leetcode.cn/problems/next-greater-element-iv/"
difficulty: "Hard"
rating: 2175
created: "2022-11-22T23:25:02+08:00"
updated: "2022-11-22T23:25:02+08:00"
upvotes: 0
comments: 0
---

# 2454. 下一个更大元素IV

> **[yiduobo的每日leetcode 2454.下一个更大元素IV](https://zhuanlan.zhihu.com/p/585844487) · 知乎 · 2022-11-22 · 赞同 0**
> 力扣：[2454. 下一个更大元素 IV](https://leetcode.cn/problems/next-greater-element-iv/) · Hard · 灵茶山艾府：[O(n) 一次遍历+双单调栈（附题单）Python/Java/C++/Go/JS/Rust](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2454.下一个更大元素IV

[力扣](https://leetcode.cn/problems/next-greater-element-iv/)

经典单调栈问题的强化版。本题需要找到某个数后面第二个比这个数大的元素的位置，对于下一个更大数的位置，可以参考之前的

[yiduobo：yiduobo的每日leetcode 496.下一个更大元素I](https://zhuanlan.zhihu.com/p/257283167)

那么在这里有一个思路就是，对于这些利用496题中的方法找到了下一个更大元素的数而言，只需再执行一次相同的算法就可以找到本题所需的答案了。由于之前的做法需要将这些数保留在栈中，那么在这里可以另起一个栈来储存这些已经找到了下一个更大元素的数。需要注意的是，这个新栈中数的顺序应该与老栈中保持一致，其他的细节则可以直接照搬之前的做法。

最后附上python代码：

```python
class Solution(object):
    def secondGreaterElement(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        stack_for_first = []
        stack_for_second = []

        res = [-1] * len(nums)
        for index, num in enumerate(nums):
            while stack_for_second and nums[stack_for_second[-1]] < num:
                res[stack_for_second[-1]] = num
                stack_for_second.pop()
            
            p = len(stack_for_first) - 1
            while p >= 0 and nums[stack_for_first[p]] < num:
                p -= 1
            
            for pos in stack_for_first[p + 1 : len(stack_for_first)]:
                stack_for_second.append(pos)

            while len(stack_for_first) > p + 1:
                stack_for_first.pop()
            
            stack_for_first.append(index)
        
        return res
```
