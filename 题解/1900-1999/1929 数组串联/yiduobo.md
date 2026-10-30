---
title: "1929. 数组串联"
aliases: ["yiduobo的每日leetcode 1929.数组串联"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/487018092"
zhihu_id: "487018092"
zhihu_title: "yiduobo的每日leetcode 1929.数组串联"
question_id: "1929"
question: "数组串联"
problem_url: "https://leetcode.cn/problems/concatenation-of-array/"
difficulty: "Easy"
created: "2022-03-24T21:38:28+08:00"
updated: "2022-03-24T21:38:29+08:00"
upvotes: 0
comments: 0
---

# 1929. 数组串联

> **[yiduobo的每日leetcode 1929.数组串联](https://zhuanlan.zhihu.com/p/487018092) · 知乎 · 2022-03-24 · 赞同 0**
> 力扣：[1929. 数组串联](https://leetcode.cn/problems/concatenation-of-array/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1929.数组串联

[力扣](https://leetcode-cn.com/problems/concatenation-of-array/)

比较基础的题目，直接把原数组原样复制两份放进答案里面即可。

最后附上python代码：

```python
class Solution(object):
    def getConcatenation(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        res = nums[:]
        for num in nums:
            res.append(num)
        
        return res
```
