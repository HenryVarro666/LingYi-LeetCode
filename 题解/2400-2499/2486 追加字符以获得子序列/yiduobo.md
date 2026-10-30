---
title: "2486. 追加字符以获得子序列"
aliases: ["yiduobo的每日leetcode 2486.追加字符以获得子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/四-双序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589809128"
zhihu_id: "589809128"
zhihu_title: "yiduobo的每日leetcode 2486.追加字符以获得子序列"
question_id: "2486"
question: "追加字符以获得子序列"
problem_url: "https://leetcode.cn/problems/append-characters-to-string-to-make-subsequence/"
difficulty: "Medium"
rating: 1363
created: "2022-12-07T02:04:16+08:00"
updated: "2022-12-07T02:04:16+08:00"
upvotes: 0
comments: 0
---

# 2486. 追加字符以获得子序列

> **[yiduobo的每日leetcode 2486.追加字符以获得子序列](https://zhuanlan.zhihu.com/p/589809128) · 知乎 · 2022-12-07 · 赞同 0**
> 力扣：[2486. 追加字符以获得子序列](https://leetcode.cn/problems/append-characters-to-string-to-make-subsequence/) · Medium · 灵茶山艾府：[两种双指针写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2486.追加字符以获得子序列

[力扣](https://leetcode.cn/problems/append-characters-to-string-to-make-subsequence/description/)

由于只能在s的末尾添加字符，那么实际上要求的就是s的子序列能匹配t的前缀最大值，这是一个经典的贪心问题。对s进行一趟遍历，并使用一个变量p记录下一个需要匹配的字符为t[p]，那么若当前的s[index] \= t[p]，那么就将p向后移动一位。遍历完成后，t就是当前能匹配的最大值，此时只需补上t中剩余的字符，也就是用t的长度减去p即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def appendCharacters(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """
        
        p = 0
        n = len(t)
        for char in s:
            if p < n and t[p] == char:
                p += 1
        
        return n - p
```
