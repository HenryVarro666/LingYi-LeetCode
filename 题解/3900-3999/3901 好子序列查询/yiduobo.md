---
title: "3901. 好子序列查询"
aliases: ["yiduobo的每日leetcode 3901.好子序列查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/segment-tree", "leetcode/number-theory", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/八-树状数组和线段树", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2028606952519770122"
zhihu_id: "2028606952519770122"
zhihu_title: "yiduobo的每日leetcode 3901.好子序列查询"
question_id: "3901"
question: "好子序列查询"
problem_url: "https://leetcode.cn/problems/good-subsequence-queries/"
difficulty: "Hard"
rating: 2545
created: "2026-04-18T00:46:50+08:00"
updated: "2026-04-18T00:47:00+08:00"
upvotes: 0
comments: 0
---

# 3901. 好子序列查询

> **[yiduobo的每日leetcode 3901.好子序列查询](https://zhuanlan.zhihu.com/p/2028606952519770122) · 知乎 · 2026-04-18 · 赞同 0**
> 力扣：[3901. 好子序列查询](https://leetcode.cn/problems/good-subsequence-queries/) · Hard · 灵茶山艾府：[结论+证明，用线段树维护（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3901.好子序列查询

<https://leetcode.cn/problems/good-subsequence-queries/description/>

给出一个长度为n的整数数组nums以及一个整数p，其中n、p以及nums中的元素大小都不超过50000。

若nums的某个长度严格小于n的非空子序列中，各元素的最大公约数恰好等于p，那么就称其为好子序列。

另外给出一个长度为q的二维整数数组queries，其中queries\[index\] \= \[idx\[index\], val\[index\]\]，表示将nums\[index\]更新为val\[index\]。

每次查询后，检测数组中是否存在任意好子序列。要求有多少次查询时，数组中存在好子序列。

如果不考虑长度严格小于n的限制，那么一个最大公约数为p的子序列必然满足：

- 其中每个元素都是p的倍数
- 所有元素除以p之后，得到的商形成的子序列的最大公约数恰好为1

由于最大公约数是随着子序列的加长而单调不增的，因此如果无考虑n的限制，就只需检测nums中所有p的倍数在除以p之后，得到的商的子序列的最大公约数是否为1。

另一方面， 题目中每次查询都是单点修改，如果不考虑长度小于n的限制，那么可以就是非常明确的单点修改，区间求最大公约数问题，可以通过线段树来处理。

再具体实现上，可以设置非p倍数的叶子节点值为none，而对于非叶子节点值，若左右两个子区间对应的值都为none，那么当前节点值也为none；若一侧为none，那么就取另一侧的值；若两侧都有值，就取二者的最大公约数即可。这样一来，只需对每次查询都进行单点修改，然后检测整棵线段树的根结点对应的值是否为1即可。

接下来，则需要考虑长度不能等于n这一限制。

首先，可以很快找出case，满足所有元素的最大公约数为p，但是任取子序列的最大公约数都不为p，例如p \= 2时，一共三个元素，两两之间的最大公约数分别为6、10、14，很容构造出数组[30, 42, 70]，这三个数的最大公约数恰好等于2，而[30, 42]的最大公约数是6，[30, 70]的最大公约数是10，[42, 70]的最大公约数是14。

也就是说，当数组中所有元素都是p的倍数，且这些数除以p之后的商形成的数组的最大公约数恰好为1时，并不好判断是否存在长度恰好为n - 1的好子序列。

在这里就不妨反过来思考：若数组中所有元素都是p的倍数且最大公约数为p的话，且不存在好子序列的话，任取一个长度为n - 1的子序列，这些子序列的最大公约数都不为p，且这些子序列的最大公约数必须互不相同，否则两个长度为n - 1的不同子序列，它们的最大公约数相同且不等于p的话，那么整个数组的最大公约数就不可能为p。一共存在n个不同的长度为n - 1的不同子序列，那么就意味着有n种不同的最大公约数，但是由于题目中nums的大小被限制在了50000以内，每个元素至多只有6个不同的质因子，因此上面所说的这种难处理的case，只有在n \<\= 6的情况才会出现。这样就好办了，对于n小于等于6的情况，直接暴力枚举所有子序列检测就行了，而对于n更大的情况，则只需要利用线段树检测所有p的倍数，在除以p之后的商形成的子序列的最大公约数是否为1即可。

最后附上python代码：

```python
class Solution(object):
    def countGoodSubseq(self, nums, p, queries):
        """
        :type nums: List[int]
        :type p: int
        :type queries: List[List[int]]
        :rtype: int
        """
        
        n = len(nums)
        res = 0

        def gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        if n <= 6:
            for index, v in queries:
                nums[index] = v
                flag = False
                for state in range(1, (1 << n) - 1):
                    g = None
                    for idx in range(n):
                        if (state & (1 << idx)) == (1 << idx) and nums[idx] % p == 0:
                            if g is None:
                                g = nums[idx]
                            else:
                                g = gcd(g, nums[idx])

                    if g == p:
                        flag = True
                        break

                if flag:
                    res += 1

            return res

        f = [None] * (n * 4)

        def update(x, left, right, index, v):
            if left == right:
                f[x] = v
                return

            mid = (left + right) // 2
            if index <= mid:
                update(x + x + 1, left, mid, index, v)
            else:
                update(x + x + 2, mid + 1, right, index, v)
            
            if f[x + x + 1] is None:
                if f[x + x + 2] is None:
                    f[x] = None
                else:
                    f[x] = f[x + x + 2]
            elif f[x + x + 2] is None:
                f[x] = f[x + x + 1]
            else:
                f[x] = gcd(f[x + x + 1], f[x + x + 2])
        
        tot = 0
        cnt = {}

        for index, v in enumerate(nums):
            if v % p == 0:
                v //= p
            else:
                v = None
            update(0, 0, n - 1, index, v)
        
        for index, v in queries:
            if v % p == 0:
                v //= p
            else:
                v = None
            update(0, 0, n - 1, index, v)

            if f[0] == 1:
                res += 1
        
        return res
```
