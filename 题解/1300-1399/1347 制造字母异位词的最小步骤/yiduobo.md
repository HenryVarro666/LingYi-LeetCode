---
title: "1347. 制造字母异位词的最小步骤"
aliases: ["yiduobo的每日leetcode 1347.制造字母异位词的最小步骤"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/397322607"
zhihu_id: "397322607"
zhihu_title: "yiduobo的每日leetcode 1347.制造字母异位词的最小步骤"
question_id: "1347"
question: "制造字母异位词的最小步骤"
problem_url: "https://leetcode.cn/problems/minimum-number-of-steps-to-make-two-strings-anagram/"
created: "2021-08-07T14:54:49+08:00"
updated: "2021-08-07T14:54:49+08:00"
upvotes: 0
comments: 0
---

# 1347. 制造字母异位词的最小步骤

> **[yiduobo的每日leetcode 1347.制造字母异位词的最小步骤](https://zhuanlan.zhihu.com/p/397322607) · 知乎 · 2021-08-07 · 赞同 0**
> 力扣：[1347. 制造字母异位词的最小步骤](https://leetcode.cn/problems/minimum-number-of-steps-to-make-two-strings-anagram/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1347.制造字母异位词的最小步骤

[力扣](https://leetcode-cn.com/problems/minimum-number-of-steps-to-make-two-strings-anagram/)

所谓字母异位词，实际上就是要让两个字符串中包含的字符以及出现次数一致，那么我们可以分别统计两个字符串中每个字符出现的次数，然后对于每个字符，计算其同时出现在两个字符串中的次数，这些字符是不需要修改的，而最终答案就是字符串长度减去这些字符的数目。

最后附上python代码：

```python
class Solution(object):
    def minSteps(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: int
        """

        s_cnt = {}
        t_cnt = {}
        for char in s:
            s_cnt[char] = s_cnt.get(char, 0) + 1
        for char in t:
            t_cnt[char] = t_cnt.get(char, 0) + 1
        
        res = len(s)
        for char, cnt in s_cnt.items():
            res -= min(cnt, t_cnt.get(char, 0))
        
        return res
```
