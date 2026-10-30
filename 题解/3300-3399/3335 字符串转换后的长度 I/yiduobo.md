---
title: "3335. 字符串转换后的长度I & 3337. 字符串转换后的长度II"
aliases: ["yiduobo的每日leetcode 3335.字符串转换后的长度I && 3337.字符串转换后的长度II", "3335. 字符串转换后的长度I", "3337. 字符串转换后的长度II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "leetcode/hard", "题单/动态规划", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/24931617972"
zhihu_id: "24931617972"
zhihu_title: "yiduobo的每日leetcode 3335.字符串转换后的长度I && 3337.字符串转换后的长度II"
question_id: ["3335", "3337"]
question: ["字符串转换后的长度 I", "字符串转换后的长度 II"]
problem_url: ["https://leetcode.cn/problems/total-characters-in-string-after-transformations-i/", "https://leetcode.cn/problems/total-characters-in-string-after-transformations-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2412
created: "2025-02-20T01:17:06+08:00"
updated: "2025-02-20T01:17:06+08:00"
upvotes: 1
comments: 0
---

# 3335. 字符串转换后的长度I & 3337. 字符串转换后的长度II

> **[yiduobo的每日leetcode 3335.字符串转换后的长度I && 3337.字符串转换后的长度II](https://zhuanlan.zhihu.com/p/24931617972) · 知乎 · 2025-02-20 · 赞同 1**
> 力扣：[3335. 字符串转换后的长度 I](https://leetcode.cn/problems/total-characters-in-string-after-transformations-i/) · Medium · 灵茶山艾府：[矩阵快速幂优化 DP（Python/NumPy/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3337. 字符串转换后的长度 II](https://leetcode.cn/problems/total-characters-in-string-after-transformations-ii/) · Hard · 灵茶山艾府：[两种方法：矩阵快速幂优化 DP / BM+Kitamasa（Python/NumPy/Java/C++/Go）](../3337%20字符串转换后的长度%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3335.字符串转换后的长度I

[3335. 字符串转换后的长度 I - 力扣（LeetCode）](https://leetcode.cn/problems/total-characters-in-string-after-transformations-i/description/)

3337.字符串转换后的长度II

[3337. 字符串转换后的长度 II - 力扣（LeetCode）](https://leetcode.cn/problems/total-characters-in-string-after-transformations-ii/description/)

先描述3337题。3337题给出一个由小写英文字母构成的字符串s，以及一个整数t，表示需要执行转换的次数。另外给出一个长度为26的数组nums，每次转换需要根据一下规则替换s中的每个字符：

将s[i]替换为字母表中后续的nums[s[i] - 'a']个连续字符。例如s[i] \= 'a'且nums[0] \= 3，那么需要将'a'替换为后面的3个连续字符，即'bcd'。另外，若转换超出了'z'，那么就需要回绕到字母表开头。例如s[i] \= 'y'且nums[24] \= 3，那么需要将'y'替换为后面的3个连续字符，即'zab'。

问恰好执行t次后得到的字符串长度为多少。

3335题则可以认为是3337题的一个特例：同样是给出s和t，另外固定了nums \= [1, 1, 1, ..., 1, 1, 1, 2]，问执行t次后得到的字符串长度为多少。

---

题目的数据规模很大，其中s的长度可以达到10^5，而t则来到了10^9，因此直接模拟显然是不行的，需要想办法进行优化。

由于字符串中只包含小写字符，且变换的规则是固定的，因此一个自然的想法就是令f\[index\]\[c\]表示执行index次操作后，字符串中第c种字符的数量。那么对于f\[index\]\[c\]，c将在下次变换中变为c后面的连续nums\[c\]个字符，也就是第c + 1到c + nums\[c\]种字符，因此需要将f\[index\]\[c\]累加到f\[index + 1\]\[c + 1\]、f\[index + 1\]\[c + 2\]、...、f\[index + 1\]\[c + nums\[c\]\]中。计算完成后，sum(f\[t\])即为最终答案。

然而t在这里非常大，直接递推依然是不行的，需要进一步进行优化。

---

对于这类项与项之间关系固定的递归式，一种常见的优化方法就是快速幂加矩阵乘法进行优化。

不妨将f[index]想象成一个1 \* 26的矩阵A，那么在这里就需要构造一个26 \* 26的乘数矩阵B，这个矩阵表示的是状态转移的关系，目标是让A \* B得到的结果矩阵C恰好就是f[index + 1]。

本题中的B是很好构造的。根据矩阵乘法的定义，A\[0\]\[i\] \* B\[i\]\[j\]将会被累加到C\[0\]\[j\]中。由于第i种字符将会变成第i + 1种到第i + nums\[i\]种字符，因此在这里B\[i\]\[i + 1\]到B\[i\]\[i + nums\[i\]\]都应该等于1，而B\[i\]中其他的列则应该为0。

根据上面的结论，就可以先初始化B为26 \* 26的全0矩阵，接下来从0到25枚举i，然后从i + 1到i + nums[i]枚举j，然后将B[i][j % 26]置为1就行了。

得到矩阵B之后，就有f[t] \= f[0] \* B \* B \* ... \* B，这里一共是t个B。由于矩阵乘法是满足结合律的，因此对于后面这t个B可以通过快速幂在log(t)的时间内计算出结果，这样一来时间复杂度就优化到了O(n + 26^3 \* log(t))了。

值得一提的是，矩阵快速幂在优化递推时是常见的技巧，有兴趣的读者不妨思考一下对于斐波那契数列应该如何构造矩阵B。

最后附上3337题的python代码，3335题只需将nums置为[1, 1, 1, ..., 1, 1, 2]即可：

```
class Solution(object):
    def lengthAfterTransformations(self, s, t, nums):
        """
        :type s: str
        :type t: int
        :type nums: List[int]
        :rtype: int
        """
        
        def generate(nums):
            n = len(nums)
            base = [[0] * n for _ in range(n)]
            for i, x in enumerate(nums):
                for j in range(i + 1, i + x + 1):
                    base[i][j % n] = 1
            
            return base
            
        base = generate(nums)

        res = [[0] * 26]
        for char in s:
            res[0][ord(char) - 97] += 1
        
        mod = 10 ** 9 + 7

        def mul(a, b):
            m = len(a)
            n = len(a[0])
            o = len(b[0])

            c = [[0] * o for _ in range(m)]
            for i in range(m):
                for j in range(n):
                    for k in range(o):
                        c[i][k] = (c[i][k] + a[i][j] * b[j][k]) % mod
            
            return c

        while t:
            if t & 1:
                res = mul(res, base)
            
            base = mul(base, base)
            t >>= 1

        return sum(res[0]) % mod
```
