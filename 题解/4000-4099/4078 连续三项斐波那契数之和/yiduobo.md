---
title: "4078. 连续三项斐波那契数之和"
aliases: ["yiduobo的每日leetcode 4078.连续三项斐波那契数之和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2093864941182890657"
zhihu_id: "2093864941182890657"
zhihu_title: "yiduobo的每日leetcode 4078.连续三项斐波那契数之和"
question_id: "4078"
question: "连续三项斐波那契数之和"
problem_url: "https://leetcode.cn/problems/three-fibonacci-sum/"
created: "2026-10-15T00:49:03+08:00"
updated: "2026-10-15T00:49:03+08:00"
upvotes: 0
comments: 0
---

# 4078. 连续三项斐波那契数之和

> **[yiduobo的每日leetcode 4078.连续三项斐波那契数之和](https://zhuanlan.zhihu.com/p/2093864941182890657) · 知乎 · 2026-10-15 · 赞同 0**
> 力扣：[4078. 连续三项斐波那契数之和](https://leetcode.cn/problems/three-fibonacci-sum/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4078.连续三项斐波那契数之和

<https://leetcode.cn/problems/three-fibonacci-sum/description/>

题目给出一个整数n，为n是否可以表示成斐波那契数列中连续三项之和。若可以，则返回true，否则返回false。

对于斐波那契数列中的连续三项f[index]、f[index + 1]以及f[index + 2]，这三者之和f[index] + f[index + 1] + f[index + 2]可以将前两项合并，那么得到的就是f[index + 2] \* 2。换言之，题目问的就是n是否为数列中某一项的两倍。

因此，在这里可以先判断n是否为奇数，若是，则返回false。否则先将n除以2，然后从0和1开始向后递推，直到计算的项大于等于n为止。若最后计算得到的这一项恰好等于n，那么答案就是true，否则就是false。

最后附上python代码：

```python
class Solution(object):
    def threeFibonacciSum(self, n):
        """
        :type n: int
        :rtype: bool
        """
        
        if n % 2 == 1:
            return False
        
        n //= 2
        a, b = 0, 1
        while b < n:
            a, b = b, a + b
        
        return b == n
```
