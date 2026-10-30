---
title: "3869. 统计区间内奇妙数的数目"
aliases: ["yiduobo的每日leetcode 3869.统计区间内奇妙数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2018760740438286518"
zhihu_id: "2018760740438286518"
zhihu_title: "yiduobo的每日leetcode 3869.统计区间内奇妙数的数目"
question_id: "3869"
question: "统计区间内奇妙数的数目"
problem_url: "https://leetcode.cn/problems/count-fancy-numbers-in-a-range/"
difficulty: "Hard"
rating: 2255
created: "2026-03-21T19:19:53+08:00"
updated: "2026-03-21T19:20:01+08:00"
upvotes: 0
comments: 0
---

# 3869. 统计区间内奇妙数的数目

> **[yiduobo的每日leetcode 3869.统计区间内奇妙数的数目](https://zhuanlan.zhihu.com/p/2018760740438286518) · 知乎 · 2026-03-21 · 赞同 0**
> 力扣：[3869. 统计区间内奇妙数的数目](https://leetcode.cn/problems/count-fancy-numbers-in-a-range/) · Hard · 灵茶山艾府：[状态机数位 DP + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3869.统计区间内奇妙数的数量

<https://leetcode.cn/problems/count-fancy-numbers-in-a-range/>

题目给出两个整数l和r，满足1 \<\= l \<\= r \<\= 10^15。

若某个整数的数位形成一个严格单调的序列，即数位是严格递增或者严格递减的，那么就称这个整数为好数。所有的一位数都被认为是好数。

若一个整数是好数，或者它的数位和是好数，那么就称这个数为奇妙数。

问区间[l, r]内奇妙数的数量。

根据题目中对于奇妙数的定义，奇妙数要么满足数位单调，要么满足数位之和单调。由于题目中r不超过10^15，那么就意味着区间内任意元素的数位之和都不超过9 \* 15 \= 135，于是可以先对1到135之间的所有元素进行预处理，找出其中的好数。对于一个1到135之间的数v，若其为好数，那么令g[v]为true，否则为false。

预处理的具体过程如下：

首先，所有的一位数都是好数。

接下来，对于所有的两位数，只要其个位上的数与十位上的数不同，那么其数位就必然是单调递增或者单调递减的，也就是说除了11、22、33、...这些数之外，其他的两位数都是好数。

最后，对于三位数，由于上限是135，因此限定了百位上为1，于是只需确保十位上为2或者3，且个位上的数大于十位上的数，这个数就是好数。

---

预处理完成后，接下来就可以利用数位动态规划来进行求解了。在计算开始之前，可以先将l和r转化为数位数组，并为l补充足够的前缀0，使得l的长度和r相同。

接下来，令f[level][s][last][state]表示最高的level位上填充元素之和为s，最后填充的一位为last，且已经填充元素的准固态为state时的奇妙数数量。这里的state为5为的二进制数，其含义分别为：

- 最高位表示目前填充的元素是否紧贴着上界r的前缀
- 次高位表示目前填充的元素是否紧贴着下界l的前缀
- 第三位表示目前填充的元素是否依然处于前导0的状态
- 第四位表示目前填充的元素是否为单调递减的状态
- 最低位表示目前填充的元素是否为单调递增的状态

需要注意的是，处于前导0的状态是单调递增和单调递减的状态是无意义的，而当从前导0状态变为非前导0状态时，此时即可以认为是单调递增的状态，也可以认为是单调递减的状态。

那么对于f[level][s][last][state]：

1、若level等于n，说明填充完成了。此时有两种情况为奇妙数，分别为

- 数位之和为好数，也就是g[s]为true
- 填充的元素单调递增或者单调递减，也就是最低的两位中至少有一个1，即state & 3非0

2、若level \< n，则需要考虑当前这一位应该填充什么。

首先需要先分离state，分别记

- 最高位为high_bound
- 次高位为low_bound
- 第三位为prefix_zero
- 最低的两位为st

先通过high_bound和low_bound限定填充元素的上下界，保证填充元素不会越过l或r。具体来说，若high_bound为1，那么填充的上界end就是r[level]，否则就是9；若low_bound为1，那么填充的下界start就是l[level]，否则就是0。

接下来，从start到end遍历，尝试将其中的元素填充到当前位。对于遍历到的元素d，需要根据d来初始化nxt_state：

1）若当前处于前导0的状态，即prefix_zero为1，且d为0，那么接下来依然会处于前导0的状态，此时应该令nxt_state为4，也就是第三位上为1

2）若当前处于前导0的状态，且d非0，那么接下来将从前导0状态变为非前导0状态，此时应该令nxt_state为3，也就是最低的两位上都为1，表示接下来同时处于单调递增和单调递减的状态

3）若当前处于非前导0的状态，且st的低位为1，也就是目前处于单调递增的状态，同时last \< d，那么接下来依然会处于单调递增的状态，此时就应该令nxt_state为1，也就是最低位上为1

4）若当前处于非前导0的状态，且st的高位为1，也就是目前处于单调递减的状态，同时last > d，那么接下来依然会处于单调递减的状态，此时就应该令nxt_state为2，也就是次低位上为1

5）若当前处于非前导0的状态，且不满足上面的3)和4)，那么接下来即不会单调递减，也不会单调递增，此时就应该令nxt_state为0

得到初始的nxt_state后，还需要根据d的大小确定与上下界的关系，具体来说：

- 若d与l[level]相同，且low_bound为1，那么就需要将nxt_state的次高位置为1，也就是将8按位或到nxt_state上
- 若d与r[level]相同，且high_bound为1，那么就需要将nxt_state的最高位置为1，也就是将16按位或到nxt_state上

得到最终的nxt_state后，递归计算f[level + 1][s + d][d][nxt_state]，然后将其累加到f[level][s][d][state]即可。

初始的计算入口为f[0][0][0][28]，其中前3个0都好理解，最后的28即二进制的11100，表示上下界受限，同时处于前导0的状态。

最后附上python代码：

```python
class Solution(object):
    def countFancy(self, l, r):
        """
        :type l: int
        :type r: int
        :rtype: int
        """
        
        r = [int(x) for x in str(r)]
        l = [int(x) for x in str(l)]
        n = len(r)
        l = [0] * (n - len(l)) + l
        
        ma = 9 * n
        g = [True] * (ma + 1)
        for v in range(10, min(99, ma) + 1):
            if v % 10 == v // 10:
                g[v] = False
        for v in range(100, ma + 1):
            if v // 10 % 10 < 2 or v % 10 <= v // 10 % 10:
                g[v] = False
        
        f = [[[[None] * 32 for _ in range(10)] for _ in range(ma + 1)] for _ in range(n)]
        def calc(level, s, last, state, f):
            if level == n:
                if (state & 3) > 0 or g[s]:
                    return 1
                return 0
            
            if f[level][s][last][state] is None:
                f[level][s][last][state] = 0
                st = state & 3
                prefix_zero = state & 4
                low_bound = state & 8
                high_bound = state & 16

                start, end = 0, 9
                if low_bound:
                    start = l[level]
                if high_bound:
                    end = r[level]
                
                for d in range(start, end + 1):
                    if prefix_zero == 4:
                        if d == 0:
                            nxt_state = 4
                        else:
                            nxt_state = 3
                    else:
                        if (st & 1) == 1 and last + 1 <= d:
                            nxt_state = 1
                        elif (st & 2) == 2 and last - 1 >= d:
                            nxt_state = 2
                        else:
                            nxt_state = 0
                    
                    if low_bound and d == l[level]:
                        nxt_state |= 8
                    if high_bound and d == r[level]:
                        nxt_state |= 16
                    
                    f[level][s][last][state] += calc(level + 1, s + d, d, nxt_state, f)
            
            return f[level][s][last][state]
        
        return calc(0, 0, 0, 28, f)
```
