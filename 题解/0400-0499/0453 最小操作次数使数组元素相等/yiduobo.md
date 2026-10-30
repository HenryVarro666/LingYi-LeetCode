---
title: "453. 最小移动次数使数组元素相等"
aliases: ["yiduobo的每日leetcode 453.最小移动次数使数组元素相等"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/214391720"
zhihu_id: "214391720"
zhihu_title: "yiduobo的每日leetcode 453.最小移动次数使数组元素相等"
question_id: "453"
question: "最小操作次数使数组元素相等"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-equal-array-elements/"
difficulty: "Medium"
created: "2020-09-03T23:51:47+08:00"
updated: "2020-09-03T23:51:47+08:00"
upvotes: 0
comments: 0
---

# 453. 最小移动次数使数组元素相等

> **[yiduobo的每日leetcode 453.最小移动次数使数组元素相等](https://zhuanlan.zhihu.com/p/214391720) · 知乎 · 2020-09-03 · 赞同 0**
> 力扣：[453. 最小操作次数使数组元素相等](https://leetcode.cn/problems/minimum-moves-to-equal-array-elements/) · Medium · 灵茶山艾府：[等价转换（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

453.最小移动次数使数组元素相等<https://leetcode-cn.com/problems/minimum-moves-to-equal-array-elements/>

由于最后的要求是要让数组中的所有元素相等，那么每个元素的绝对大小并不重要，只需要考察相对大小。对于题目中描述的使n - 1个元素增加1，在相对大小的角度上就可以认为是让剩下的那一个元素减去1。于是题目就变成了每次可以选一个元素减去1，问多少次操作才能让所有元素相等，那么将所有元素都减小到最小值即可。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        return sum(nums) - min(nums) * len(nums)
```
