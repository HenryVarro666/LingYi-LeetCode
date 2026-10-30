---
title: "1694. 重新格式化电话号码"
aliases: ["yiduobo的每日leetcode 1694.重新格式化电话号码"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/446993382"
zhihu_id: "446993382"
zhihu_title: "yiduobo的每日leetcode 1694.重新格式化电话号码"
question_id: "1694"
question: "重新格式化电话号码"
problem_url: "https://leetcode.cn/problems/reformat-phone-number/"
created: "2021-12-18T15:04:07+08:00"
updated: "2021-12-18T15:04:07+08:00"
upvotes: 0
comments: 0
---

# 1694. 重新格式化电话号码

> **[yiduobo的每日leetcode 1694.重新格式化电话号码](https://zhuanlan.zhihu.com/p/446993382) · 知乎 · 2021-12-18 · 赞同 0**
> 力扣：[1694. 重新格式化电话号码](https://leetcode.cn/problems/reformat-phone-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1694.重新格式化电话号码

[力扣](https://leetcode-cn.com/problems/reformat-phone-number/)

直接从左向右一趟扫描，对于当前字符：

1、若该字符为破折号或者空格，那么直接跳过处理下一个字符

2、若该字符为数字，那么将其加入到答案数组中，并将当前的数字计数器cnt加上1。若此时的cnt变成了3，那么在答案数组的末尾加入一个破折号，同时将cnt清0

遍历完成后，此时还有两种特殊情况：

1、若cnt\=0，说明此时的号码恰好按三个一组分好了，但是上面的操作会在最后一组的后面额外添加一个破折号，因此需要将其删去

2、若cnt\=1，说明最后出现了一个落单的字符，是不符合题目要求的。此时应该将其与倒数第二组的三个字符综合起来分成两个长度为2的部分，具体操作只需要将倒数第二个破折号与倒数第三个数字对调即可

最后附上python代码：

```python
class Solution(object):
    def reformatNumber(self, number):
        """
        :type number: str
        :rtype: str
        """

        res = []
        cnt = 0
        for char in number:
            if char == '-' or char == ' ':
                continue
            res.append(char)
            cnt += 1
            if cnt == 3:
                res.append('-')
                cnt = 0
        
        if cnt == 0:
            res.pop()
        elif cnt == 1:
            res[-2] = res[-3]
            res[-3] = '-'

        return ''.join(res)
```
