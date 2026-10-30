---
title: "1758. 生成交替二进制字符串的最少操作次数"
aliases: ["yiduobo的每日leetcode 1758.生成交替二进制字符串的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/459173569"
zhihu_id: "459173569"
zhihu_title: "yiduobo的每日leetcode 1758.生成交替二进制字符串的最少操作次数"
question_id: "1758"
question: "生成交替二进制字符串的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-changes-to-make-alternating-binary-string/"
difficulty: "Easy"
created: "2022-01-18T23:08:12+08:00"
updated: "2022-01-18T23:08:12+08:00"
upvotes: 0
comments: 0
---

# 1758. 生成交替二进制字符串的最少操作次数

> **[yiduobo的每日leetcode 1758.生成交替二进制字符串的最少操作次数](https://zhuanlan.zhihu.com/p/459173569) · 知乎 · 2022-01-18 · 赞同 0**
> 力扣：[1758. 生成交替二进制字符串的最少操作数](https://leetcode.cn/problems/minimum-changes-to-make-alternating-binary-string/) · Easy · 灵茶山艾府：[只有两种情况（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1758.生成交替二进制字符串的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-changes-to-make-alternating-binary-string/)

最终答案的字符串上有么偶数位全1，奇数位全0，要么正好反过来。

首先考虑偶数位全1，奇数位全0。若想达成这个条件，那么需要将偶数位上的1以及奇数位上的0全部进行翻转。记这两种数出现的次数之和为cnt，那么将字符串变为偶数位全1，奇数位全0的操作次数就等于cnt。

另一方面，如果想变成偶数位全0，奇数位全1，那么就需要统计偶数位上的0以及奇数位上的1，这个恰好与上面这种情况相反，因此这种情况下这些数出现次数总和必然就是len(s) - cnt。

综合上面的结论，那么就可以先统计得到cnt，然后最终答案就是min(cnt, len(s) - cnt)

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s):
        """
        :type s: str
        :rtype: int
        """

        cnt = 0
        for index in range(len(s)):
            if index % 2 == 0 and s[index] == '0':
                cnt += 1
            elif index % 2 == 1 and s[index] == '1':
                cnt += 1
        
        return min(cnt, len(s) - cnt)
```
