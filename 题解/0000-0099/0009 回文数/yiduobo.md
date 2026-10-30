---
title: "9. 回文数"
aliases: ["yiduobo的每日leetcode 9.回文数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "题单/数学算法", "题单/面试经典-150-题", "题单/数学算法/七-杂项", "题单/面试经典-150-题/数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/113993014"
zhihu_id: "113993014"
zhihu_title: "yiduobo的每日leetcode 9.回文数"
question_id: "9"
question: "回文数"
problem_url: "https://leetcode.cn/problems/palindrome-number/"
difficulty: "Easy"
created: "2020-03-17T21:44:48+08:00"
updated: "2020-03-17T21:44:48+08:00"
upvotes: 0
comments: 0
---

# 9. 回文数

> **[yiduobo的每日leetcode 9.回文数](https://zhuanlan.zhihu.com/p/113993014) · 知乎 · 2020-03-17 · 赞同 0**
> 力扣：[9. 回文数](https://leetcode.cn/problems/palindrome-number/) · Easy · 灵茶山艾府：[详细解释，比官方题解少循环一次（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

9.回文数<https://leetcode-cn.com/problems/palindrome-number/>

首先，负数一定不是回文数。

接下来，0是符合要求的，但是其他以0结尾的数都不符合。

对于其他的情况，都可以按整数翻转的做法，翻转后n / 2位之后比较与前n / 2位是否一样。需要注意的是这里的n如果是奇数，那么需要将较大的数整除10之后再进行比较。

最后附上python代码：

```python
class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        if x < 0:
            return False
        if x == 0:
            return True
        if x % 10 == 0:
            return False

        y = 0
        while x > y:
            y = y * 10 + x % 10
            x /= 10
        
        if x == y or x == y / 10:
            return True
        
        return False
```
