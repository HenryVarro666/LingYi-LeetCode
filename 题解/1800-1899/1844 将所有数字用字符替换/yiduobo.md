---
title: "1844. 将所有数字用字符替换"
aliases: ["yiduobo的每日leetcode 1844.将所有数字用字符替换"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/469697618"
zhihu_id: "469697618"
zhihu_title: "yiduobo的每日leetcode 1844.将所有数字用字符替换"
question_id: "1844"
question: "将所有数字用字符替换"
problem_url: "https://leetcode.cn/problems/replace-all-digits-with-characters/"
created: "2022-02-20T00:17:49+08:00"
updated: "2022-02-20T00:17:49+08:00"
upvotes: 0
comments: 1
---

# 1844. 将所有数字用字符替换

> **[yiduobo的每日leetcode 1844.将所有数字用字符替换](https://zhuanlan.zhihu.com/p/469697618) · 知乎 · 2022-02-20 · 赞同 0**
> 力扣：[1844. 将所有数字用字符替换](https://leetcode.cn/problems/replace-all-digits-with-characters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1844.将所有数字用字符替换

[力扣](https://leetcode-cn.com/problems/replace-all-digits-with-characters/)

比较基础的题目，一趟扫描，利用ascii码来完成题目替换的要求即可。

最后附上python代码：

```python
class Solution(object):
    def replaceDigits(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = []
        for index in range(0, len(s), 2):
            char = s[index]
            res.append(char)
            if index + 1 < len(s):
                offset = int(s[index + 1])
                res.append(chr(ord(char) + offset))
        
        return ''.join(res)
```
