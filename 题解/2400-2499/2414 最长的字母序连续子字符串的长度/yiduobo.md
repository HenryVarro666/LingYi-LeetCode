---
title: "2414. 最长的字母序连续子字符串的长度"
aliases: ["yiduobo的每日leetcode 2414.最长的字母序连续子字符串的长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/569197647"
zhihu_id: "569197647"
zhihu_title: "yiduobo的每日leetcode 2414.最长的字母序连续子字符串的长度"
question_id: "2414"
question: "最长的字母序连续子字符串的长度"
problem_url: "https://leetcode.cn/problems/length-of-the-longest-alphabetical-continuous-substring/"
difficulty: "Medium"
rating: 1222
created: "2022-09-29T02:30:13+08:00"
updated: "2022-09-29T02:30:13+08:00"
upvotes: 0
comments: 0
---

# 2414. 最长的字母序连续子字符串的长度

> **[yiduobo的每日leetcode 2414.最长的字母序连续子字符串的长度](https://zhuanlan.zhihu.com/p/569197647) · 知乎 · 2022-09-29 · 赞同 0**
> 力扣：[2414. 最长的字母序连续子字符串的长度](https://leetcode.cn/problems/length-of-the-longest-alphabetical-continuous-substring/) · Medium · 灵茶山艾府：[维护连续递增长度（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2414.最长的字母序连续子字符串的长度

[力扣](https://leetcode.cn/problems/length-of-the-longest-alphabetical-continuous-substring/)

令f[i]表示以s[i]结尾的最长字母序连续子字符串的长度，那么对于f[i]：

1、i \= 0时，有f[0] \= 1

2、s[i]不是s[i - 1]在字母序中的下一个字符时，同样是f[i] \= 1

3、s[i]是在字母序中的下一个字符时，有f[i] \= f[i - 1] + 1

注意到这里的f每一轮只与上一轮有关，因此可以使用一个遍历迭代来节省空间，于是现在的做法就是一趟遍历，使用一个变量now记录以当前字符结尾的最长的字母序连续子字符串的长度。对于当前的字符s[i]，当i \= 0或者s[i]不是s[i - 1]在字母序中的下一个字符时，now应该重置为1，否则now \= now + 1。遍历过程中now的最大值即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def longestContinuousSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        now = 0
        for index, char in enumerate(s):
            if index == 0 or ord(char) != ord(s[index - 1]) + 1:
                res = max(res, now)
                now = 0
            now += 1
        
        return max(res, now)
```
