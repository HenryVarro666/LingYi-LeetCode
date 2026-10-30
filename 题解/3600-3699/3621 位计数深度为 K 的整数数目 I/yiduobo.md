---
title: "3621. 位计数深度为K的整数数目I"
aliases: ["yiduobo的每日leetcode 3621.位计数深度为K的整数数目I"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1944526177298552054"
zhihu_id: "1944526177298552054"
zhihu_title: "yiduobo的每日leetcode 3621.位计数深度为K的整数数目I"
question_id: "3621"
question: "位计数深度为 K 的整数数目 I"
problem_url: "https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-i/"
difficulty: "Hard"
rating: 3352
created: "2025-08-28T22:44:32+08:00"
updated: "2025-08-28T22:44:32+08:00"
upvotes: 0
comments: 0
---

# 3621. 位计数深度为K的整数数目I

> **[yiduobo的每日leetcode 3621.位计数深度为K的整数数目I](https://zhuanlan.zhihu.com/p/1944526177298552054) · 知乎 · 2025-08-28 · 赞同 0**
> 力扣：[3621. 位计数深度为 K 的整数数目 I](https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-i/) · Hard · 灵茶山艾府：[数位 DP，做法同 3352 题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3621.位计数深度为K的整数数目I

<https://leetcode.cn/problems/number-of-integers-with-popcount-depth-equal-to-k-i/description/>

对于任意正整数x，题目定义以下序列：

p[0] \= x

p[index + 1] \= popcount(p[index])，这里的popcount(y)表示的是y的二进制表示中1的数目。

这个序列最终会到达值1，而x的位计数深度则定义为使得p[index] \= 1的最小整数index。

例如对于x \= 7(二进制表示为111)，得到的序列为7(111) -> 3(11) -> 2(10) -> 1，因此7的位计数深度为3。

现在给出两个整数n和k，要求找出1到n之间位计数深度恰好为k的整数数目。其中n可达10^15，k在0到5之间。

题目中的n规模非常大，很明显不能直接暴力计算，不过10^15刚好小于2^50，也就是说在对于1到n之间的任意整数x，在一次操作后，其对应的p[1] \= popcount(x) \<\= 50。

基于这一点，就可以先预处理出1到50的位计数深度，不妨记为f，那么对于其中所有满足f[x] \= k - 1的x，在1到n之间，且二进制表示中恰好有f[x]个1的元素，在经过一次操作后就会变成f[x]，然后经过剩下的k - 1次操作后将变为1，也就是说这些元素的位计数深度恰好为k。

到了这里，问题就转化成了对于所有等于k - 1的f[x]，求1到n之间，二进制表示中恰好有f[x]个1的元素的数目。对于这个问题，则可以使用数位动态规划。令g[level][cnt][state]表示填充了这个元素二进制表示的最高的level位，其中包含cnt个1，且填充的位与n的二进制表示的最高level位的异同关系为state时的填充方案数，那么对于g[level][cnt][state]：

1、若level等于n的长度，那么此时应该检测cnt是否刚好等于f[x]，若等于，则说明当前的填充方案有效，对应的g[level][cnt][state]为1，否则为0

2、若level \< n，则需要尝试给level这一位填充0或者1。

0是一定可以填充的，而填充1的前提条件是state为0，或者state为1且f[x]的level这一位为1。

对于填充的数值d，首先由nxt_cnt \= cnt + d，另一方面，若state为1，且d与f[x]的level这一位相等，那么nxt_state就等于1，否则等于0。接下来，只需递归计算f[level + 1][nxt_cnt][nxt_state]，然后将其累加到f[level][cnt][state]中即可。

对于每种符合条件的f[x]，计算其对应的g数组，然后将g[0][0][1]累加到最终答案中即可。需要特别注意的是，当k \= 0时，不存在合法的f[x]，但是x \= 1是符合条件的，应该直接返回1；而当k \= 1时，若x \= 1，其f[x]也等于0，但是此时并没有x转化为f[x]，也就是1转换到1这一步，因此需要排除掉x \= 1这种情况。

最后附上python代码：

```python
class Solution(object):
    def popcountDepth(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        
        if k == 0:
            return 1

        f = [None] * 51
        f[1] = 0
        for v in range(2, 51):
            x = v
            step = 0
            while f[x] is None:
                cnt = 0
                while x:
                    if x % 2 == 1:
                        cnt += 1
                    x //= 2
                x = cnt
                step += 1
            f[v] = step + f[x]
        
        bound = []
        while n:
            bound.append(n % 2)
            n //= 2
        bound.reverse()
        
        def calc(level, cnt, state, g):
            if level == len(bound):
                if cnt == x:
                    return 1
                else:
                    return 0
            
            if g[level][cnt][state] is None:
                g[level][cnt][state] = 0
                start = 0
                end = 1
                if state == 1 and bound[level] == 0:
                    end = 0

                for d in range(start, end + 1):
                    nxt_cnt = cnt + d
                    if state == 1 and d == bound[level]:
                        nxt_state = 1
                    else:
                        nxt_state = 0
                    
                    if nxt_cnt <= x:
                        g[level][cnt][state] += calc(level + 1, nxt_cnt, nxt_state, g)
            
            return g[level][cnt][state]

        res = 0
        for x in range(1, 51):
            if f[x] == k - 1:
                g = [[[None] * 2 for _ in range(x + 1)] for _ in range(len(bound))]
                res += calc(0, 0, 1, g)
                if x == 1:
                    res -= 1
        
        return res
```
