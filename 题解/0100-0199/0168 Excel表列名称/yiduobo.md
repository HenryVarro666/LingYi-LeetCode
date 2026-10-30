---
title: "168. Excel表列名称"
aliases: ["yiduobo的每日leetcode 168.Excel表列名称"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/144615116"
zhihu_id: "144615116"
zhihu_title: "yiduobo的每日leetcode 168.Excel表列名称"
question_id: "168"
question: "Excel表列名称"
problem_url: "https://leetcode.cn/problems/excel-sheet-column-title/"
created: "2020-05-29T23:21:15+08:00"
updated: "2020-05-29T23:21:15+08:00"
upvotes: 0
comments: 0
---

# 168. Excel表列名称

> **[yiduobo的每日leetcode 168.Excel表列名称](https://zhuanlan.zhihu.com/p/144615116) · 知乎 · 2020-05-29 · 赞同 0**
> 力扣：[168. Excel表列名称](https://leetcode.cn/problems/excel-sheet-column-title/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

168.Excel表列名称<https://leetcode-cn.com/problems/excel-sheet-column-title/>

看题目写这么大一堆，其实本质上就是整数的二十六进制表示。这里需要注意的一点是，列A到列Z是取1到26，但是正常的二十六进制是0到25，所以在转换时需要特别判断模26等于0的情况。

另外，A的ascii码是65，我在这里采取了chr(余数 + 64)的写法来完成1-26到A-Z的转换。

最后附上python代码：

```python
class Solution(object):
    def convertToTitle(self, n):
        """
        :type n: int
        :rtype: str
        """

        res = ''
        while n:
            tmp = n % 26
            n /= 26
            if not tmp:
                n -= 1
                tmp = 26
            res = chr(tmp + 64) + res

        return res
```
