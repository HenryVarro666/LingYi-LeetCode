---
title: "816. 模糊坐标"
aliases: ["yiduobo的每日leetcode 816.模糊坐标"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/343830079"
zhihu_id: "343830079"
zhihu_title: "yiduobo的每日leetcode 816.模糊坐标"
question_id: "816"
question: "模糊坐标"
problem_url: "https://leetcode.cn/problems/ambiguous-coordinates/"
created: "2021-01-15T22:31:18+08:00"
updated: "2021-01-15T22:31:18+08:00"
upvotes: 0
comments: 0
---

# 816. 模糊坐标

> **[yiduobo的每日leetcode 816.模糊坐标](https://zhuanlan.zhihu.com/p/343830079) · 知乎 · 2021-01-15 · 赞同 0**
> 力扣：[816. 模糊坐标](https://leetcode.cn/problems/ambiguous-coordinates/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

816.模糊坐标

[力扣](https://leetcode-cn.com/problems/ambiguous-coordinates/)

首先去掉S两侧的括号，然后将S分为两个部分，分别判断这两个部分可以形成的合法坐标，然后再两两组合起来加入到答案中。

对于一个字符串：

1、若其长度为1，那么可以形成的合法坐标就是其本身

2、若其长度大于1：

2-1）首位不为0，那么其本身是合法坐标之一

2-2）末位不为0，那么可以尝试在里面加入小数点。进一步的，若首位为0，那么只能将小数点加在0后面；若首位不为0，则小数点可以在首位到末位之间随意放置。

最后附上python代码：

```python
class Solution(object):
    def ambiguousCoordinates(self, S):
        """
        :type S: str
        :rtype: List[str]
        """

        S = S[1:-1]
        n = len(S)
        res = []
        for index in range(1, n):
            part_one = self.check(S[:index])
            part_two = self.check(S[index:])
            res.extend(["(%s, %s)" % (x, y) for x in part_one for y in part_two])
        
        return res
    
    def check(self, s):
        if len(s) == 1:
            return [s]

        res = []
        if s[0] != '0':
            res.append(s)
        
        if s[-1] != '0':
            if s[0] == '0':
                res.append(s[0] + '.' + s[1:])
            else:
                for index in range(1, len(s)):
                    res.append(s[:index] + '.' + s[index:])
        
        return res
```
