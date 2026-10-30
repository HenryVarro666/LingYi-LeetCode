---
title: "3754. 连接非零数字并乘以其数字和I & 3756. 连接非零数字并乘以其数字和II"
aliases: ["yiduobo的每日leetcode 3754.连接非零数字并乘以其数字和I && 3756.连接非零数字并乘以其数字和II", "3754. 连接非零数字并乘以其数字和I", "3756. 连接非零数字并乘以其数字和II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976042333851105115"
zhihu_id: "1976042333851105115"
zhihu_title: "yiduobo的每日leetcode 3754.连接非零数字并乘以其数字和I && 3756.连接非零数字并乘以其数字和II"
question_id: ["3754", "3756"]
question: ["连接非零数字并乘以其数字和 I", "连接非零数字并乘以其数字和 II"]
problem_url: ["https://leetcode.cn/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/", "https://leetcode.cn/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1968
created: "2025-11-24T19:09:32+08:00"
updated: "2025-11-24T19:09:35+08:00"
upvotes: 0
comments: 0
---

# 3754. 连接非零数字并乘以其数字和I & 3756. 连接非零数字并乘以其数字和II

> **[yiduobo的每日leetcode 3754.连接非零数字并乘以其数字和I && 3756.连接非零数字并乘以其数字和II](https://zhuanlan.zhihu.com/p/1976042333851105115) · 知乎 · 2025-11-24 · 赞同 0**
> 力扣：[3754. 连接非零数字并乘以其数字和 I](https://leetcode.cn/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/) · Easy · 灵茶山艾府：[不用字符串的做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3756. 连接非零数字并乘以其数字和 II](https://leetcode.cn/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/) · Medium · 灵茶山艾府：[三个前缀和（Python/Java/C++/Go）](../3756%20连接非零数字并乘以其数字和%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3754.连接非零数字并乘以其数字和I

[3754. 连接非零数字并乘以其数字和 I - 力扣（LeetCode）](https://leetcode.cn/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/description/)

3756.连接非零数字并乘以其数字和II

[3756. 连接非零数字并乘以其数字和 II - 力扣（LeetCode）](https://leetcode.cn/problems/concatenate-non-zero-digits-and-multiply-by-sum-ii/description/)

题目给出一个长度为m的字符串s，其中仅包含数字，长度不超过10^5。另外给出一个二维整数数组queries，其中queries\[index\] \= \[left\[index\], right\[index\]\]，其长度也不超过10^5。

对于每个queries[index]，提取子串s[left[index]: right[index] + 1]，将其中为0的数位去掉，得到一个新的整数x。若其中全为0，则x为0。接下来，将x中所有数位之和，与x相乘后，就得到了这次查询的答案。要求返回每组查询对应的答案，对10^9 + 7取模后的结果。

其中第一题可以认为是第二题中queries \= \[\[0, len(s) - 1\]\]的特殊情况。

对于区间[left, right]，其中各数位之和是典型的区间和，由于0不会对和产生影响，因此在这里可以直接计算s各数位的前缀和ss。方便起见记ss[0] \= 0，那么x的数位之和就是ss[right + 1] - ss[left]。

另一方面，而对于x自身的值，同样可以通过前缀之差计算得到。

如果不考虑0，那么s[left: right + 1]，就可以认为是s[:right + 1] - s[:left] \* 10^(right - left + 1)，例如12345中的34，可以认为是1234 - 12 \* 10^2。当然，直接记录s的前缀是不可行的，因为s太长了，记录不了这么大的数。不过本题需要对10^9 + 7取模，因此可以记录每种前缀对10^9 + 7取模后的结果。

不妨将这个数组记为v，方便起见，记v[0] \= 0，那么接下来只需要一趟遍历，对于当前遍历到的index，有v[index + 1] \= (v[index] \* 10 + s[index]) % (10^9 + 7)。

接下来考虑有0的情况。由于0在这里不应该被计入prefix，因此对于s[index]为0的位，v[index + 1]只需直接沿用v[index]的结果就行了。另外，在这里还需要注意10^(right - left + 1)这一项中也应该排除掉0的影响，于是可以使用另一个前缀数组non_zero记录前缀中非0元素出现的次数，同样的，初始情况下令non_zero[0] \= 0，那么left到right这一段中非0元素的数量就是non_zero[right + 1] - non_zero[left]，也就是说此时的x就应该是

v[right + 1] - v[left] \* 10^(non_zero[right + 1] - non_zero[left])

将其与上面得到的数位之和相乘即为此次查询对应的答案。

最后附上python代码：

```python
class Solution(object):
    def sumAndMultiply(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        ss = [0]
        v = [0]
        p10 = [1]
        non_zero = [0]
        mod = 10 ** 9 + 7
        for c in s:
            d = int(c)
            ss.append((ss[-1] + d) % mod)
            p10.append(p10[-1] * 10 % mod)
            if c != '0':
                v.append((v[-1] * 10 + d) % mod)
                non_zero.append(non_zero[-1] + 1)
            else:
                v.append(v[-1])
                non_zero.append(non_zero[-1])

        res = []
        for x, y in queries:
            ds = (ss[y + 1] - ss[x] + mod) % mod
            dv = (v[y + 1] - v[x] * p10[non_zero[y + 1] - non_zero[x]] % mod + mod) % mod
            res.append(ds * dv % mod)
        return res
```
