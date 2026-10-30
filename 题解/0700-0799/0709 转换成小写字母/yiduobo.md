---
title: "709. 转换成小写字母"
aliases: ["yiduobo的每日leetcode 709.转换成小写字母"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/324680494"
zhihu_id: "324680494"
zhihu_title: "yiduobo的每日leetcode 709.转换成小写字母"
question_id: "709"
question: "转换成小写字母"
problem_url: "https://leetcode.cn/problems/to-lower-case/"
difficulty: "Easy"
created: "2020-12-01T22:21:18+08:00"
updated: "2020-12-01T22:21:18+08:00"
upvotes: 0
comments: 0
---

# 709. 转换成小写字母

> **[yiduobo的每日leetcode 709.转换成小写字母](https://zhuanlan.zhihu.com/p/324680494) · 知乎 · 2020-12-01 · 赞同 0**
> 力扣：[709. 转换成小写字母](https://leetcode.cn/problems/to-lower-case/) · Easy · 灵茶山艾府：[三种方法：库函数/手动计算/位运算（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

790.转换成小写字母

[力扣](https://leetcode-cn.com/problems/to-lower-case/)

高级语言都是有函数可以直接用的，我这里采用的是ascii码转换的方法。大写字母ascii码在65到90之间，而小写字母则是97到122之间。

对于字符串中的某个字符，若其ascii码在65到90之间，那么该字母为大写字母，将其转换成ascii码之后加上32，再转换回字母就得到对应的小写字母了。

最后附上python代码：

```python
class Solution(object):
    def toLowerCase(self, str):
        """
        :type str: str
        :rtype: str
        """

        str_list = list(str)
        for index in range(len(str_list)):
            if str_list[index] >= 'A' and str_list[index] <= 'Z':
                str_list[index] = chr(ord(str_list[index]) + 32)
        
        return ''.join(str_list)
```
