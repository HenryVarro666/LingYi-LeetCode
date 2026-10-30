---
title: "3525. 求出数组的X值II"
aliases: ["yiduobo的每日leetcode 3525.求出数组的X值II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/math", "leetcode/divide-and-conquer", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1904627989066551510"
zhihu_id: "1904627989066551510"
zhihu_title: "yiduobo的每日leetcode 3525.求出数组的X值II"
question_id: "3525"
question: "求出数组的 X 值 II"
problem_url: "https://leetcode.cn/problems/find-x-value-of-array-ii/"
difficulty: "Hard"
rating: 2645
created: "2025-05-11T22:50:45+08:00"
updated: "2025-05-11T22:50:45+08:00"
upvotes: 1
comments: 0
---

# 3525. 求出数组的X值II

> **[yiduobo的每日leetcode 3525.求出数组的X值II](https://zhuanlan.zhihu.com/p/1904627989066551510) · 知乎 · 2025-05-11 · 赞同 1**
> 力扣：[3525. 求出数组的 X 值 II](https://leetcode.cn/problems/find-x-value-of-array-ii/) · Hard · 灵茶山艾府：[从分治到线段树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3525.求出数组的X值II

[3525. 求出数组的 X 值 II - 力扣（LeetCode）](https://leetcode.cn/problems/find-x-value-of-array-ii/description/)

题目给出一个由正整数组成的数组nums，以及一个正整数k。其中nums的长度不超过10^5，其中元素值的取值范围在1到10^9之间，同时k的取值范围在1到5之间。

另外已给出一个二维数组queries，其中queries\[i\] \= \[index\[i\], value\[i\], start\[i\], x\[i\]\]。

对于queries中的每个查询，需要：

1、将nums\[index\[i\]\]的值更新为value\[i\]，这个修改将影响到后续所有的询问

2、计算nums中以start[i]开头的子数组nums[start[i]:]对应的x[i]值

其中数组的x[i]值指的是对数组执行一次移除操作后，数组中剩余元素之积模k的余数为x[i]的移除方案数。这里的移除操作可以移除掉数组的某个后缀，移除的后缀可以为空，但是移除后的数组不能为空。

本题中关于x值的定义与上题略有不同，计算的是子数组移除某个后缀之后，剩余元素之积模k余x的移除方案数，那么实际上可以认为是子数组中有多少前缀的乘积模k余x。另一方面，本题中还有单点的修改操作，询问的对象也变成了原数组的某个后缀子数组，因此实际上可以认为是单点修改以及区间查询。

对于这类问题，第一想法自然是往线段树上去靠。由于需要解决的问题是如何计算区间中前缀乘积模k余x的数量，那么在这里就可以令f[x][now]表示对于线段树中节点now对应的区间，其中有多少个前缀乘积模k恰好等于x。而对于f[x][now]的计算，不妨设now对应的区间为[left, right]，那么：

1、若left \= right：

此时区间中就只有nums[left]这唯一的一个元素，因此可以先将f[0][now]到f[k - 1][now]全部置为0，然后将f[nums[left] % k][now]置为1

2、若left \< right：

与常规的线段树操作相同，此时依然是先将区间一分为二，计算中点mid \= (left + right) // 2。

接下来，先递归计算左右两个子区间对应的f值，接下来从0到k - 1枚举x，就有

2-1）对于左半边区间：

左半边区间的前缀也是当前区间的前缀，因此可以直接将左半边中符合条件的前缀数量直接累加到当前区间符合条件的前缀数量中，也就是将f[x][now.leftchild]累加到f[x][now]中。其中now.leftchild表示now在线段树中的左孩子，其对应的区间就是[left, mid]。

2-2）对于右半边区间：

右半边区间的前缀必须拼接上整个左半边区间，才能形成当前区间的前缀，因此在这里还需要先计算左半边区间的乘积。

区间乘积的具体计算方法依然是使用线段树。令mul[now]表示now对应区间的乘积模k的结果，那么当left \= rigth时，mul[now]就等于nums[left] % k，否则mul[now] \= mul[now.leftchild] \* mul[now.rightchlid] % k。

回到计算f上来。此时有左半边区间的乘积为mul[now.leftchild]，那么在这里就可以将f[x][now.rightchild]累加到f[x \* mul[now.leftchild] % k][now]中。

这样一来，初始线段树的建立就完成了。而对于单点更新操作，只需要自顶向下找到线段树中对应的节点，修改其对应的mul以及f，然后在回溯的过程中更新其所有祖先节点对应的f和mul即可，更新方式与上面相同。

另外对于查询操作，也是按照常规线段树的区间查询，根据查询区间落在当前区间的哪个部分来决定如何计算，稍有不同的地方是如果查询区间跨越了左右两个半边区间的，此时应该递归查询落在左半边区间中的部分，而对于落在右半边区间的部分，则需要先计算落在左半边区间中的部分的乘积left_r，然后从0到k - 1枚举v，若v \* left_r % x等于k，则递归查询落在右半边区间中的部分，不过查询的x值此时应该变为v，理由与上面相同，右半边区间的前缀必须与左半边的全体元素拼接，才能形成整个子区间的前缀。

最后附上python代码：

```python
class Solution(object):
    def resultArray(self, nums, k, queries):
        """
        :type nums: List[int]
        :type k: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        res = []
        n = len(nums)
        f = [[0] * (n * 4) for _ in range(k)]
        mul = [0] * (n * 4)

        def build(now, left, right, f, mul):
            if left == right:
                mul[now] = nums[left] % k
                for x in range(k):
                    f[x][now] = 0
                f[nums[left] % k][now] = 1
                return
            
            mid = (left + right) >> 1
            build(now + now + 1, left, mid, f, mul)
            build(now + now + 2, mid + 1, right, f, mul)

            mul[now] = mul[now + now + 1] * mul[now + now + 2] % k
            for x in range(k):
                f[x][now] += f[x][now + now + 1]
                f[x * mul[now + now + 1] % k][now] += f[x][now + now + 2]

        def update(now, left, right, p, v, f, mul):
            if left == right:
                mul[now] = v % k
                for x in range(k):
                    f[x][now] = 0
                f[v][now] = 1
                return 
            
            mid = (left + right) >> 1
            if p <= mid:
                update(now + now + 1, left, mid, p, v, f, mul)
            else:
                update(now + now + 2, mid + 1, right, p, v, f, mul)
            
            for x in range(k):
                f[x][now] = f[x][now + now + 1]

            left_r = mul[now + now + 1]
            for x in range(k):
                f[x * left_r % k][now] += f[x][now + now + 2]

            mul[now] = mul[now + now + 1] * mul[now + now + 2] % k

        def find_mul(now, left, right, start, end, mul):
            if left == start and right == end:
                return mul[now]
            
            mid = (left + right) >> 1
            if end <= mid:
                return find_mul(now + now + 1, left, mid, start, end, mul)
            elif start > mid:
                return find_mul(now + now + 2, mid + 1, right, start, end, mul)
            else:
                left_r = find_mul(now + now + 1, left, mid, start, mid, mul)
                if left_r == 0:
                    return 0
                return left_r * find_mul(now + now + 2, mid + 1, right, mid + 1, end, mul) % k

        def find_x(now, left, right, start, end, x, f, mul):
            if left == start and right == end:
                return f[x][now]
            
            mid = (left + right) >> 1
            if end <= mid:
                return find_x(now + now + 1, left, mid, start, end, x, f, mul)
            elif start > mid:
                return find_x(now + now + 2, mid + 1, right, start, end, x, f, mul)
            else:
                res = find_x(now + now + 1, left, mid, start, mid, x, f, mul)
                left_r = find_mul(now + now + 1, left, mid, start, mid, mul)
                if left_r == 0:
                    if x == 0:
                        return res + end - mid
                    else:
                        return res

                for v in range(k):
                    if v * left_r % k == x:
                        res += find_x(now + now + 2, mid + 1, right, mid + 1, end, v, f, mul)
                return res
        

        build(0, 0, n - 1, f, mul)
        for index, value, start, x in queries:
            update(0, 0, n - 1, index, value % k, f, mul)
            res.append(find_x(0, 0, n - 1, start, n - 1, x, f, mul))
        
        return res
```
