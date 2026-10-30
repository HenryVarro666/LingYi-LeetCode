---
title: "1593. 拆分字符串使唯一子字符串的数目最大"
aliases: ["yiduobo的每日leetcode 1593.拆分字符串使唯一子字符串的数目最大"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432284003"
zhihu_id: "432284003"
zhihu_title: "yiduobo的每日leetcode 1593.拆分字符串使唯一子字符串的数目最大"
question_id: "1593"
question: "拆分字符串使唯一子字符串的数目最大"
problem_url: "https://leetcode.cn/problems/split-a-string-into-the-max-number-of-unique-substrings/"
created: "2021-11-11T23:33:17+08:00"
updated: "2021-11-11T23:33:17+08:00"
upvotes: 0
comments: 0
---

# 1593. 拆分字符串使唯一子字符串的数目最大

> **[yiduobo的每日leetcode 1593.拆分字符串使唯一子字符串的数目最大](https://zhuanlan.zhihu.com/p/432284003) · 知乎 · 2021-11-11 · 赞同 0**
> 力扣：[1593. 拆分字符串使唯一子字符串的数目最大](https://leetcode.cn/problems/split-a-string-into-the-max-number-of-unique-substrings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1593.拆分字符串使唯一子字符串的数目最大

[力扣](https://leetcode-cn.com/problems/split-a-string-into-the-max-number-of-unique-substrings/)

题目要求将一个字符拆分成若干个子字符串，这些子字符串不能重复，同时要求子字符串的数目最多。没有想出什么很优美的做法，不过好在这里n的规模很小，那么可以直接暴力搜索回溯求解。

对于当前字符串而言，若其没有被使用过，那么不划分也是一种选择，此时可以用已划分出来的字符串个数，再加上1来更新答案。除此之外，还可以枚举当前字符串中的所有前缀，若该前缀没有被使用过，那么就尝试进行划分，然后递归求解剩下的后缀。

当然，硬要用动态规划来做也是可以的，但是状态表示同样是2^n级别的。相比之下，如果在包里搜索回溯里面加上一些简单的最优性剪枝，反而性能会更好。

最后附上python代码：

```python
class Solution(object):
    def maxUniqueSplit(self, s):
        """
        :type s: str
        :rtype: int
        """

        self.res = 0
        n = len(s)
        used = set()
        self.dfs(s, 0, 0, n, used)
        
        return self.res

    def dfs(self, s, pos, now, n, used):
        if s[pos:] not in used and now + 1 > self.res:
            self.res = now + 1
        if pos == n - 1:
            return

        if n - pos + now <= self.res:
            return
        
        for cut_pos in range(pos, n - 1):
            if s[pos : cut_pos + 1] not in used:
                used.add(s[pos : cut_pos + 1])
                self.dfs(s, cut_pos + 1, now + 1, n, used)
                used.remove(s[pos : cut_pos + 1])
```
