---
title: "1521. 找到最接近目标值的函数值"
aliases: ["yiduobo的每日leetcode 1521.找到最接近目标值的函数值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/bit-manipulation", "leetcode/sliding-window", "题单/位运算", "题单/位运算/三-与或-AND/OR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422017694"
zhihu_id: "422017694"
zhihu_title: "yiduobo的每日leetcode 1521.找到最接近目标值的函数值"
question_id: "1521"
question: "找到最接近目标值的函数值"
problem_url: "https://leetcode.cn/problems/find-a-value-of-a-mysterious-function-closest-to-target/"
difficulty: "Hard"
rating: 3171
created: "2021-10-15T23:26:51+08:00"
updated: "2021-10-15T23:26:51+08:00"
upvotes: 0
comments: 0
---

# 1521. 找到最接近目标值的函数值

> **[yiduobo的每日leetcode 1521.找到最接近目标值的函数值](https://zhuanlan.zhihu.com/p/422017694) · 知乎 · 2021-10-15 · 赞同 0**
> 力扣：[1521. 找到最接近目标值的函数值](https://leetcode.cn/problems/find-a-value-of-a-mysterious-function-closest-to-target/) · Hard · 灵茶山艾府：[两种方法：LogTrick/滑动窗口+栈（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1521.找到最接近目标值的函数值

[力扣](https://leetcode-cn.com/problems/find-a-value-of-a-mysterious-function-closest-to-target/)

首先观察func的构成。这个函数的作用是将arr中l到r这一段的所有数进行按位与，那么对于这个按位与操作而言，当固定了左边界l时，若右边界r越大，那么按位与的结果就越小。反过来也一样，当固定了右边界r之后，左边界l越小，按位与的结果就越大。

根据上面这条与单调性相关的结论，很自然想到使用滑动窗口来处理这个问题。

对于当前窗口[l, r]而言，若执行func得到的结果小于target，那么此时应该将l向后移动。反过来若这个结果大于target，则应该将r向后移动。重复这个过程，每次移动时都更新答案，直到r移出数组末尾。

接下来的问题就是如何高效求得区间[l, r]执行func后的结果。本题与一般的滑动窗口问题有所不同的地方是，当右边界向后移动时，可以通过按位与操作很快更新得到窗口内的值，但左边界向后移动时，就没有办法直接通过按位与来进行更新了。此时有两种思路：

1、直接计算l到r这个区间的值

当然这里的直接计算不是一趟循环计算，这样的复杂度就太高了。对于动态的情况，一般的做法是线段树，而这里由于是静态的，则可以使用st算法来解决。

令f[i][j]表示区间[i, i + 2^j - 1]中每个数按位与的值，那么对于f[i][j]：

1-1）当j \= 0时，显然有f[i][j] \= arr[i]

1-2）当j > 0时，若i + 2^j - 1 >\= n，说明区间越界了，无意义。若i + 2^j - 1 \< n，那么可以将这个区间拆开成为[i, i + 2^(j - 1) - 1]以及[i + 2^(j - 1), i + 2^j - 1]这两个区间。根据与运算的性质，可以得到

func(i, i + 2^j - 1) \= func(i, i + 2^(j - 1) - 1) & func(i + 2^(j - 1), i + 2^j - 1)

转换到f上，就是f[i][j] \= f[i][j - 1] & f[i + 2^(j - 1)][j - 1]

这样一来，就可以在O(nlogn)的时间复杂度内求解出所有的f。

而对于区间[l, r]，可以先找到最大的j，满足2^j \<\= r - l + 1，那么就可以将区间[l, r]拆分成[l, l + 2^j - 1]以及[l + 2^j - 1, r]，前面这个区间按位与的值就是f[l][j]，而对于后面这个区间，则可以重复这个过程直到j等于0为止。这个过程的复杂度是O(logn)的，也就是说在O(logn)的时间复杂度内就可以求出func(l, r)，因此整个算法的时间复杂度就是O(nlogn)。

2、统计l到r这个区间内，每个二进制位中1出现的次数

这种想法的前提是arr中的数都小于2^20 \= 1048576，因此其二进制位中至多只有20个1，于是可以对于每一位都储存其在当前区间内1的数目，记为cnt。

对于cnt而言，其中cnt[p]表示区间arr[l]到arr[r]这些数中p这一位为1的数的数目，若这个cnt[p]等于区间长度r - l + 1，那么说明arr[l]到arr[r]这些数的p这一位都是1，因此按位与结果中的这一位就为1，否则就为0。

当区间边界发生变化时，若l向后移动，那么先将arr[l]按二进制位分离，然后对于其中为1的所有位数，将cnt中对应的位置减去1。类似的，当r向后移动时，则是将arr[r]按二进制分离，然后对于其中1的所有位数，将cnt中对应的位置加上1。

这个做法中cnt的大小取决于arr中最大的数有多大，即最大的数为M，那么时间复杂度就是O(nlog(M))。

我在这里采用的是方法1，最后附上python代码：

```python
class Solution(object):
    def closestToTarget(self, arr, target):
        """
        :type arr: List[int]
        :type target: int
        :rtype: int
        """

        pow2 = [1]
        level = 0
        n = len(arr)
        while pow2[-1] <= n:
            pow2.append(pow2[-1] + pow2[-1])
            level += 1
        
        level -= 1
        pow2.pop()

        f = [[0] * (level + 1) for _ in range(n)]
        for j in range(level + 1):
            for i in range(n):
                if j == 0:
                    f[i][j] = arr[i]
                elif i + pow2[j] - 1 < n:
                    f[i][j] = f[i][j - 1] & f[i + pow2[j - 1]][j - 1]
        
        res = abs(arr[0] - target)
        l = r = 0
        now = arr[0]
        while r + 1 < n:
            r += 1
            now &= arr[r]
            res = min(res, abs(now - target))
            if res == 0:
                return res
            while l < r and now < target:
                l += 1
                p = l
                now = None
                j = level
                while p <= r:
                    while pow2[j] > r - p + 1:
                        j -= 1
                    if now is None:
                        now = f[p][j]
                    else:
                        now &= f[p][j]
                    
                    p += pow2[j]
                
                res = min(res, abs(now - target))
                if res == 0:
                    return res

        return res
```
