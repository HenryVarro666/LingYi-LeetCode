---
title: "2730. 找到最长的半重复子字符串"
aliases: ["yiduobo的每日leetcode 2730.找到最长的半重复子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652410992"
zhihu_id: "652410992"
zhihu_title: "yiduobo的每日leetcode 2730.找到最长的半重复子字符串"
question_id: "2730"
question: "找到最长的半重复子字符串"
problem_url: "https://leetcode.cn/problems/find-the-longest-semi-repetitive-substring/"
difficulty: "Medium"
created: "2023-08-26T01:01:41+08:00"
updated: "2023-08-26T01:01:41+08:00"
upvotes: 0
comments: 0
---

# 2730. 找到最长的半重复子字符串

> **[yiduobo的每日leetcode 2730.找到最长的半重复子字符串](https://zhuanlan.zhihu.com/p/652410992) · 知乎 · 2023-08-26 · 赞同 0**
> 力扣：[2730. 找到最长的半重复子字符串](https://leetcode.cn/problems/find-the-longest-semi-repetitive-substring/) · Medium · 灵茶山艾府：[滑动窗口，简洁写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2730.找到最长的半重复子字符串

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-the-longest-semi-repetitive-substring/description/)

题目要求找出字符串中不包含两组或更多相邻重复字符的最长子串，那么一个自然的想法就是先将字符串中所有相邻重复字符的位置找出来。接下来对于第index组相邻重复字符，如果子串需要包含这一组字符，那么其左边界最远就只能选择第index - 1组相邻重复字符的后一个字符，而右边界最远则是第index + 1组相邻重复字符的前一个字符。根据这个结论，就可以逐个遍历这些相邻重复字符组并求解最终答案了。

在具体实现上，由于只需要考虑连续的三组相邻重复字符，因此可以使用两个变量来迭代当前最靠后的两组相邻重复字符组。特别的，若当前的相邻重复字符组不到两组，那么当前的整个前缀就都是合法的半重复子字符串，应该用这个前缀的长度来更新答案。

最后附上python代码：

```python
class Solution(object):
    def longestSemiRepetitiveSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        b = a = None
        for index in range(len(s)):
            if index > 0 and s[index] == s[index - 1]:
                b, a = a, index

            if b is None:
                res = index + 1
            else:
                res = max(res, index - b + 1)
        
        return res
```
