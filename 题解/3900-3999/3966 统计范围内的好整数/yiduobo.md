---
title: "3966. 统计范围内的好整数"
aliases: ["yiduobo的每日leetcode 3966.统计范围内的好整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052143076576081855"
zhihu_id: "2052143076576081855"
zhihu_title: "yiduobo的每日leetcode 3966.统计范围内的好整数"
question_id: "3966"
question: "统计范围内的好整数"
problem_url: "https://leetcode.cn/problems/count-good-integers-in-a-range/"
difficulty: "Hard"
rating: 2006
created: "2026-06-23T22:46:40+08:00"
updated: "2026-06-23T22:46:43+08:00"
upvotes: 2
comments: 0
---

# 3966. 统计范围内的好整数

> **[yiduobo的每日leetcode 3966.统计范围内的好整数](https://zhuanlan.zhihu.com/p/2052143076576081855) · 知乎 · 2026-06-23 · 赞同 2**
> 力扣：[3966. 统计范围内的好整数](https://leetcode.cn/problems/count-good-integers-in-a-range/) · Hard · 灵茶山艾府：[【模板】上下界数位 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3966.统计范围内的好整数

<https://leetcode.cn/problems/count-good-integers-in-a-range/>

题目给出三个整数l、r以及k，其中l和r在10到10^15之间，k在0到9之间。

若一个数字中每一对相邻数位之间的绝对差都至多为k，那么就称该数字为好数。

要求计算l到r之间好数的数量。

题目的数据规模较大，同时好数的限制又体现在相邻数位的绝对差之间，因此在这里使用数位动态规划是很自然的想法。

首先，将l和r转化为数位数组，若l的长度比r短，在这里需要在l的高位补充前导0，让l和r的长度相同。

接下来，令f[level][last][state]表示已经填充了最高的level位，最后一位为last，且与上下界以及前导0的关系为state时可能得到的好数数目。其中state是一个三位的二进制数，最高位表示当前是否处于前导0的状态，中间位表示当前填充的数是否与r的前level位相同，最低位表示当前填充的数是否与l的前level位相同。

那么对于f[level][last][state]：

1、首先初始化下一位可填充数字的上下界start和end分别为0和9

2、分离state的三位，分别记录为prefix_zero、high_bound和low_bound：

若prefix_zero为true，那么目前还在前导0的状态，无需考虑当前这一位与last的绝对差，因此无需修改start和end，否则下一位填充的上下界start和end需要修改为max(start, last - k)以及min(end, last + k)。

若high_bound为true，那么下一位填充的元素不能大于r[level]，因此需要调整上界end为min(end, r[level])。

若low_bound为true，那么下一位填充的元素不能小于l[level]，因此需要调整下界start为max(start, l[level])。

3、在确定了start和end后，从start到end进行遍历，对于当前遍历到的d：

初始化nxt_state为0，然后根据d来进行调整。

若prefix_zero为true，且d为0，说明还在前导0的状态中，此时应该将nxt_state的最高位置为1，即将nxt_state |\= 4。

若high_bound为true，且d与r[level]相同，说明填充的元素与r的前level + 1位相同，此时应该将nxt_state的中间位置为1，即将nxt_state |\= 2。

若low_bound为true，且d如l[level]相同，说明填充的元素与l的前level + 1位相同，此时应该将nxt_state的最低位置为1，即将nxt_state |\= 1。

确定好nxt_state后，递归计算f[level + 1][d][nxt_state]，然后将其累加到f[level][last][state]中即可。

最后附上python代码：

```python
class Solution(object):
    def goodIntegers(self, l, r, k):
        """
        :type l: int
        :type r: int
        :type k: int
        :rtype: int
        """
        
        r = [int(x) for x in str(r)]
        l = [int(x) for x in str(l)]
        l = [0] * (len(r) - len(l)) + l
        n = len(l)

        f = [[[None] * 8 for _ in range(10)] for _ in range(n)]

        def calc(level, last, state, f):
            if level == n:
                return 1
            
            if f[level][last][state] is None:
                f[level][last][state] = 0
                start = 0
                end = 9

                if state & 4:
                    prefix_zero = True
                else:
                    prefix_zero = False
                    start = max(start, last - k)
                    end = min(end, last + k)

                if state & 2:
                    high_bound = True
                    end = min(end, r[level])
                else:
                    high_bound = False

                if state & 1:
                    low_bound = True
                    start = max(start, l[level])
                else:
                    low_bound = False

                for d in range(start, end + 1):
                    nxt_state = 0
                    if prefix_zero and d == 0:
                        nxt_state |= 4
                    if high_bound and d == r[level]:
                        nxt_state |= 2
                    if low_bound and d == l[level]:
                        nxt_state |= 1
                    
                    f[level][last][state] += calc(level + 1, d, nxt_state, f)
            
            return f[level][last][state]
        
        return calc(0, 0, 7, f)
```
