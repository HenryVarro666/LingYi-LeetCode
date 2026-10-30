---
title: "633. 平方数之和"
aliases: ["yiduobo的每日leetcode 633.平方数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/enumeration", "题单/滑动窗口与双指针", "题单/数学算法", "题单/滑动窗口与双指针/三-单序列双指针", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/270643987"
zhihu_id: "270643987"
zhihu_title: "yiduobo的每日leetcode 633.平方数之和"
question_id: "633"
question: "平方数之和"
problem_url: "https://leetcode.cn/problems/sum-of-square-numbers/"
difficulty: "Medium"
created: "2020-10-31T19:24:46+08:00"
updated: "2020-10-31T19:24:46+08:00"
upvotes: 0
comments: 0
---

# 633. 平方数之和

> **[yiduobo的每日leetcode 633.平方数之和](https://zhuanlan.zhihu.com/p/270643987) · 知乎 · 2020-10-31 · 赞同 0**
> 力扣：[633. 平方数之和](https://leetcode.cn/problems/sum-of-square-numbers/) · Medium · 灵茶山艾府：[两种方法：枚举/双指针（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

633.平方数之和

[力扣](https://leetcode-cn.com/problems/sum-of-square-numbers/)

应该存在数学定理能在常数时间解决这个问题，不过具体怎么说的记不太清了。我这里使用的是O(sqrt(n))的枚举法，直接枚举a，然后通过sqrt(c - a^2)得到b，再判断a^2 + b^2是否等于c。

最后附上python代码：

```python
class Solution(object):
    def judgeSquareSum(self, c):
        """
        :type c: int
        :rtype: bool
        """

        a = 0
        while (a * a + a * a <= c):
            b = int(sqrt(c - a * a))
            if a * a + b * b == c:
                return True
            a += 1

        return False
```
