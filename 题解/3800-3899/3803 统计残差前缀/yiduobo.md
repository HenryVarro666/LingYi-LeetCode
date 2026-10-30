---
title: "3803. 统计残差前缀"
aliases: ["yiduobo的每日leetcode 3803.统计残差前缀"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1993822132732445612"
zhihu_id: "1993822132732445612"
zhihu_title: "yiduobo的每日leetcode 3803.统计残差前缀"
question_id: "3803"
question: "统计残差前缀"
problem_url: "https://leetcode.cn/problems/count-residue-prefixes/"
difficulty: "Easy"
created: "2026-01-13T02:40:52+08:00"
updated: "2026-01-13T02:40:55+08:00"
upvotes: 0
comments: 0
---

# 3803. 统计残差前缀

> **[yiduobo的每日leetcode 3803.统计残差前缀](https://zhuanlan.zhihu.com/p/1993822132732445612) · 知乎 · 2026-01-13 · 赞同 0**
> 力扣：[3803. 统计残差前缀](https://leetcode.cn/problems/count-residue-prefixes/) · Easy · 灵茶山艾府：[两种方法：哈希集合 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3803.统计残差前缀

[100959. 统计残差前缀 - 力扣（LeetCode）](https://leetcode.cn/problems/count-residue-prefixes/description/)

题目给出一个仅由小写英文字母组成的字符串s。

若s的某个前缀prefix中不同字符的数量等于len(prefix) % 3，那么就称prefix为残差前缀。

问s中残差前缀的数量。

对s进行一趟遍历，使用集合记录每种前缀中不同字符的数量。接下来对于当前前缀，若字符串中字符的数量恰好等于前缀长度模3，那么就更新答案。

这里的一个隐藏条件就是对于当前的前缀s[:index + 1]，是在上一个前缀s[:index]的基础上，新增字符s[index]得到的，因此可以在上一个前缀字符集的基础上，加入s[index]得到当前前缀的字符集。另一方面，第0到第index个字符形成的前缀长度为index + 1，因此判断的基准就是字符集的大小，是否等于(index + 1) % 3。

最后附上python代码：

```python
class Solution(object):
    def residuePrefixes(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        cnt = set()
        res = 0
        for index, c in enumerate(s):
            cnt.add(c)
            if len(cnt) == (index + 1) % 3:
                res += 1
        
        return res
```
