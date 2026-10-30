---
title: "3798. 最大的偶数"
aliases: ["yiduobo的每日leetcode 3798.最大的偶数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1992274961100993172"
zhihu_id: "1992274961100993172"
zhihu_title: "yiduobo的每日leetcode 3798.最大的偶数"
question_id: "3798"
question: "最大的偶数"
problem_url: "https://leetcode.cn/problems/largest-even-number/"
difficulty: "Easy"
created: "2026-01-08T01:22:24+08:00"
updated: "2026-01-08T01:22:26+08:00"
upvotes: 0
comments: 0
---

# 3798. 最大的偶数

> **[yiduobo的每日leetcode 3798.最大的偶数](https://zhuanlan.zhihu.com/p/1992274961100993172) · 知乎 · 2026-01-08 · 赞同 0**
> 力扣：[3798. 最大的偶数](https://leetcode.cn/problems/largest-even-number/) · Easy · 灵茶山艾府：[移除所有的尾 1（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3798.最大的偶数

<https://leetcode.cn/problems/largest-even-number/description/>

题目给出一个仅有字符'1'和'2'组成的字符串s。

现在可以删除其中的一些字符，剩余字符的顺序不变。

问可能得到的最大偶数是什么。若不存在这样的字符串，则返回空字符串。

为了使得最终结果为偶数，必须保证最后一个字符为'2'。另一方面，为了使得结果最大，因此应该尽量少删字符。综合以上两点，则应该删除掉s末尾连续的'1'，使得s以'2'结尾。于是可以从后往前找到s中最后一个'2'的下标p，最终答案就是s[:p + 1]。若不存在合法的p，那么答案就是空字符串。

最后附上python代码：

```python
class Solution(object):
    def largestEven(self, s):
        """
        :type s: str
        :rtype: str
        """
        
        p = len(s) - 1
        while p >= 0 and s[p] == '1':
            p -= 1
        return s[:p + 1]
```
