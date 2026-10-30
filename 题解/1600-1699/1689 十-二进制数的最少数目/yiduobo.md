---
title: "1689. 十-二进制数的最少数目"
aliases: ["yiduobo的每日leetcode 1689.十-二进制数的最少数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/446828318"
zhihu_id: "446828318"
zhihu_title: "yiduobo的每日leetcode 1689.十-二进制数的最少数目"
question_id: "1689"
question: "十-二进制数的最少数目"
problem_url: "https://leetcode.cn/problems/partitioning-into-minimum-number-of-deci-binary-numbers/"
difficulty: "Medium"
rating: 1355
created: "2021-12-17T23:14:54+08:00"
updated: "2021-12-17T23:14:54+08:00"
upvotes: 0
comments: 0
---

# 1689. 十-二进制数的最少数目

> **[yiduobo的每日leetcode 1689.十-二进制数的最少数目](https://zhuanlan.zhihu.com/p/446828318) · 知乎 · 2021-12-17 · 赞同 0**
> 力扣：[1689. 十-二进制数的最少数目](https://leetcode.cn/problems/partitioning-into-minimum-number-of-deci-binary-numbers/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1689.十-二进制数的最少数目

[力扣](https://leetcode-cn.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/)

题目要求将一个整数n分解成若干个只由0和1组成的十进制数，且这个分解的数目最少。由于每一位只能是0或者1，那么对于n的某一位，不妨设其为k，就需要分解出来的数中有k个该位为1。由于位与位之间是相互独立的，那么就只需找出n中最大的位k，这个k就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def minPartitions(self, n):
        """
        :type n: str
        :rtype: int
        """

        res = 0
        for char in n:
            res = max(res, int(char))
        
        return res
```
