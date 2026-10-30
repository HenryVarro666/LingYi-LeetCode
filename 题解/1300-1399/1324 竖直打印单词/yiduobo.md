---
title: "1324. 竖直打印单词"
aliases: ["yiduobo的每日leetcode 1324.竖直打印单词"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394118849"
zhihu_id: "394118849"
zhihu_title: "yiduobo的每日leetcode 1324.竖直打印单词"
question_id: "1324"
question: "竖直打印单词"
problem_url: "https://leetcode.cn/problems/print-words-vertically/"
created: "2021-07-28T22:46:24+08:00"
updated: "2021-07-28T22:46:24+08:00"
upvotes: 0
comments: 0
---

# 1324. 竖直打印单词

> **[yiduobo的每日leetcode 1324.竖直打印单词](https://zhuanlan.zhihu.com/p/394118849) · 知乎 · 2021-07-28 · 赞同 0**
> 力扣：[1324. 竖直打印单词](https://leetcode.cn/problems/print-words-vertically/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1324.竖直打印单词

[力扣](https://leetcode-cn.com/problems/print-words-vertically/)

比较基础的题目，按空格分离单词后逐位输出即可。需要注意不能有后缀空格的情况。

最后附上python代码：

```python
class Solution(object):
    def printVertically(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        words = s.split(' ')
        res = []
        p = 0
        while True:
            flag = False
            tmp = []
            for index in range(len(words) - 1, -1, -1):
                if p < len(words[index]):
                    tmp.append(words[index][p])
                    flag = True
                elif flag:
                    tmp.append(' ')
            
            if len(tmp) == 0:
                break

            res.append(''.join(tmp[::-1]))
            p += 1
        
        return res
```
