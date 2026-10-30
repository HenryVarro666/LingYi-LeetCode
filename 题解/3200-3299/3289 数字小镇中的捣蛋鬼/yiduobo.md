---
title: "3289. 数字小镇中的捣蛋鬼"
aliases: ["yiduobo的每日leetcode 3289.数字小镇中的捣蛋鬼"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/875320555"
zhihu_id: "875320555"
zhihu_title: "yiduobo的每日leetcode 3289.数字小镇中的捣蛋鬼"
question_id: "3289"
question: "数字小镇中的捣蛋鬼"
problem_url: "https://leetcode.cn/problems/the-two-sneaky-numbers-of-digitville/"
difficulty: "Easy"
created: "2024-10-08T22:17:16+08:00"
updated: "2024-10-08T22:17:16+08:00"
upvotes: 1
comments: 0
---

# 3289. 数字小镇中的捣蛋鬼

> **[yiduobo的每日leetcode 3289.数字小镇中的捣蛋鬼](https://zhuanlan.zhihu.com/p/875320555) · 知乎 · 2024-10-08 · 赞同 1**
> 力扣：[3289. 数字小镇中的捣蛋鬼](https://leetcode.cn/problems/the-two-sneaky-numbers-of-digitville/) · Easy · 灵茶山艾府：[O(1) 空间做法：位运算 / 数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3289.数字小镇中的捣蛋鬼

[. - 力扣（LeetCode）](https://leetcode.cn/problems/the-two-sneaky-numbers-of-digitville/)

题目给出一个数字列表nums，其中包含从0到n - 1中的整数，其中有两个数字出现了两次，剩下的所有数字都只出现一次。现在需要找出出现了两次的数字是什么。

最简单的做法自然是一趟遍历，使用哈希表统计每种数字出现的次数。

除此之外，通过求和则可以得到空间复杂度为O(1)的做法。

若只有一个出现了两次的数字x，那么数组和s \= 0 + 1 + ... + n - 1 + x \= n \* (n - 1) // 2 + x，此时可以直接解出x \= s - n \* (n - 1) // 2。

需要注意这里的n不是应该是nums的长度减去2，因为存在两个重复数字。

现在有两个出现了两次的数字x和y，那么就需要至少两个方程。

首先依然是

s \= 0 + 1 + ... + n - 1 + x + y \= n \* (n - 1) // 2 + x + y

另一个方程可以选择平方和

t \= 0^2 + 1^2 + ... + (n - 1)^2 + x^2 + y^2 \= (n - 1) \* n \* (n \* 2 - 1) // 6 + x^2 + y^2

也就是

x + y \= s - n \* (n + 1) // 2

x^2 + y^2 \= t - (n - 1) \* n \* (n \* 2 - 1) // 6

接下来只需暴力枚举x，然后检测是否存在可行的y即可。

最后附上python代码：

```python
class Solution(object):
    def getSneakyNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        s, t = 0, 0
        for v in nums:
            s += v
            t += v * v
        
        n = len(nums) - 2
        s -= n * (n - 1) // 2
        t -= (n - 1) * n * (n * 2 - 1) // 6
        for x in range(n):
            y = s - x
            if x * x + y * y == t:
                return [x, y]
        
        return []
```
