---
title: "831. 隐藏个人信息"
aliases: ["yiduobo的每日leetcode 831.隐藏个人信息"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/344823121"
zhihu_id: "344823121"
zhihu_title: "yiduobo的每日leetcode 831.隐藏个人信息"
question_id: "831"
question: "隐藏个人信息"
problem_url: "https://leetcode.cn/problems/masking-personal-information/"
created: "2021-01-22T19:13:23+08:00"
updated: "2021-01-22T19:13:23+08:00"
upvotes: 1
comments: 0
---

# 831. 隐藏个人信息

> **[yiduobo的每日leetcode 831.隐藏个人信息](https://zhuanlan.zhihu.com/p/344823121) · 知乎 · 2021-01-22 · 赞同 1**
> 力扣：[831. 隐藏个人信息](https://leetcode.cn/problems/masking-personal-information/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

831.隐藏个人信息

[力扣](https://leetcode-cn.com/problems/masking-personal-information/)

直接按照题目要求进行处理即可。python处理这类问题确实是很方便。

首先，将S通过@进行分割：

1、若分割后只有一个部分，说明S是一个电话号码，此时可以从后往前遍历S：

1-1）若当前的字符是一个数字，那么将cnt加一

1-2）当cnt为5、8或11时，应该加上-

1-3）当cnt小于等于4时，就将当前数字加入到答案中，否则应该在答案中加入\*

遍历完成后，若最终cnt的数目大于10，说明这是一个国际号码，应该再往答案中加入+

2、若分割后有两个部分，说明S是一个邮箱地址：

2-1）首先将第一部分的首字母转化为小写，然后加入到答案中

2-2）往答案中加入5个\*

2-3）接下来将第一部分的最后一个字母转化为小写并加入到答案中

2-4）往答案中加入@

2-5）最后遍历第二部分，将每个字符都转化为小写然后加入到答案中

最后附上python代码：

```python
class Solution(object):
    def maskPII(self, S):
        """
        :type S: str
        :rtype: str
        """

        parts = S.split('@')
        if len(parts) == 1:
            cnt = 0
            res = ''
            for char in S[::-1]:
                if char >= '0' and char <= '9':
                    cnt += 1
                    if cnt == 5 or cnt == 8 or cnt == 11:
                        res = '-' + res
                    if cnt <= 4:
                        res = char + res
                    else:
                        res = '*' + res
            
            if cnt > 10:
                res = '+' + res
        else:
            if parts[0][0] >= 'A' and parts[0][0] <= 'Z':
                res = chr(ord(parts[0][0]) + 32)
            else:
                res = parts[0][0]

            res += '*' * 5

            if parts[0][-1] >= 'A' and parts[0][-1] <= 'Z':
                res += chr(ord(parts[0][-1]) + 32)
            else:
                res += parts[0][-1]

            res += '@'

            for char in parts[1]:
                if char >= 'A' and char <= 'Z':
                    res = res + chr(ord(char) + 32)
                else:
                    res = res + char
        
        return res
```
