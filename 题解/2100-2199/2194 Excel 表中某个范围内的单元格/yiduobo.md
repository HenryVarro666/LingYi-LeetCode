---
title: "2194. Excel表中某个范围内的单元格"
aliases: ["yiduobo的每日leetcode 2194.Excel表中某个范围内的单元格"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/string", "leetcode/enumeration", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/538052529"
zhihu_id: "538052529"
zhihu_title: "yiduobo的每日leetcode 2194.Excel表中某个范围内的单元格"
question_id: "2194"
question: "Excel 表中某个范围内的单元格"
problem_url: "https://leetcode.cn/problems/cells-in-a-range-on-an-excel-sheet/"
difficulty: "Easy"
created: "2022-07-06T00:12:22+08:00"
updated: "2022-07-06T00:12:22+08:00"
upvotes: 0
comments: 0
---

# 2194. Excel表中某个范围内的单元格

> **[yiduobo的每日leetcode 2194.Excel表中某个范围内的单元格](https://zhuanlan.zhihu.com/p/538052529) · 知乎 · 2022-07-06 · 赞同 0**
> 力扣：[2194. Excel 表中某个范围内的单元格](https://leetcode.cn/problems/cells-in-a-range-on-an-excel-sheet/) · Easy · 灵茶山艾府：[模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2194.Excel表中某个范围内的单元格

[力扣](https://leetcode.cn/problems/cells-in-a-range-on-an-excel-sheet/)

比较基础的题目，直接按先列后行的顺序进行遍历，将列和行拼起来填充到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def cellsInRange(self, s):
        """
        :type s: str
        :rtype: List[str]
        """

        c1 = ord(s[0])
        c2 = ord(s[3])
        r1 = int(s[1])
        r2 = int(s[4])
        res = []
        for c in range(c1, c2 + 1):
            for r in range(r1, r2 + 1):        
                res.append(chr(c) + str(r))
        
        return res
```
