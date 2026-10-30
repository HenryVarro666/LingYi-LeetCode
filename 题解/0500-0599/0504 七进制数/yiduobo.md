---
title: "504. 七进制数"
aliases: ["yiduobo的每日leetcode 504.七进制数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/258951819"
zhihu_id: "258951819"
zhihu_title: "yiduobo的每日leetcode 504.七进制数"
question_id: "504"
question: "七进制数"
problem_url: "https://leetcode.cn/problems/base-7/"
created: "2020-09-24T20:43:10+08:00"
updated: "2020-09-24T20:43:10+08:00"
upvotes: 0
comments: 0
---

# 504. 七进制数

> **[yiduobo的每日leetcode 504.七进制数](https://zhuanlan.zhihu.com/p/258951819) · 知乎 · 2020-09-24 · 赞同 0**
> 力扣：[504. 七进制数](https://leetcode.cn/problems/base-7/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

504.七进制数<https://leetcode-cn.com/problems/base-7/>

比较基础的题目，直接仿照转二进制的方法，不断模七除以七即可。

需要注意在使用python2时对负数取模稍有差别，因此需要记录符号转换成正数来做。

最后附上python代码：

```python
class Solution(object):
    def convertToBase7(self, num):
        """
        :type num: int
        :rtype: str
        """

        if num == 0:
            return "0"

        neg_flag = False
        if num < 0:
            neg_flag = True
            num = -num
        res = []
        while num:
            res.append(str(num % 7))
            num /= 7
        res.reverse()
        if neg_flag:
            return "-" + ''.join(res)
        else:
            return ''.join(res)
```
