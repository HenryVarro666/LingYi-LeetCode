---
title: "3906. 统计网格路径中好整数的数目"
aliases: ["yiduobo的每日leetcode 3906.统计网格路径中好整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/十-数位-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2030073264928707613"
zhihu_id: "2030073264928707613"
zhihu_title: "yiduobo的每日leetcode 3906.统计网格路径中好整数的数目"
question_id: "3906"
question: "统计网格路径中好整数的数目"
problem_url: "https://leetcode.cn/problems/count-good-integers-on-a-grid-path/"
difficulty: "Hard"
rating: 2160
created: "2026-04-22T01:59:35+08:00"
updated: "2026-04-22T01:59:53+08:00"
upvotes: 1
comments: 0
---

# 3906. 统计网格路径中好整数的数目

> **[yiduobo的每日leetcode 3906.统计网格路径中好整数的数目](https://zhuanlan.zhihu.com/p/2030073264928707613) · 知乎 · 2026-04-22 · 赞同 1**
> 力扣：[3906. 统计网格路径中好整数的数目](https://leetcode.cn/problems/count-good-integers-on-a-grid-path/) · Hard · 灵茶山艾府：[两种方法：上下界数位 DP / 组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3906.统计网格路径中好整数的数目

<https://leetcode.cn/problems/count-good-integers-on-a-grid-path/description/>

题目给出两个整数l和r，满足1 \<\= l \<\= r \<\= 9 \* 10^15。

另外给出一个由恰好三个'D'和三个'R'组成的字符串directions。

对于在范围[l, r]之内的每个整数x，执行以下步骤：

1、若x的位数不足16位，则在其左侧补充前导零，使其成为16位的字符串

2、将这个16位数，按从上到下从左到右的顺序，填充到一个4 \* 4的网格当中

3、从左上角单元格，也就是(0, 0)出发，按照顺序应用directions中的6个字符：

- 碰到'D'时，让行数加1
- 碰到'R'时，让列数加1

记录按照这个路径访问的数字序列，包括(0, 0)，得到一个长度为7的序列。若这个序列是非递减的，那么就认为x是一个好整数。

问[l, r]这个区间中有多少个好整数。

题目中的数据规模较大，直接枚举显然是不行的。对于这类给定上下界寻找合法元素数量的问题，通常的想法是往数位动态规划去做。对于本题，除了常规的上下界限定之外，还存在一个非递减数字序列的限制需要想办法处理。

不妨先来看看这个数字序列是怎么生成的。可以发现，由于directions在一开始就给定了，那么从左上角(0, 0)出发，走过的单元格也随之固定了下来，换言之，出现在数字序列中的数位下标也固定了下来。在这里不妨初始化一个长度为16的布尔数组checkpoints，其中checkpoints[p]为true，表示p这个数位上的数属于数字序列，反之则表示不属于。那么对于数位动态规划而言，对于当前数位level，其填充的元素在满足了上下界的前提下，若checkpoints[level]为true，那么这一位上填充的元素还需要大于等于上一个checkpoints为true的位置填充的元素，也就是说上一次填充的元素值需要保留在状态中。这样一来，就得到了动态规划的状态表示：

令f[level][pre][state]表示，填充了前level位，上一个checkpoints为true的数位上填充的值为pre，且填充的前缀是否紧挨着l和r的前缀的状态为state时，合法的填充方案数。其中state是一个两位的二进制，其中低位表示已填充的前缀是否挨着l，高位则表示是否挨着r，那么对于f[level][pre][state]：

1、先通过state确定本轮填充元素的上下界start和end。具体来说，若state低位为1，那么下界start就是l[level]，否则就是0；同样的，若state高位为1，那么上界end就是r[level]，否则就是9

2、接下来，若checkpoints[level]为true，那么就需要调整start为pre，保证数字序列的单调不减

3、最后，从start到end枚举level这一位填充的数字d，先计算出新状态的nxt_pre和nxt_state，然后递归求解f[level + 1][nxt_pre][nxt_state]，并累加到f[level][pre][state]中。

其中，若checkpoints[level]为true，那么nxt_pre就是当前的d，否则就还是之前的pre。

而对于nxt_state，若state的低位为1且d等于l[level]，那么nxt_state的低位就为1，否则为0；同样的，若state的高位为1且d等于r[level]，那么nxt_state的高位就为1。

递归计算的入口为f[0][0][3]，其中第一个level的0很好理解，第二个0是因为目前还未填充数字序列中的任意元素，而数字序列中的首个元素实际上是不受限制的，因此设置为0就能保证数字序列中的第一个元素不会受到状态中pre的限制。最后的3，则表示初始填充状态下不能越过l和r的最高位，所以上下界都需要限制住。

最后附上python代码：

```python
class Solution(object):
    def countGoodIntegersOnPath(self, l, r, directions):
        """
        :type l: int
        :type r: int
        :type directions: str
        :rtype: int
        """
        
        checkpoints = [False] * 16
        checkpoints[0] = True
        p = 0
        for c in directions:
            if c == 'D':
                p += 4
            else:
                p += 1
            checkpoints[p] = True
        
        f = [[[None] * 4 for _ in range(10)] for _ in range(16)]
        l = [int(d) for d in list(str(l))]
        r = [int(d) for d in list(str(r))]
        l = [0] * (16 - len(l)) + l
        r = [0] * (16 - len(r)) + r

        def calc(level, pre, state):
            if level == 16:
                return 1

            if f[level][pre][state] is None:
                f[level][pre][state] = 0
                start, end = 0, 9
                if state & 1:
                    start = max(start, l[level])
                if checkpoints[level]:
                    start = max(start, pre)
                
                if state & 2:
                    end = min(end, r[level])
                
                for d in range(start, end + 1):
                    if checkpoints[level]:
                        nxt_pre = d
                    else:
                        nxt_pre = pre
                    
                    nxt_state = 0
                    if (state & 1) and d == l[level]:
                        nxt_state |= 1
                    if (state & 2) and d == r[level]:
                        nxt_state |= 2
                    
                    f[level][pre][state] += calc(level + 1, nxt_pre, nxt_state)
            
            return f[level][pre][state]
    
        return calc(0, 0, 3)
```
