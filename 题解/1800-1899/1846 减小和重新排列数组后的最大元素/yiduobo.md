---
title: "1846. 减小和重新排列数组后的最大元素"
aliases: ["yiduobo的每日leetcode 1846.减小和重新排列数组后的最大元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/469916353"
zhihu_id: "469916353"
zhihu_title: "yiduobo的每日leetcode 1846.减小和重新排列数组后的最大元素"
question_id: "1846"
question: "减小和重新排列数组后的最大元素"
problem_url: "https://leetcode.cn/problems/maximum-element-after-decreasing-and-rearranging/"
difficulty: "Medium"
rating: 1454
created: "2022-02-20T19:35:15+08:00"
updated: "2022-02-20T19:35:15+08:00"
upvotes: 0
comments: 0
---

# 1846. 减小和重新排列数组后的最大元素

> **[yiduobo的每日leetcode 1846.减小和重新排列数组后的最大元素](https://zhuanlan.zhihu.com/p/469916353) · 知乎 · 2022-02-20 · 赞同 0**
> 力扣：[1846. 减小和重新排列数组后的最大元素](https://leetcode.cn/problems/maximum-element-after-decreasing-and-rearranging/) · Medium · 灵茶山艾府：[贪心好想，如何证明？（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1846.减小和重新排列数组后的最大元素

[力扣](https://leetcode-cn.com/problems/maximum-element-after-decreasing-and-rearranging/)

题目中只提供减1和重排这两种操作，因此为了使得答案最大，在不得已执行减一操作的时候就应该先对较小的数执行减一操作，这样才可能保住较大的数。于是在这里可以先对数组arr从小到大进行排序。

由于题目规定了答案的第一个数为1，那么此时的arr[0]就需要通过减1操作变为1。接下来考虑arr[1]以及之后的数。即当前已经处理完的最后一个数的大小为last，那么对于当前遍历到的数num，若num > last + 1，此时就必须将num缩减成last + 1，否则num就可以保持不变。处理完成后，更新last然后继续向后处理即可。最后一次更新后的last即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def maximumElementAfterDecrementingAndRearranging(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        sorted_arr = sorted(arr)
        last = 1
        for num in sorted_arr[1:]:
            if num - last > 1:
                last += 1
            else:
                last = num
        
        return last
```
