---
title: "3309. 连接二进制表示可形成的最大数值"
aliases: ["yiduobo的每日leetcode 3309.连接二进制表示可形成的最大数值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1270566179"
zhihu_id: "1270566179"
zhihu_title: "yiduobo的每日leetcode 3309.连接二进制表示可形成的最大数值"
question_id: "3309"
question: "连接二进制表示可形成的最大数值"
problem_url: "https://leetcode.cn/problems/maximum-possible-number-by-binary-concatenation/"
difficulty: "Medium"
created: "2024-10-16T01:07:47+08:00"
updated: "2024-10-16T01:07:47+08:00"
upvotes: 0
comments: 0
---

# 3309. 连接二进制表示可形成的最大数值

> **[yiduobo的每日leetcode 3309.连接二进制表示可形成的最大数值](https://zhuanlan.zhihu.com/p/1270566179) · 知乎 · 2024-10-16 · 赞同 0**
> 力扣：[3309. 连接二进制表示可形成的最大数值](https://leetcode.cn/problems/maximum-possible-number-by-binary-concatenation/) · Medium · 灵茶山艾府：[非暴力做法：O(nlogn) 排序（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3309.连接二进制表示可形成的最大数值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-possible-number-by-binary-concatenation/)

题目给出一个长度为3的整数数组nums，要求将其中的元素转换成二进制然后按某种顺序连接，问可以得到的最大数值是多少。

由于题目中数组的大小只有3，那么完全可以暴力枚举出所有的排列方式，计算出形成的数值，取其中的最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxGoodNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        length = [0] * 3
        for index, v in enumerate(nums):
            x = v
            while x:
                length[index] += 1
                x >>= 1
        
        res = 0
        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                for k in range(3):
                    if i == k or j == k:
                        continue
                    v = (nums[i] << (length[j] + length[k])) + (nums[j] << length[k]) + nums[k]
                    res = max(res, v)
        
        return res
```
