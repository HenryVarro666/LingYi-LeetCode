---
title: "3699. 锯齿形数组的总数I"
aliases: ["yiduobo的每日leetcode 3699.锯齿形数组的总数I"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1956403888853857760"
zhihu_id: "1956403888853857760"
zhihu_title: "yiduobo的每日leetcode 3699.锯齿形数组的总数I"
question_id: "3699"
question: "锯齿形数组的总数 I"
problem_url: "https://leetcode.cn/problems/number-of-zigzag-arrays-i/"
difficulty: "Hard"
rating: 2123
created: "2025-10-04T20:35:01+08:00"
updated: "2025-10-04T20:35:01+08:00"
upvotes: 1
comments: 0
---

# 3699. 锯齿形数组的总数I

> **[yiduobo的每日leetcode 3699.锯齿形数组的总数I](https://zhuanlan.zhihu.com/p/1956403888853857760) · 知乎 · 2025-10-04 · 赞同 1**
> 力扣：[3699. 锯齿形数组的总数 I](https://leetcode.cn/problems/number-of-zigzag-arrays-i/) · Hard · 灵茶山艾府：[前缀和优化 DP + 利用对称性优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3699.锯齿形数组的总数I

[3699. 锯齿形数组的总数 I - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-zigzag-arrays-i/description/)

题目给出三个整数n、l和r。长度为n的锯齿形数组定义如下：

1、数组中所有元素的取值范围都在l到r之间

2、数组中任意两个相邻元素都不相等

3、数组中任意三个元素都不能构成一个严格递增或者严格递减的序列

问可以构造出来的锯齿形数组的总数。

本题中n的取值范围在3到2000之间，l和r在1到2000之间。

从题面上看应该是非常标准的动态规划，不过在动手之前，可以先做一些简化。

首先，由于题目只需要关心数组中相邻元素的相对大小，因此在这里可以先将这个取值范围[l, r]转化为[0, r - l]，这样做有一个好处就是方便动态规划时的数组下标对应。

接下来，由于题目中构造的数组要么是^^^^^形的，要么是vvvvv形的，而对于任意一个^^^^^形的锯齿数组，其中元素的取值范围都在0到r - l之间，那么只需将所有元素都用r - l再减去，就可以得到一个vvvvv形的锯齿数组。也就是说，这两种类型的数组是一一对应的，那么在这里就只需要计算出^^^^^形数组的数量，乘以2即为最终答案。

接下来考虑如何计算形如^^^^^的锯齿形数组的数目。由于涉及到具体的取值，在这里可以用f[index][v]表示长度为index，且以v结尾的锯齿形数组的数目，方便期间，f数组从下标1开始计算。

值得一提的是，在这里不需要保留最后两个元素是上升还是下降，因为之前已经固定了f是用来计算形如^^^^^的锯齿形数组，因此偶数下标对应的就是上升，奇数下标对应的是下降。

对于f的初始值，可以先设置f[1][0]到f[1][r - l]都为1，也可以从f[2]开始计算，我在这里采用的是后者。对于长度为2的情况，由于必须是递增的情况，那么对于以v结尾的子数组，其上一个元素只能是0到v - 1中的某一个，一共v中选择。换言之，在这里就可以直接初始化f[2][v]为v。

接下来从3到n进行遍历，对于当前的index：

若index为偶数，那么v的上一个元素必须比v小，于是里就有

f[index][v] \= f[index - 1][0] + f[index - 1][1] + ... + f[index - 1][v - 1]

反过来，当index为奇数时，则有

f[index][v] \= f[index - 1][v + 1] + f[index - 1][v + 2] + ... + f[index - 1][r - l]

可以发现，两个转移方程分别是一个前缀和与一个后缀和的，可以同一转化为前缀和进行计算。

令s[index][v] \= f[index][0] + f[index][1] + ... + f[index][v]，那么上面的转移方程：

当index为偶数时，有

f[index][v] \= s[index - 1][v - 1]，在这里需要注意处理v为0的情况

当index为奇数时，有

f[index][v] \= s[index - 1][-1] - s[index - 1][v]

这样一来，就可以在O(n\*(r - l))的时间复杂度内计算出所有的f了。基于上面对称的结论，最终的结果就是s[n][-1]的两倍。

另外，由于f只依赖于上一轮的s，而s只依赖于本轮的f，因此s和f可以通过互相滚动的方式，优化掉index这一维。

最后附上python代码：

```python
class Solution(object):
    def zigZagArrays(self, n, l, r):
        """
        :type n: int
        :type l: int
        :type r: int
        :rtype: int
        """
        
        r -= l
        f = []
        s = []
        for v in range(r + 1):
            f.append(v)
            if not s:
                s.append(f[-1])
            else:
                s.append(s[-1] + f[-1])

        mod = 10 ** 9 + 7

        for length in range(3, n + 1):
            for v in range(r + 1):
                if length % 2 == 0:
                    if v == 0:
                        f[v] = 0
                    else:
                        f[v] = s[v - 1]
                else:
                    f[v] = s[-1] - s[v]
                    if f[v] < 0:
                        f[v] += mod
            
            s = []
            for v in range(r + 1):
                if not s:
                    s.append(f[v])
                else:
                    s.append(s[-1] + f[v])
                    if s[-1] >= mod:
                        s[-1] -= mod

        res = s[-1] + s[-1]
        if res >= mod:
            res -= mod
        return res
```
