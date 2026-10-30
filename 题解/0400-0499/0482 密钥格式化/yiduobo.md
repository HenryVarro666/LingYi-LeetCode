---
title: "482. 密钥格式化"
aliases: ["yiduobo的每日leetcode 482.密钥格式化"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/248994032"
zhihu_id: "248994032"
zhihu_title: "yiduobo的每日leetcode 482.密钥格式化"
question_id: "482"
question: "密钥格式化"
problem_url: "https://leetcode.cn/problems/license-key-formatting/"
created: "2020-09-16T21:38:00+08:00"
updated: "2020-09-16T21:38:00+08:00"
upvotes: 0
comments: 0
---

# 482. 密钥格式化

> **[yiduobo的每日leetcode 482.密钥格式化](https://zhuanlan.zhihu.com/p/248994032) · 知乎 · 2020-09-16 · 赞同 0**
> 力扣：[482. 密钥格式化](https://leetcode.cn/problems/license-key-formatting/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

482.密钥格式化<https://leetcode-cn.com/problems/license-key-formatting/>

比较基础的题目。去掉字符串中的破折号之后，计算字符串的长度以及第一段的长度，然后一趟扫描逐个处理每个字符即可。

最后附上python代码：

```python
class Solution(object):
    def licenseKeyFormatting(self, S, K):
        """
        :type S: str
        :type K: int
        :rtype: str
        """

        S = S.replace('-', '')
        l = len(S)
        cnt = l % K
        if cnt > 0:
            cnt = K - cnt
        
        res = ''
        for index in range(len(S)):
            char = S[index]
            if char >= 'a':
                char = chr(ord(char) - 32)
            res += char
            cnt += 1
            if cnt == K:
                if index != len(S) - 1:
                    res += '-'
                cnt = 0
        
        return res
```
