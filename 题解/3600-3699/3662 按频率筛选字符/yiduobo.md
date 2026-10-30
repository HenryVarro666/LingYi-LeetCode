---
title: "3662. 按频率筛选字符"
aliases: ["yiduobo的每日leetcode 3662.按频率筛选字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950294131701154780"
zhihu_id: "1950294131701154780"
zhihu_title: "yiduobo的每日leetcode 3662.按频率筛选字符"
question_id: "3662"
question: "按频率筛选字符"
problem_url: "https://leetcode.cn/problems/filter-characters-by-frequency/"
created: "2025-09-16T00:55:11+08:00"
updated: "2025-09-16T00:55:13+08:00"
upvotes: 0
comments: 0
---

# 3662. 按频率筛选字符

> **[yiduobo的每日leetcode 3662.按频率筛选字符](https://zhuanlan.zhihu.com/p/1950294131701154780) · 知乎 · 2025-09-16 · 赞同 0**
> 力扣：[3662. 按频率筛选字符](https://leetcode.cn/problems/filter-characters-by-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3662.按频率筛选字符

[3662. 按频率筛选字符 - 力扣（LeetCode）](https://leetcode.cn/problems/filter-characters-by-frequency/description/)

题目给出一个包含小写英文字母的字符串s以及一个整数k，现在要求构造一个新的字符串，其中只包含在s中出现次数少于k次的字符。新字符串中字符的顺序必须与s中的顺序相同。若没有合法的字符，则返回空字符串。

一趟遍历，使用哈希表记录每种字符出现的次数。接下来再一趟遍历，通过哈希表检测当前字符出现的次数是否小于k，若小于，则将当前字符加入到答案数组中即可。

最后附上python代码：

```python
class Solution(object):
    def filterCharacters(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """
        
        cnt = {}
        for c in s:
            cnt[c] = cnt.get(c, 0) + 1
        
        res = []
        for c in s:
            if cnt[c] < k:
                res.append(c)
        return ''.join(res)
```
