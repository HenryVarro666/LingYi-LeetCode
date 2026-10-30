---
title: "1417. 重新格式化字符串"
aliases: ["yiduobo的每日leetcode 1417.重新格式化字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/407070961"
zhihu_id: "407070961"
zhihu_title: "yiduobo的每日leetcode 1417.重新格式化字符串"
question_id: "1417"
question: "重新格式化字符串"
problem_url: "https://leetcode.cn/problems/reformat-the-string/"
created: "2021-09-05T16:39:17+08:00"
updated: "2021-09-05T16:39:17+08:00"
upvotes: 2
comments: 0
---

# 1417. 重新格式化字符串

> **[yiduobo的每日leetcode 1417.重新格式化字符串](https://zhuanlan.zhihu.com/p/407070961) · 知乎 · 2021-09-05 · 赞同 2**
> 力扣：[1417. 重新格式化字符串](https://leetcode.cn/problems/reformat-the-string/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1417.重新格式化字符串

[力扣](https://leetcode-cn.com/problems/reformat-the-string/)

为了使得最终答案中数字与字符交替出现，那么数字出现的次数以及字符的次数之间的差值必须小于1。若满足该条件，那么我们从出现较多的那一种开始交替使用来构造答案。若不满足，那么直接返回空字符串即可。

最后附上python代码：

```python
class Solution(object):
    def reformat(self, s):
        """
        :type s: str
        :rtype: str
        """

        char_list = []
        digit_list = []
        for char in s:
            if char >= '0' and char <= '9':
                digit_list.append(char)
            else:
                char_list.append(char)
        
        char_cnt = len(char_list)
        digit_cnt = len(digit_list)
        if abs(char_cnt - digit_cnt) > 1:
            return ""
        
        res = []
        if char_cnt > digit_cnt:
            for index in range(digit_cnt):
                res.append(char_list[index])
                res.append(digit_list[index])
            res.append(char_list[-1])
        else:
            for index in range(char_cnt):
                res.append(digit_list[index])
                res.append(char_list[index])
            if digit_cnt > char_cnt:
                res.append(digit_list[-1])
        
        return ''.join(res)
```
