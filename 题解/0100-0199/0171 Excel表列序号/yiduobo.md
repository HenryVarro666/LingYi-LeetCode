---
title: "171. Excel表列序号"
aliases: ["yiduobo的每日leetcode 171.Excel表列序号"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144790817"
zhihu_id: "144790817"
zhihu_title: "yiduobo的每日leetcode 171.Excel表列序号"
question_id: "171"
question: "Excel表列序号"
problem_url: "https://leetcode.cn/problems/excel-sheet-column-number/"
created: "2020-05-30T23:10:23+08:00"
updated: "2020-05-30T23:10:23+08:00"
upvotes: 0
comments: 0
---

# 171. Excel表列序号

> **[yiduobo的每日leetcode 171.Excel表列序号](https://zhuanlan.zhihu.com/p/144790817) · 知乎 · 2020-05-30 · 赞同 0**
> 力扣：[171. Excel表列序号](https://leetcode.cn/problems/excel-sheet-column-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

171.Excel表列序号<https://leetcode-cn.com/problems/excel-sheet-column-number/>

与168题相反，但是本质依然是26进制转换。同样需要注意这里的26进制是从1到26而不是0到25，另外依然可以运用大写A的ascii码是65来方便进制转换。

最后附上python代码：

```python
class Solution(object):
    def titleToNumber(self, s):
        """
        :type s: str
        :rtype: int
        """

        res = 0
        for char in s:
            res = res * 26 + ord(char) - 64

        return res
```
