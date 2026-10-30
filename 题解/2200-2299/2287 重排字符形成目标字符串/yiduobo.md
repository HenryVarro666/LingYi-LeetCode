---
title: "2287. 重排字符形成目标字符串"
aliases: ["yiduobo的每日leetcode 2287.重排字符形成目标字符串"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/552714734"
zhihu_id: "552714734"
zhihu_title: "yiduobo的每日leetcode 2287.重排字符形成目标字符串"
question_id: "2287"
question: "重排字符形成目标字符串"
problem_url: "https://leetcode.cn/problems/rearrange-characters-to-make-target-string/"
difficulty: "Easy"
created: "2022-08-11T20:26:44+08:00"
updated: "2022-08-11T20:26:44+08:00"
upvotes: 0
comments: 0
---

# 2287. 重排字符形成目标字符串

> **[yiduobo的每日leetcode 2287.重排字符形成目标字符串](https://zhuanlan.zhihu.com/p/552714734) · 知乎 · 2022-08-11 · 赞同 0**
> 力扣：[2287. 重排字符形成目标字符串](https://leetcode.cn/problems/rearrange-characters-to-make-target-string/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2287.重排字符形成目标字符串

[力扣](https://leetcode.cn/problems/rearrange-characters-to-make-target-string/)

由于可以随意选择和重新排列字符，因此只需要需要的字符数量足够，就能拼凑出目标字符串。于是可以分别统计s和target中每个字符串出现的次数，然后遍历target中的字符，计算s中相同的字符足够几个target使用，取其中的最小值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def rearrangeCharacters(self, s, target):
        """
        :type s: str
        :type target: str
        :rtype: int
        """

        char_cnt_s = {}
        for char in s:
            char_cnt_s[char] = char_cnt_s.get(char, 0) + 1
        
        char_cnt_target = {}
        for char in target:
            char_cnt_target[char] = char_cnt_target.get(char, 0) + 1
        
        res = len(s)
        for char, target_cnt in char_cnt_target.items():
            res = min(res, char_cnt_s.get(char, 0) / target_cnt)

        return res
```
