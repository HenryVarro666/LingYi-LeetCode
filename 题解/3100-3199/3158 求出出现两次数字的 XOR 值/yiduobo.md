---
title: "3158. 求出出现两次数字的XOR值"
aliases: ["yiduobo的每日leetcode 3158.求出出现两次数字的XOR值"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/704363953"
zhihu_id: "704363953"
zhihu_title: "yiduobo的每日leetcode 3158.求出出现两次数字的XOR值"
question_id: "3158"
question: "求出出现两次数字的 XOR 值"
problem_url: "https://leetcode.cn/problems/find-the-xor-of-numbers-which-appear-twice/"
difficulty: "Easy"
created: "2024-06-20T00:01:34+08:00"
updated: "2024-06-20T00:01:34+08:00"
upvotes: 0
comments: 0
---

# 3158. 求出出现两次数字的XOR值

> **[yiduobo的每日leetcode 3158.求出出现两次数字的XOR值](https://zhuanlan.zhihu.com/p/704363953) · 知乎 · 2024-06-20 · 赞同 0**
> 力扣：[3158. 求出出现两次数字的 XOR 值](https://leetcode.cn/problems/find-the-xor-of-numbers-which-appear-twice/) · Easy · 灵茶山艾府：[一次遍历+O(1) 空间（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3158.求出出现两次数字的XOR值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-xor-of-numbers-which-appear-twice/description/)

题目给出一个数组nums，其中的数字要么出现一次要么出现两次。问其中所有出现两次的数字的异或值是多少。

使用哈希表统计每种数字出现的次数，接下来遍历哈希表中的元素，若当前元素出现了两次，就将其异或到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def duplicateNumbersXOR(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        freq = Counter(nums)
        res = 0
        for v, f in freq.items():
            if f == 2:
                res ^= v
        
        return res
```
