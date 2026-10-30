---
title: "342. 4的幂"
aliases: ["yiduobo的每日leetcode 342. 4的幂"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163011059"
zhihu_id: "163011059"
zhihu_title: "yiduobo的每日leetcode 342. 4的幂"
question_id: "342"
question: "4的幂"
problem_url: "https://leetcode.cn/problems/power-of-four/"
difficulty: "Easy"
created: "2020-07-22T22:00:39+08:00"
updated: "2020-07-22T22:00:39+08:00"
upvotes: 0
comments: 0
---

# 342. 4的幂

> **[yiduobo的每日leetcode 342. 4的幂](https://zhuanlan.zhihu.com/p/163011059) · 知乎 · 2020-07-22 · 赞同 0**
> 力扣：[342. 4的幂](https://leetcode.cn/problems/power-of-four/) · Easy · 灵茶山艾府：[两种方法：位运算 / 数学（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

342\. 4的幂<https://leetcode-cn.com/problems/power-of-four/>

我在这里采用的是类似于3的幂的做法，首先计算出整数范围内最大的4的幂，为1073741824。但是这里不能直接通过1073741824模n来判断，因为n可能是4^k \* 2这种形式的。

注意到对于所有4的幂，除了4^0\=1之外，其他幂都必然以4或者6结尾，那么对于4^k \* 2这种形式就必然以2或者8结尾，于是在上面1073741824模n的基础上，再判断n%10是否等于4或者6即可。

最后附上python代码：

```python
class Solution(object):
    def isPowerOfFour(self, num):
        """
        :type num: int
        :rtype: bool
        """

        if num <= 0:
            return False

        if num == 1:
            return True

        if 1073741824 % num == 0 and num % 10 in (4, 6):
            return True

        return False
```
