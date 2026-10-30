---
title: "3178. 找出K秒后拿着球的孩子"
aliases: ["yiduobo的每日leetcode 3178.找出K秒后拿着球的孩子"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/705846893"
zhihu_id: "705846893"
zhihu_title: "yiduobo的每日leetcode 3178.找出K秒后拿着球的孩子"
question_id: "3178"
question: "找出 K 秒后拿着球的孩子"
problem_url: "https://leetcode.cn/problems/find-the-child-who-has-the-ball-after-k-seconds/"
difficulty: "Easy"
created: "2024-06-27T22:47:49+08:00"
updated: "2024-06-27T22:47:49+08:00"
upvotes: 0
comments: 0
---

# 3178. 找出K秒后拿着球的孩子

> **[yiduobo的每日leetcode 3178.找出K秒后拿着球的孩子](https://zhuanlan.zhihu.com/p/705846893) · 知乎 · 2024-06-27 · 赞同 0**
> 力扣：[3178. 找出 K 秒后拿着球的孩子](https://leetcode.cn/problems/find-the-child-who-has-the-ball-after-k-seconds/) · Easy · 灵茶山艾府：[O(1) 公式（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3178.找出K秒后拿着球的孩子

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-child-who-has-the-ball-after-k-seconds/)

题目给出两个正整数n和k，有编号为0到n - 1的n个孩子站成一排。最开始，0号孩子拿着一个球并开始向右侧传球，每经过一秒都会进行一次传球。当球到达n - 1号孩子手上后，传球的方向将改为向左侧传球，而当球再次回到0号孩子手上后，传球的方向又将改成向右侧传球，如此循环往复。问k秒后球会在哪个孩子手上。

可以发现，每经过n - 1秒，球会到达n - 1号孩子手上，此时开始反向传球，而再经过n - 1秒，球将回到0号孩子手上，此时相当于回到了原始状态，也就是说每经过(n - 1) \* 2秒都会完成一次传球的循环，因此可以先将k对(n - 1) \* 2取模，对于剩下的k，若其小于等于n - 1，说明还在向右侧传球的过程中，此时球就在编号为k的孩子手上；若其大于n - 1，则说明现在已经处在向左侧传球的过程中，此时球向左侧传递了k - (n - 1)次，因此球就应该在编号为(n - 1) - (k - (n - 1)) \= (n - 1) \* 2 - k的孩子手上。

最后附上python代码：

```python
class Solution(object):
    def numberOfChild(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        k %= (n - 1) * 2
        if k <= n - 1:
            return k
        else:
            return (n - 1) * 2 - k
```
