---
title: "389. 找不同"
aliases: ["yiduobo的每日leetcode 389.找不同"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/172532576"
zhihu_id: "172532576"
zhihu_title: "yiduobo的每日leetcode 389.找不同"
question_id: "389"
question: "找不同"
problem_url: "https://leetcode.cn/problems/find-the-difference/"
created: "2020-08-07T23:27:51+08:00"
updated: "2020-08-07T23:27:51+08:00"
upvotes: 0
comments: 0
---

# 389. 找不同

> **[yiduobo的每日leetcode 389.找不同](https://zhuanlan.zhihu.com/p/172532576) · 知乎 · 2020-08-07 · 赞同 0**
> 力扣：[389. 找不同](https://leetcode.cn/problems/find-the-difference/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

389.找不同<https://leetcode-cn.com/problems/find-the-difference/>

比较基础的题目，直接统计两个字符串中各个字符出现的次数即可。当然也可以将题目看成两个数字串，找出出现奇数次的那个数字，因此也可以通过异或来解决问题。

最后附上python代码：

```python
class Solution(object):
    def findTheDifference(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """

        char_dict = {}
        for char in t:
            char_dict[char] = char_dict.get(char, 0) + 1
        for char in s:
            char_dict[char] -= 1
        
        for char in char_dict:
            if char_dict[char] > 0:
                return char
```
