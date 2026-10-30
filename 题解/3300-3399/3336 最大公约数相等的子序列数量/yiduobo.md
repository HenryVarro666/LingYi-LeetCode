---
title: "3336. 最大公约数相等的子序列数量"
aliases: ["yiduobo的每日leetcode 3336.最大公约数相等的子序列数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "leetcode/number-theory", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/一-数论", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25209262184"
zhihu_id: "25209262184"
zhihu_title: "yiduobo的每日leetcode 3336.最大公约数相等的子序列数量"
question_id: "3336"
question: "最大公约数相等的子序列数量"
problem_url: "https://leetcode.cn/problems/find-the-number-of-subsequences-with-equal-gcd/"
difficulty: "Hard"
rating: 2403
created: "2025-02-21T02:55:08+08:00"
updated: "2025-02-21T02:55:08+08:00"
upvotes: 3
comments: 0
---

# 3336. 最大公约数相等的子序列数量

> **[yiduobo的每日leetcode 3336.最大公约数相等的子序列数量](https://zhuanlan.zhihu.com/p/25209262184) · 知乎 · 2025-02-21 · 赞同 3**
> 力扣：[3336. 最大公约数相等的子序列数量](https://leetcode.cn/problems/find-the-number-of-subsequences-with-equal-gcd/) · Hard · 灵茶山艾府：[两种方法：多维 DP / 倍数容斥（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3336.最大公约数相等的子序列数量

[3336. 最大公约数相等的子序列数量 - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-number-of-subsequences-with-equal-gcd/)

题目给出一个整数数组nums，要求统计所有满足下面两个条件的非空子序列对(seq1, seq2)的数量：

1、子序列seq1和seq2不相交，即nums中不存在同时出现在两个序列中的下标

2、seq1中元素的最大公约数与seq2中元素的最大公约数相等

问有多少组满足条件的子序列对。

题目涉及到子序列对的计数，同时需要考虑最大公约数，看上去必须想办法从数值方面入手来进行计算。

在这里不妨先思考一下如何计算seq1的最大公约数为first，seq2的最大公约数为second的序列对应该如何计算。由于需要从数值方面入手计算，那么与最大公约数有关的就是倍数关系了，受到之前3312题的启发，在这里也可以使用类似的方法来进行计算。

[yiduobo：yiduobo的每日leetcode 3312.查询排序后的最大公约数](https://zhuanlan.zhihu.com/p/1709794890)

具体来说，就是先计算由值为first的倍数的元素构成seq1，由值为second的倍数的元素构成seq2，且seq1和seq2不相交的序列对的数目g[first][second]，然后用g[first][second]减去f[first \* 2][second]、f[first \* 3][second]、...、f[first][second \* 2]、f[first \* 2][second \* 2]、...、f[first \* p][second \* q]之后，得到的就是f[first][second]。在这里first \* p和second \* q的上界都是最大公约数的最大可能取值，可以简单设置为nums中最大的元素。

例如需要计算f[2][3]，设最大元素为6，那么在这里需要先计算出g[2][3]，然后用g[2][3]减去f[2][6]、f[4][3]、f[4][6]、f[6][3]、f[6][6]，就可以得到f[2][3]了。理由是在g[2][3]中，虽然seq1中的元素都是2的倍数，但是这些元素构成的子序列的最大公约数可能是2、4、6，同理，seq2中元素构成的子序列的最大公约数可能是3、6，因此g[2][3]实际上记录了所有这些子序列对，那么为了得到f[2][3]，就需要从中减去其他的f。

另一方面，对于f[6][6]，其必然就等于g[6][6]，因为没有其他可能了，而f[4][6]则等于g[4][6]减去f[6][6]。换言之，在这里只需要先计算得到所有的g，就可以倒序遍历逐个计算出所有的f了。

---

接下来的问题就变成了如何计算数组g。

不妨考虑g[first][second]应该如何计算。首先可以明确的是，nums中的元素可以分为4类，分别是

1）既是first的倍数，又是second的倍数。对于这一类的数，不妨设lcm为first和second的最小公倍数，那么这一类数实际上就是nums中所有为lcm倍数的数

2）仅是first的倍数

3）仅是second的倍数

4）都不是

可以发现，第一类数有三种选择，即放进seq1、放进seq2、或者两边都不放。而第二、三类的数则只能选择放进对应的seq，或者不妨。最后这一类不需要考虑。

不妨设前三类数的数目分别为x、y、z，那么直观上来看，可以形成的合法子序列对就是(3^x) \* (2^y) \* (2^z)，分别表示三类数中每种数可行的选择数目。

不过需要注意的是，题目要求构造的是非空子序列，因此在上面的式子中，若2^y中唯一这一种可能：第二类的数全都不选，遇上3^x中的2^x种可能：第一类的数不选或者放进seq2，那么seq1就是空子序列，此时的第三类数如何选择不影响，也就是说其中一共有(2^x) \* (2^z)种可能选出空的seq1。

同样的道理，有(2^x) \* (2^y)种可能选出空的seq2。

也就是说，应该在(3^x) \* (2^y) \* (2^z)的基础上分别减去(2^x) \* (2^z)和(2^x) \* (2^y)才行。

但是在这里需要特别注意的是，在(2^x) \* (2^z)和(2^x) \* (2^y)这些选择方法中还包含了一种重复的选取方法，那就是两个子序列都为空。这种情况被减去了两次，因此最终的次数还应该再加上1。

综合起来，就有g[first][second] \= (3^x) \* (2^y) \* (2^z) - (2^x) \* (2^z) - (2^x) \* (2^y) + 1。

到了这里，还需要解决一个问题就是x、y、z应该如何计算。

经过了上面的思考，在这里再次运用倍数间的减法就是很容易想到的处理方法了。令mul[v]表示nums中为v的倍数的元素数量，那么x就等于mul[lcm]，而y和z则分别为mul[first] - mul[lcm]以及mul[second] - mul[lcm]。这样一来，只需要先遍历nums中的每个元素x，然后利用类似筛法的处理方法，从x开始，按x为步长遍历到数组中的最大元素就能得到mul数组，接下来就可以计算出g数组了。

最后附上python代码：

```python
class Solution(object):
    def subsequencePairCount(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        ma = max(nums)
        cnt = [0] * (ma + 1)
        for v in nums:
            cnt[v] += 1
        
        mul = [0] * (ma + 1)
        for v in range(1, ma + 1):
            for x in range(v, ma + 1, v):
                mul[v] += cnt[x]

        pow3 = [1]
        pow2 = [1]
        mod = 10 ** 9 + 7
        for index in range(1, max(mul) + 1):
            pow3.append(pow3[-1] * 3 % mod)
            pow2.append(pow2[-1] * 2 % mod)

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x

        seq_pair = [[0] * (ma + 1) for _ in range(ma + 1)]
        for first in range(1, ma + 1):
            for second in range(1, ma + 1):
                if mul[first] == 0 or mul[second] == 0:
                    continue
                lcm = first * second // gcd(first, second)
                if lcm <= ma:
                    lcm_cnt = mul[lcm]
                else:
                    lcm_cnt = 0

                seq_pair[first][second] = pow3[lcm_cnt] * pow2[mul[first] - lcm_cnt] % mod * pow2[mul[second] - lcm_cnt] % mod
                seq_pair[first][second] -= pow2[mul[first]]
                if seq_pair[first][second] < 0:
                    seq_pair[first][second] += mod
                seq_pair[first][second] -= pow2[mul[second]]
                if seq_pair[first][second] < 0:
                    seq_pair[first][second] += mod
                seq_pair[first][second] += 1
                if seq_pair[first][second] >= mod:
                    seq_pair[first][second] -= mod

        final_pair = [[0] * (ma + 1) for _ in range(ma + 1)]
        for s in range(ma + ma, 1, -1):
            for first in range(ma, 0, -1):
                second = s - first
                if second <= 0 or second > ma or seq_pair[first][second] == 0:
                    continue
                final_pair[first][second] = seq_pair[first][second]
                for x in range(first, ma + 1, first):
                    for y in range(second, ma + 1, second):
                        if x > first or y > second:
                            final_pair[first][second] -= final_pair[x][y]
                            if final_pair[first][second] < 0:
                                final_pair[first][second] += mod

        res = 0
        for v in range(1, ma + 1):
            res += final_pair[v][v]
            if res >= mod:
                res -= mod
        return res
```
