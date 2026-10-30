---
title: "3697. 计算十进制表示"
aliases: ["yiduobo的每日leetcode 3697.计算十进制表示"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956334846902243697"
zhihu_id: "1956334846902243697"
zhihu_title: "yiduobo的每日leetcode 3697.计算十进制表示"
question_id: "3697"
question: "计算十进制表示"
problem_url: "https://leetcode.cn/problems/compute-decimal-representation/"
difficulty: "Easy"
created: "2025-10-03T15:37:15+08:00"
updated: "2025-10-03T15:37:15+08:00"
upvotes: 0
comments: 0
---

# 3697. 计算十进制表示

> **[yiduobo的每日leetcode 3697.计算十进制表示](https://zhuanlan.zhihu.com/p/1956334846902243697) · 知乎 · 2025-10-03 · 赞同 0**
> 力扣：[3697. 计算十进制表示](https://leetcode.cn/problems/compute-decimal-representation/) · Easy · 灵茶山艾府：[遍历数位（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3697.计算十进制表示

[3697. 计算十进制表示 - 力扣（LeetCode）](https://leetcode.cn/problems/compute-decimal-representation/description/)

题目给出一个正整数n。如果一个正整数可以表示为1到9的单个数字，与10的非负整数次幂之积，则称这个整数为一个10进制分量。现在要求将n拆分成若干个仅由10进制分量组成的和，且使用的10进制分量数量最少。返回这些10进制分量的数组，并按照大小降序排列。

题目实际上就是要将n中非零的个位、整十、整百、整千等拆分出来，于是只需使用模10除以10的方法逐位分离n的数位，同时使用一个变量p记录当前分离出来的位对应的10的幂次，然后将所以非零数位与p的乘积添加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def decimalRepresentation(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        
        res = []
        p = 1
        while n:
            if n % 10 != 0:
                res.append(n % 10 * p)
            n //= 10
            p *= 10
        
        return res[::-1]
```
