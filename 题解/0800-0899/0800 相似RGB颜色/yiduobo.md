---
title: "800. 相似RGB颜色"
aliases: ["yiduobo的每日leetcode 800.相似RGB颜色"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/606727619"
zhihu_id: "606727619"
zhihu_title: "yiduobo的每日leetcode 800.相似RGB颜色"
question_id: "800"
question: "相似RGB颜色"
problem_url: "https://leetcode.cn/problems/similar-rgb-color/"
created: "2023-02-16T03:22:28+08:00"
updated: "2023-02-16T03:22:28+08:00"
upvotes: 0
comments: 0
---

# 800. 相似RGB颜色

> **[yiduobo的每日leetcode 800.相似RGB颜色](https://zhuanlan.zhihu.com/p/606727619) · 知乎 · 2023-02-16 · 赞同 0**
> 力扣：[800. 相似RGB颜色](https://leetcode.cn/problems/similar-rgb-color/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

800.相似RGB颜色

[力扣](https://leetcode.cn/problems/similar-rgb-color/)

题目给出一个由三个负的平方项组成的表达式，要求这个表达式的结果最大。换言之，就是要让三个平方项中括号的绝对值最小，于是可以从0到15枚举所有颜色，选择与当前差值绝对值最小的作为最终答案。

需要注意的是，这里的绝对值需要在16进制下进行计算。

最后附上python代码：

```python
class Solution(object):
    def similarRGB(self, color):
        """
        :type color: str
        :rtype: str
        """

        c = []
        for index in range(1, 7, 2):
            c.append(0)
            if '0' <= color[index] <= '9':
                c[-1] += int(color[index]) * 16
            else:
                c[-1] += (ord(color[index]) - 87) * 16
            
            if '0' <= color[index + 1] <= '9':
                c[-1] += int(color[index + 1])
            else:
                c[-1] += ord(color[index + 1]) - 87

        mi = [0, 0, 0]
        for v in range(1, 16):
            for index in range(3):
                if abs(c[index] - mi[index] * 17) > abs(c[index] - v * 17):
                    mi[index] = v

        res = '#'
        for v in mi:
            if v >= 10:
                res += chr(v + 87)
                res += chr(v + 87)
            else:
                res += str(v)
                res += str(v)
        
        return res
```
