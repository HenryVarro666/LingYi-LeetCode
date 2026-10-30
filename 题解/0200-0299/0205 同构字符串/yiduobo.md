---
title: "205. 同构字符串"
aliases: ["yiduobo的每日leetcode 205.同构字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/146767928"
zhihu_id: "146767928"
zhihu_title: "yiduobo的每日leetcode 205.同构字符串"
question_id: "205"
question: "同构字符串"
problem_url: "https://leetcode.cn/problems/isomorphic-strings/"
created: "2020-06-08T21:30:58+08:00"
updated: "2020-06-08T21:30:58+08:00"
upvotes: 0
comments: 0
---

# 205. 同构字符串

> **[yiduobo的每日leetcode 205.同构字符串](https://zhuanlan.zhihu.com/p/146767928) · 知乎 · 2020-06-08 · 赞同 0**
> 力扣：[205. 同构字符串](https://leetcode.cn/problems/isomorphic-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

205.同构字符串<https://leetcode-cn.com/problems/isomorphic-strings/>

比较基础的题目。首先两个串如果不等长，那么一定不是同构的，接下来从头开始逐个字符往后扫描。

1、若s[index]已经有了映射，那么检测s[index]的映射是否等于t[index]。

2、若s[index]还没有映射，但是t[index]已经被映射过了，由于题目规定两个字符不能映射到同一字符，因此不同构。

3、若s[index]还没有映射，且t[index]没有被映射过，那么建立s[index]到t[index]的映射并记录t[index]已经被映射过。

最后附上python代码：

```python
class Solution(object):
    def isIsomorphic(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """

        if len(s) != len(t):
            return False

        char_dict = {}
        used_char = set()

        for index in range(len(s)):
            if s[index] in char_dict:
                if t[index] != char_dict[s[index]]:
                    return False
            elif t[index] in used_char:
                return False
            else:
                char_dict[s[index]] = t[index]
                used_char.add(t[index])

        return True
```
