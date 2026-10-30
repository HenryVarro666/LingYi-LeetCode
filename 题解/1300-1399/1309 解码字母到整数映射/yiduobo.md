---
title: "1309. 解码字母到整数映射"
aliases: ["yiduobo的每日leetcode 1309.解码字母到整数映射"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/391928395"
zhihu_id: "391928395"
zhihu_title: "yiduobo的每日leetcode 1309.解码字母到整数映射"
question_id: "1309"
question: "解码字母到整数映射"
problem_url: "https://leetcode.cn/problems/decrypt-string-from-alphabet-to-integer-mapping/"
created: "2021-07-21T22:26:10+08:00"
updated: "2021-07-21T22:26:10+08:00"
upvotes: 0
comments: 0
---

# 1309. 解码字母到整数映射

> **[yiduobo的每日leetcode 1309.解码字母到整数映射](https://zhuanlan.zhihu.com/p/391928395) · 知乎 · 2021-07-21 · 赞同 0**
> 力扣：[1309. 解码字母到整数映射](https://leetcode.cn/problems/decrypt-string-from-alphabet-to-integer-mapping/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1309.解码字母到整数映射

[力扣](https://leetcode-cn.com/problems/decrypt-string-from-alphabet-to-integer-mapping/)

题目中的j到z由两位整数和后缀'\#'来表示，那么我们可以从后往前一趟遍历。若当前字符为\#，那么就将其与之前的两个字符组合起来解码，然后往前移动三位到上一个未解码字符，否则直接解码当前字符，然后向前移动一位到上一个未解码字符。

扫描完成后，所有字符的解码就完成了，此时只需将答案倒序输出即可。

最后附上python代码：

```python
class Solution(object):
    def freqAlphabets(self, s):
        """
        :type s: str
        :rtype: str
        """

        res = []
        p = len(s) - 1
        while p >= 0:
            if s[p] == '#':
                res.append(chr(int(s[p - 2]) * 10 + int(s[p - 1]) + 96))
                p -= 3
            else:
                res.append(chr(int(s[p]) + 96))
                p -= 1
        
        return ''.join(res[::-1])
```
