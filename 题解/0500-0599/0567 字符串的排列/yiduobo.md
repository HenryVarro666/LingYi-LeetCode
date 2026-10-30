---
title: "567. 字符串的排列"
aliases: ["yiduobo的每日leetcode 567.字符串的排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266490026"
zhihu_id: "266490026"
zhihu_title: "yiduobo的每日leetcode 567.字符串的排列"
question_id: "567"
question: "字符串的排列"
problem_url: "https://leetcode.cn/problems/permutation-in-string/"
difficulty: "Medium"
created: "2020-10-17T22:06:26+08:00"
updated: "2020-10-17T22:06:26+08:00"
upvotes: 0
comments: 0
---

# 567. 字符串的排列

> **[yiduobo的每日leetcode 567.字符串的排列](https://zhuanlan.zhihu.com/p/266490026) · 知乎 · 2020-10-17 · 赞同 0**
> 力扣：[567. 字符串的排列](https://leetcode.cn/problems/permutation-in-string/) · Medium · 灵茶山艾府：[定长滑动窗口，从 O(26n) 到 O(n)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

567.字符串的排列<https://leetcode-cn.com/problems/permutation-in-string/>

题目需要判断s2中是否存在一个子串，其为s1中字符的排列。若存在这样一个子串，那么这个子串的长度就必然要与s1的长度相等，因此就可以使用滑动窗口，从左往右检索s2中所有长度为len(s1)的子串是否是s1中字符的排列。

对于字符的排列这种说法，实际上只需要两个串中每个字符出现的次数完全一致即可，因此可以使用一个dict保存s1中每个字符出现的次数，同时在窗口滑动的过程中维护另一个dict，保存当前窗口对应子串中每个字符出现的次数。当这两个dict一致时，说明存在对应的子串。

当窗口滑动时，将右侧的字符加入到dict中，同时将左侧的字符从dict中移除即可。

最后附上python代码：

```python
class Solution(object):
    def checkInclusion(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        if len(s1) > len(s2):
            return False

        count_dict = {}
        for char in s1:
            count_dict[char] = count_dict.get(char, 0) + 1
        
        now_dict = {}
        for index in range(len(s1)):
            now_dict[s2[index]] = now_dict.get(s2[index], 0) + 1
        if count_dict == now_dict:
            return True

        for index in range(len(s1), len(s2)):
            remove = s2[index - len(s1)]
            now_dict[remove] -= 1
            now_dict[s2[index]] = now_dict.get(s2[index], 0) + 1
            if now_dict[remove] == 0:
                now_dict.pop(remove)

            if now_dict == count_dict:
                return True

        return False
```
