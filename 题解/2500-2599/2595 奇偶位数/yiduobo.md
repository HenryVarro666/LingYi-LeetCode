---
title: "2595. 奇偶位数"
aliases: ["yiduobo的每日leetcode 2595.奇偶位数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/ku-han-shu", "leetcode/er-jin-zhi", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643827341"
zhihu_id: "643827341"
zhihu_title: "yiduobo的每日leetcode 2595.奇偶位数"
question_id: "2595"
question: "奇偶位数"
problem_url: "https://leetcode.cn/problems/number-of-even-and-odd-bits/"
difficulty: "Easy"
created: "2023-07-16T00:07:19+08:00"
updated: "2023-07-16T00:07:19+08:00"
upvotes: 1
comments: 0
---

# 2595. 奇偶位数

> **[yiduobo的每日leetcode 2595.奇偶位数](https://zhuanlan.zhihu.com/p/643827341) · 知乎 · 2023-07-16 · 赞同 1**
> 力扣：[2595. 奇偶位数](https://leetcode.cn/problems/number-of-even-and-odd-bits/) · Easy · 灵茶山艾府：[两种方法：从 O(logn) 到 O(1)（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2595.奇偶位数

[力扣](https://leetcode.cn/problems/number-of-even-and-odd-bits/)

使用一个变量p从0开始向上遍历所有的二进制位，对于当前遍历到的p，若n在这一位上为1，那么n与2^p执行与运算的结果就应该等于2^p，此时就应该根据p的奇偶性更新答案，然后利用异或运算将2^p从n中去除。重复此过程直到n变为0为止。

最后附上python代码：

```python
class Solution(object):
    def evenOddBit(self, n):
        """
        :type n: int
        :rtype: List[int]
        """

        res = [0, 0]
        p = 0
        while n > 0:
            if n & (1 << p) == (1 << p):
                res[p % 2] += 1
                n ^= (1 << p)
            p += 1
        
        return res
```
