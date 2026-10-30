---
title: "1180. 统计只包含单一字母的子串"
aliases: ["yiduobo的每日leetcode 1180.统计只包含单一字母的子串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/611873172"
zhihu_id: "611873172"
zhihu_title: "yiduobo的每日leetcode 1180.统计只包含单一字母的子串"
question_id: "1180"
question: "统计只包含单一字母的子串"
problem_url: "https://leetcode.cn/problems/count-substrings-with-only-one-distinct-letter/"
created: "2023-03-06T23:39:13+08:00"
updated: "2023-03-06T23:39:13+08:00"
upvotes: 0
comments: 0
---

# 1180. 统计只包含单一字母的子串

> **[yiduobo的每日leetcode 1180.统计只包含单一字母的子串](https://zhuanlan.zhihu.com/p/611873172) · 知乎 · 2023-03-06 · 赞同 0**
> 力扣：[1180. 统计只包含单一字母的子串](https://leetcode.cn/problems/count-substrings-with-only-one-distinct-letter/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1180.统计只包含单一字母的子串

<https://leetcode.cn/problems/count-substrings-with-only-one-distinct-letter/>

题目要求子串中只能出现一种字符，那么对于一个长度为k的由同一个字符构成的区间而言，其可以形成k个长度为1的合法子串，k - 1个长度为2的合法子串，...，1个长度为k的合法子串，也就是说一共可以形成(1 + k) \* k / 2个合法子串。于是只需一趟遍历，找出所有由同一个字符构成的区间长度，并计算合法子串的数目。

最后附上python代码：

```python
class Solution(object):
    def countLetters(self, s):
        """
        :type s: str
        :rtype: int
        """

        last = None
        cnt = 0
        res = 0
        for char in s:
            if char == last:
                cnt += 1
            else:
                res += cnt * (cnt + 1) / 2
                last = char
                cnt = 1
        
        return res + cnt * (cnt + 1) / 2
```
