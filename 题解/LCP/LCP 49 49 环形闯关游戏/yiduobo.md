---
title: "LCP 49. 环形闯关游戏"
aliases: ["yiduobo的每日leetcode LCP49.环形闯关游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/577292776"
zhihu_id: "577292776"
zhihu_title: "yiduobo的每日leetcode LCP49.环形闯关游戏"
question_id: "LCP 49"
question: "环形闯关游戏"
created: "2022-10-26T03:27:03+08:00"
updated: "2022-10-26T03:27:03+08:00"
upvotes: 1
comments: 0
---

# LCP 49. 环形闯关游戏

> **[yiduobo的每日leetcode LCP49.环形闯关游戏](https://zhuanlan.zhihu.com/p/577292776) · 知乎 · 2022-10-26 · 赞同 1**
> 力扣：LCP 49. 环形闯关游戏

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP49.环形闯关游戏

[力扣](https://leetcode.cn/problems/K8GULz/)

题目的数据规模非常大，不过涉及到位运算，那么一个自然的想法就是从高位开始逐位向下确定当前位为0时能否完成闯关。若可以，那么该位就是0，否则该位是1。

由于题目中只能与比当前值更小的数进行按位或运算，那么对于最高位上的1，就必须要最终答案一开始就带了这个1，否则的话无论怎么安排闯关顺序不可能得到最高位上的1。

接下来就需要按位枚举后面位上的1，对于当前枚举的结果res，需要检测以res开头能否完成闯关。

题目中的关卡是环形的，简单起见在这里不妨先考虑解决线性的闯关问题，因为环形问题通常可以通过复制多份来转化为线性的问题。于是当前的问题就变成了，给出一个数组，能否找到一个位置p，从p开始向左右两侧扩展可以扩展完整个数组。这里的扩展指的的是若当前的res >\= nums[p]，那么就将nums[p]通过或运算合并到res中。

上面这种判定方法，可能有一个疑问是如果出现某种需要先向左侧位置p扩展，合并左侧值nums[p]之后才能向右侧位置q扩展的情况应该怎么办。

对于这类情况，如果一开始无法向q扩展，说明nums[q]的某个高位上存在1，且当前res和可扩展的右侧值中都没有这一位1，但nums[p]存在这一位1。对于这种情况，如果可以从当前位置开始扩展到nums[p]，那么反过来，从nums[p]开始向右也必然可以扩展到当前的数，这是因为从nums[p]开始的话自带了这个右侧都不存在的高位的1，必然是大于等于右侧这些数的。

在确定了这种判定方式的正确性之后，就可以一趟遍历，计算出从数组中的每个数开始向左和向右最远能扩展到哪个位置。接下来遍历数组中的每个位置，若从当前位置开始可以扩展完整个数组，说明从当前数开始可以完成闯关。当然，朴素的逐位枚举然后扩展依然是O(n^2)的，但是在这里同样可以利用单调性。即从nums[p]可以扩展到nums[p + 1]的话，那么从nums[p + 1]开始可扩展的最远位置就是从nums[p]开始可扩展的最远位置，于是在这里可以利用类似于求解下一个更大数的单调栈的做法，在一趟遍历的时间内求出所有数向右扩展的最远位置。同样的，反向遍历一趟，就可以求出所有数向左扩展的最远位置。

到了这里，就得到了一种在O(n)时间内判断当前res能否完成线性数组中闯关的算法。

接下来，将问题还原成环形数组。此时只需将数组复制三次，然后正中间n到2n - 1的部分，求解最左侧和最右侧可扩展的位置，然后遍历这个中间部分，若其最右侧扩展的位置减去最左侧扩展的位置大于等于n，说明其可以扩展整个数组，即可以完成闯关。

最后附上python代码：

```python
class Solution(object):
    def ringGame(self, challenge):
        """
        :type challenge: List[int]
        :rtype: int
        """

        n = len(challenge)
        ma = max(challenge)
        max_l = 0
        while ma:
            max_l += 1
            ma /= 2
        
        pow2 = 1
        for index in range(max_l - 1):
            pow2 += pow2
        
        check_list = challenge[:] + challenge[:] + challenge[:]

        def check():
            left = [None] * n
            right = [None] * n

            stack = []
            now = res
            p = n
            while p < n + n:
                while p < n + n + n and now >= check_list[p]:
                    now |= check_list[p]
                    if p < n + n:
                        stack.append(p)
                    p += 1
            
                while stack:
                    right[stack[-1] - n] = p
                    stack.pop()
                
                if p < n + n:
                    right[p - n] = p
                now = res
                p += 1
            
            stack = []
            now = res
            p = n + n - 1
            while p >= n:
                while p >= 0 and now >= check_list[p]:
                    now |= check_list[p]
                    if p >= n:
                        stack.append(p)
                    p -= 1
                
                while stack:
                    left[stack[-1] - n] = p
                    stack.pop()
                
                if p >= n:
                    left[p - n] = p
                now = res
                p -= 1

            for index in range(n):
                if right[index] - 1 - left[index] >= n:
                    return True

            return False

        res = pow2 + pow2 - 1
        pow2 /= 2
        while pow2:
            res -= pow2
            if not check():
                res += pow2
            pow2 /= 2

        return res
```
