---
title: "438. 找到字符串中的所有字母异位词"
aliases: ["yiduobo的每日leetcode 438.找到字符串中的所有字母异位词"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/LeetCode-热题-100/滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/201682967"
zhihu_id: "201682967"
zhihu_title: "yiduobo的每日leetcode 438.找到字符串中的所有字母异位词"
question_id: "438"
question: "找到字符串中所有字母异位词"
problem_url: "https://leetcode.cn/problems/find-all-anagrams-in-a-string/"
difficulty: "Medium"
created: "2020-08-28T01:05:02+08:00"
updated: "2020-08-28T01:05:02+08:00"
upvotes: 0
comments: 0
---

# 438. 找到字符串中的所有字母异位词

> **[yiduobo的每日leetcode 438.找到字符串中的所有字母异位词](https://zhuanlan.zhihu.com/p/201682967) · 知乎 · 2020-08-28 · 赞同 0**
> 力扣：[438. 找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/) · Medium · 灵茶山艾府：[两种方法：定长滑窗/不定长滑窗（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

438.找到字符串中的所有字母异位词<https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/>

注意到题目要求的异位词是字母出现相同的子串，那么很自然可以想到滑动窗口的做法。

首先统计p中每个字符出现的次数p_cnt，然后按照p的长度在s中初始化窗口，同时统计窗口中每个字符出现的次数now_cnt。先对比p_cnt是否与now_cnt相同，如果是，那么0是一个可行的解。接下来将窗口往右滑动，每次移动将窗口左边界的字符从now_cnt中移除，同时将窗口右边界的字符加入到now_cnt中，再判断now_cnt是否与p_cnt相同，若相同，那么新的窗口左边界是一个可行的解。

一趟扫描，逐个判断每个可行的区间即可。

最后附上python代码：

```python
class Solution(object):
    def findAnagrams(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: List[int]
        """

        if len(s) < len(p):
            return []

        p_cnt = {}
        for char in p:
            p_cnt[char] = p_cnt.get(char, 0) + 1
        
        now_cnt = {}
        for char in s[:len(p)]:
            now_cnt[char] = now_cnt.get(char, 0) + 1

        res = []

        if now_cnt == p_cnt:
            res.append(0)

        for index in range(len(p), len(s)):
            add_char = s[index]
            del_char = s[index - len(p)]
            now_cnt[add_char] = now_cnt.get(add_char, 0) + 1
            now_cnt[del_char] -= 1
            flag = True
            for char, cnt in p_cnt.items():
                if now_cnt.get(char, 0) != cnt:
                    flag = False
                    break
            if flag:
                res.append(index - len(p) + 1)

        return res
```
