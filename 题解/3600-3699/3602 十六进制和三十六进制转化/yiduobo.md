---
title: "3602. 十六进制和三十六进制转化"
aliases: ["yiduobo的每日leetcode 3062.十六进制和三十六进制转化"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1941641801648824619"
zhihu_id: "1941641801648824619"
zhihu_title: "yiduobo的每日leetcode 3062.十六进制和三十六进制转化"
question_id: "3602"
question: "十六进制和三十六进制转化"
problem_url: "https://leetcode.cn/problems/hexadecimal-and-hexatrigesimal-conversion/"
difficulty: "Easy"
title_number_fixed: ["3062→3602"]
created: "2025-08-20T23:28:29+08:00"
updated: "2025-08-20T23:28:29+08:00"
upvotes: 1
comments: 0
---

# 3602. 十六进制和三十六进制转化

> **[yiduobo的每日leetcode 3062.十六进制和三十六进制转化](https://zhuanlan.zhihu.com/p/1941641801648824619) · 知乎 · 2025-08-20 · 赞同 1**
> 力扣：[3602. 十六进制和三十六进制转化](https://leetcode.cn/problems/hexadecimal-and-hexatrigesimal-conversion/) · Easy · 灵茶山艾府：[库函数写法（Python/Java/C++/Go）](灵茶山艾府.md)
> 原文标题里的题号写作 3062，这里改成 3602：文章里的力扣链接和题名都对应这道题

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3602.十六进制和三十六进制转化

[3602. 十六进制和三十六进制转化 - 力扣（LeetCode）](https://leetcode.cn/problems/hexadecimal-and-hexatrigesimal-conversion/)

题目给出一个整数n，要求返回n^2的十六进制表示以及n^3的三十六进制表示拼接而成的字符串。十六进制由A到F表示10到15的值，三十六进制则使用A到Z表示10到35的值。

常规的进制转化问题，直接使用模b除以b的方法计算转换后的数位，反转后即为对应的b进制数。需要注意要将大于等于10的数位转换为字母。

最后附上python代码：

```python
class Solution(object):
    def concatHex36(self, n):
        """
        :type n: int
        :rtype: str
        """
        
        def trans(x, base):
            res = []
            while x:
                res.append(x % base)
                x //= base
            
            res.reverse()
            return [str(v) if 0 <= v <= 9 else chr(v + 55) for v in res]
        
        return ''.join(trans(n * n, 16) + trans(n * n * n, 36))
```
