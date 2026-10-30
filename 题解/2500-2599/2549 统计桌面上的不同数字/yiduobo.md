---
title: "2549. 统计桌面上的不同数字"
aliases: ["yiduobo的每日leetcode 2549.统计桌面上的不同数字"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638949084"
zhihu_id: "638949084"
zhihu_title: "yiduobo的每日leetcode 2549.统计桌面上的不同数字"
question_id: "2549"
question: "统计桌面上的不同数字"
problem_url: "https://leetcode.cn/problems/count-distinct-numbers-on-board/"
difficulty: "Easy"
rating: 1266
created: "2023-06-23T23:44:58+08:00"
updated: "2023-06-23T23:44:58+08:00"
upvotes: 0
comments: 0
---

# 2549. 统计桌面上的不同数字

> **[yiduobo的每日leetcode 2549.统计桌面上的不同数字](https://zhuanlan.zhihu.com/p/638949084) · 知乎 · 2023-06-23 · 赞同 0**
> 力扣：[2549. 统计桌面上的不同数字](https://leetcode.cn/problems/count-distinct-numbers-on-board/) · Easy · 灵茶山艾府：[数学 O(1) 解（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2549.统计桌面上的不同数字

[力扣](https://leetcode.cn/problems/count-distinct-numbers-on-board/)

对于任意大于等于3的整数n，都有n % (n - 1) \= 1，也就是说对于任意大于等于3的n而言，桌面上最后的数字必然是2到n，一共是n - 1个数。另一方面，对于n等于1或者2这两种情况，桌面上的数字不会发生改变，因此当n \<\= 2时，答案为1，否则为n - 1。

最后附上python代码：

```python
class Solution(object):
    def distinctIntegers(self, n):
        """
        :type n: int
        :rtype: int
        """

        if n == 1 or n == 2:
            return 1
        
        return n - 1
```
