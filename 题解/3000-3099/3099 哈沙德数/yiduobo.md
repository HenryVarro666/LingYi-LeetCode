---
title: "3099. 哈沙德数"
aliases: ["yiduobo的每日leetcode 3099.哈沙德数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699858092"
zhihu_id: "699858092"
zhihu_title: "yiduobo的每日leetcode 3099.哈沙德数"
question_id: "3099"
question: "哈沙德数"
problem_url: "https://leetcode.cn/problems/harshad-number/"
difficulty: "Easy"
created: "2024-05-26T00:14:50+08:00"
updated: "2024-05-26T00:14:50+08:00"
upvotes: 2
comments: 0
---

# 3099. 哈沙德数

> **[yiduobo的每日leetcode 3099.哈沙德数](https://zhuanlan.zhihu.com/p/699858092) · 知乎 · 2024-05-26 · 赞同 2**
> 力扣：[3099. 哈沙德数](https://leetcode.cn/problems/harshad-number/) · Easy · 灵茶山艾府：[不使用字符串，O(1) 空间写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3099.哈沙德数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/harshad-number/description/)

通过模10除10的操作逐位分离x中的数位并累加到s中，然后判断x能否被s整除即可。

最后附上python代码：

```python
class Solution(object):
    def sumOfTheDigitsOfHarshadNumber(self, x):
        """
        :type x: int
        :rtype: int
        """

        tmp = x
        s = 0
        while tmp:
            s += tmp % 10
            tmp //= 10
        
        if x % s == 0:
            return s
        return -1
```
