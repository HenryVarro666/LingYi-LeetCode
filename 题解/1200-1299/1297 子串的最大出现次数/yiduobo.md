---
title: "1297. 子串的最大出现次数"
aliases: ["yiduobo的每日leetcode 1297.子串的最大出现次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/贪心算法", "题单/字符串", "题单/滑动窗口与双指针/一-定长滑动窗口", "题单/贪心算法/五-思维题", "题单/字符串/四-字符串哈希"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390446169"
zhihu_id: "390446169"
zhihu_title: "yiduobo的每日leetcode 1297.子串的最大出现次数"
question_id: "1297"
question: "子串的最大出现次数"
problem_url: "https://leetcode.cn/problems/maximum-number-of-occurrences-of-a-substring/"
difficulty: "Medium"
rating: 1748
created: "2021-07-16T22:35:32+08:00"
updated: "2021-07-16T22:35:32+08:00"
upvotes: 1
comments: 0
---

# 1297. 子串的最大出现次数

> **[yiduobo的每日leetcode 1297.子串的最大出现次数](https://zhuanlan.zhihu.com/p/390446169) · 知乎 · 2021-07-16 · 赞同 1**
> 力扣：[1297. 子串的最大出现次数](https://leetcode.cn/problems/maximum-number-of-occurrences-of-a-substring/) · Medium · 灵茶山艾府：[脑筋急转弯+定长滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1296题由于与之前的846题重复，因此在这里就先跳过了。

1297.子串的最大出现次数

[力扣](https://leetcode-cn.com/problems/maximum-number-of-occurrences-of-a-substring/)

题目要求找出字符串中出现次数最多的，且其中不同字符数目小于等于maxLetters，长度处于minSize到maxSize之间的字符串的出现次数。

首先可以明确的是，若某个子串在s中出现了k次，那么其任意子串在s中也至少会出现k次。那么若最终答案为k，设其对应的字符串为s'，那么s'的其任意子串也会出现k次，其中所有长度为minSize的字符串也将出现k次，也就是说我们只需要检测所有长度为minSize的字符串，从中找出符合条件的字符串的出现次数即可。

于是现在可以从头开始向后扫描，检测所有长度为minSize的子串，并利用滑动窗口的思想统计其中不同字符出现的次数。若次数小于等于maxLetters，那么就将当前子串加入到dict中。扫描完成后，dict中的最大次数就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxFreq(self, s, maxLetters, minSize, maxSize):
        """
        :type s: str
        :type maxLetters: int
        :type minSize: int
        :type maxSize: int
        :rtype: int
        """

        s_dict = {}
        now = s[:minSize]
        cnt_dict = {}
        for char in now:
            cnt_dict[char] = cnt_dict.get(char, 0) + 1
        
        if len(cnt_dict) <= maxLetters:
            s_dict[now] = 1
        
        for index in range(minSize, len(s)):
            cnt_dict[now[0]] -= 1
            cnt_dict[s[index]] = cnt_dict.get(s[index], 0) + 1
            if cnt_dict[now[0]] == 0:
                cnt_dict.pop(now[0])
            now = now[1:] + s[index]
            if len(cnt_dict) <= maxLetters:
                s_dict[now] = s_dict.get(now, 0) + 1
        
        if len(s_dict) == 0:
            return 0
        return max(s_dict.values())
```
