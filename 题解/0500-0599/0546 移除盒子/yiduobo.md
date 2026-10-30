---
title: "546. 移除盒子"
aliases: ["yiduobo的每日leetcode 546.移除盒子"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261218803"
zhihu_id: "261218803"
zhihu_title: "yiduobo的每日leetcode 546.移除盒子"
question_id: "546"
question: "移除盒子"
problem_url: "https://leetcode.cn/problems/remove-boxes/"
created: "2020-10-09T21:13:41+08:00"
updated: "2020-10-09T21:13:41+08:00"
upvotes: 0
comments: 0
---

# 546. 移除盒子

> **[yiduobo的每日leetcode 546.移除盒子](https://zhuanlan.zhihu.com/p/261218803) · 知乎 · 2020-10-09 · 赞同 0**
> 力扣：[546. 移除盒子](https://leetcode.cn/problems/remove-boxes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

546.移除盒子<https://leetcode-cn.com/problems/remove-boxes/>

很有意思的动态规划问题。

首先观察两个case：

1112221222111

11122211222111

对于1112221222111而言：

方法一：

111222（1）222111，此时得到1

111（222222）111，此时得到36

111111，此时得到36

最终答案为73

方法二：

111（222）1222111，此时得到9

1111（222）111，此时的得到9

1111111，此时得到49

最终答案为67

对于11122211222111而言：

方法一：

111222（11）222111，此时得到4

111（222222）111，此时得到36

111111，此时得到36

最终答案为76

方法二：

111（222）11222111，此时得到9

11111（222）111，此时得到9

11111111，此时得到64

最终答案为82

通过观察上面两个case，可以发现一个问题就是，对于内部区间的消除，并不存在某种普适的规则，具体来说就是对于最中间的1，我们在一开始是无法得知其是否应该消除的。因此f[l][r]这种形式的状态是不行的，因为无法找到合理的状态转移方程。

再仔细看一下这两个case，实际上我们需要做的就是，对于每一段连续的值，需要考虑后面相同值是选择合并还是舍去。于是可以使用状态f[l][r][k]表示现在处理l到r这一段，且前面已经积累了k个连续的boxes[l]，最终可以获得的最大值是多少。

那么对于f[l][r][k]：

1、首先我们可以直接把这累积的k + 1个boxes[l]直接合并掉，那么就有

f[l][r][k] \= f[next_l][r][next_k] + (k + 1)^2，

其中next_k为从l + 1开始的连续出现的boxes[l + 1]的个数减一，而next_l则是连续出现我的boxes[l + 1]中最后一个的位置。

2、对于l到r这一段，我们找出之后每一个boxes[l]出现的位置next_same_pos，然后先将中间的部分合并掉，这一段合并的最大价值为f[next_l][next_same_pos - 1][next_k]，而此时前面累积的k个boxes[l + 1]融合next_same_pos开始的boxes[l + 1]，就可以得到新的new_k，那么此时就有

f[l][r][k] \= f[next_l][next_same_pos - 1][next_k] + f[next_same_pos][r][new_k]。

例如对于1112221222111这个case的起始状态[11][12221222111]，即f[2][12][2]：

1、可以直接使用掉前3个1，得到[111] + [22][21222111]，即9 + f[5][12][2]

2、也可以融合最中间1，即优先求解中间的[22]2，然后求解[111][1222111]，即f[5][5][2] + f[6][12][3]

3、也可以融合后面的1，即优先求解中间的[22]21222，然后求解[11111][1]，即f[5][9][3] + f[12][12][5]

可以发现，这样做就可以将所有可能的融合情况都考虑进来了。

这里有一个隐藏条件就是对于连续的若干个相同box，应该一次处理掉而不应该拆开，这也是上面为什么要维护连续数字的原因。

三维的状态，每次转移都需要一趟扫描，因此最终的时间复杂度为O(n^4)，空间复杂度为O(n^3)。

最后附上python代码：

```python
class Solution(object):
    def removeBoxes(self, boxes):
        """
        :type boxes: List[int]
        :rtype: int
        """

        n = len(boxes)
        
        f = [[[0] * n for _ in range(n)] for _ in range(n)]
        now = boxes[0]
        k = 0
        for index in range(1, len(boxes)):
            if boxes[index] != now:
                break
            k += 1
        
        if k == len(boxes) - 1:
            return len(boxes) ** 2

        return self.dfs(k, len(boxes) - 1, k, boxes, f)
    
    def dfs(self, l, r, k, boxes, f):
        if f[l][r][k] > 0:
            return f[l][r][k]
        if l == r:
            return (k + 1) ** 2
        
        next_k = 0
        for index in range(l + 2, r + 1):
            if boxes[index] != boxes[l + 1]:
                break
            next_k += 1
        
        if r - next_k - 1 == l:
            f[l][r][k] = (k + 1) ** 2 + (next_k + 1) ** 2
            return f[l][r][k]

        next_l = index - 1
        f[l][r][k] = (k + 1) ** 2 + self.dfs(next_l, r, next_k, boxes, f)

        next_same_pos = next_l + 1
        while True:
            while next_same_pos <= r and boxes[next_same_pos] != boxes[l]:
                next_same_pos += 1
            if next_same_pos > r:
                return f[l][r][k]
            
            part_ret = self.dfs(next_l, next_same_pos - 1, next_k, boxes, f)
            new_k = k + 1
            for index in range(next_same_pos + 1, r + 1):
                if boxes[index] != boxes[l]:
                    break
                next_same_pos = index
                new_k += 1
            
            if next_same_pos == r:
                f[l][r][k] = max(f[l][r][k], part_ret + (new_k + 1) ** 2)
                return f[l][r][k]
            
            f[l][r][k] = max(f[l][r][k], part_ret + self.dfs(next_same_pos, r, new_k, boxes, f))
            next_same_pos += 1

        return f[l][r][k]
```
