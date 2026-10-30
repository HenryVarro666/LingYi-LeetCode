---
title: "459. 重复的子字符串"
aliases: ["yiduobo的每日leetcode 459.重复的子字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/220493117"
zhihu_id: "220493117"
zhihu_title: "yiduobo的每日leetcode 459.重复的子字符串"
question_id: "459"
question: "重复的子字符串"
problem_url: "https://leetcode.cn/problems/repeated-substring-pattern/"
created: "2020-09-06T22:24:06+08:00"
updated: "2020-09-06T22:24:06+08:00"
upvotes: 1
comments: 0
---

# 459. 重复的子字符串

> **[yiduobo的每日leetcode 459.重复的子字符串](https://zhuanlan.zhihu.com/p/220493117) · 知乎 · 2020-09-06 · 赞同 1**
> 力扣：[459. 重复的子字符串](https://leetcode.cn/problems/repeated-substring-pattern/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

459.重复的子字符串<https://leetcode-cn.com/problems/repeated-substring-pattern/>

我在这里采用了一种比较取巧的做法，直接将原始字符串s复制一遍，接在后面形成新串s'，然后在s'中找s。若存在一个s的起点不等于0，且不等于len(s)，即这个起点在s中间，那么这个字符串就可以由子串重复得到。

证明也比较简洁。设这个起点为p，那么s[0:p]就是用来重复的子串。由于s与s'[p:p + len(s)]一致，那么s[0:p]就与s'[p:2p]一致，而s[p:2p]与s'[p:2p]一致，换言之，就是s[0:p]与s[p:2p]一致。接下来逐个往后递推即可证明s可以由s[0:p]构成。

最后附上python代码：

```python
class Solution(object):
    def repeatedSubstringPattern(self, s):
        """
        :type s: str
        :rtype: bool
        """

        return (s + s).find(s, 1) != len(s)
```
