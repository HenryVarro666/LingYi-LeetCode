---
title: "375. 猜数字大小II"
aliases: ["yiduobo的每日leetcode 375.猜数字大小II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/165643911"
zhihu_id: "165643911"
zhihu_title: "yiduobo的每日leetcode 375.猜数字大小II"
question_id: "375"
question: "猜数字大小II"
problem_url: "https://leetcode.cn/problems/guess-number-higher-or-lower-ii/"
created: "2020-07-31T22:28:24+08:00"
updated: "2020-07-31T22:28:24+08:00"
upvotes: 0
comments: 0
---

# 375. 猜数字大小II

> **[yiduobo的每日leetcode 375.猜数字大小II](https://zhuanlan.zhihu.com/p/165643911) · 知乎 · 2020-07-31 · 赞同 0**
> 力扣：[375. 猜数字大小II](https://leetcode.cn/problems/guess-number-higher-or-lower-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

375.猜数字大小II <https://leetcode-cn.com/problems/guess-number-higher-or-lower-ii/>

上一题的升级版，不过不能直接使用二分法来做了。虽然二分法可以保证猜中所需的次数最少，但是这里每次猜测代价不同，次数最少并不意味着代价最低。

我在这里使用的是记忆化搜索的方法，设f[l][r]表示最坏情况下，从l到r中猜到正确答案最少需要的代价，那么：

1、当l > r时，无意义

2、当l \= r时，那么此时答案不需要猜，于是f[l][r] \= 0

3、当l \= r - 1时，此时显然应该猜l，于是f[l][r] \= l

4、其他情况下，从l + 1到r - 1枚举cut_pos，表示猜测cut_pos，那么在最坏情况下，答案应该位于f[l][cut_pos - 1]和f[cut_pos + 1][r]中较大的那一边，于是有

f[l][r] \= min(max(f[l][cut_pos - 1] + f[cut_pos + 1][r]) + cut_pos)

需要注意的是，题目中是猜测1到n中的数，在实现的时候如果数组从0开始的话记得每次猜测有1的offset。

最后附上python代码：

```python
class Solution(object):
    def getMoneyAmount(self, n):
        """
        :type n: int
        :rtype: int
        """

        f = [[None] * (n) for _ in range(n)]

        return self.dfs(0, n - 1, f)

    def dfs(self, l, r, f):
        if f[l][r] is None:
            if l >= r:
                f[l][r] = 0
            elif l == r - 1:
                f[l][r] = l + 1
            else:
                f[l][r] = l + 2 + self.dfs(l + 2, r, f)
                for cut_pos in range(l + 1, r):
                    f[l][r] = min(f[l][r], cut_pos + 1 + max(self.dfs(l, cut_pos - 1, f), self.dfs(cut_pos + 1, r, f)))

        return f[l][r]
```
