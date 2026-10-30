---
title: "2311. 小于等于K的最长二进制子序列"
aliases: ["yiduobo的每日leetcode 2311.小于等于K的最长二进制子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/556059403"
zhihu_id: "556059403"
zhihu_title: "yiduobo的每日leetcode 2311.小于等于K的最长二进制子序列"
question_id: "2311"
question: "小于等于 K 的最长二进制子序列"
problem_url: "https://leetcode.cn/problems/longest-binary-subsequence-less-than-or-equal-to-k/"
difficulty: "Medium"
rating: 1840
created: "2022-08-21T00:07:13+08:00"
updated: "2022-08-21T00:07:13+08:00"
upvotes: 1
comments: 0
---

# 2311. 小于等于K的最长二进制子序列

> **[yiduobo的每日leetcode 2311.小于等于K的最长二进制子序列](https://zhuanlan.zhihu.com/p/556059403) · 知乎 · 2022-08-21 · 赞同 1**
> 力扣：[2311. 小于等于 K 的最长二进制子序列](https://leetcode.cn/problems/longest-binary-subsequence-less-than-or-equal-to-k/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2311.小于等于K的最长二进制子序列

[力扣](https://leetcode.cn/problems/longest-binary-subsequence-less-than-or-equal-to-k/)

既然是在二进制下比较，那么首先就应该计算出k的二进制表示，不妨将其记为binary_k。

接下来令m \= len(s)，n \= len(binary_k)，若m \< n，那么说明s一定小于binary_k，此时的答案就是整个s的长度m。而当m >\= n时，最理想的情况就是s的最后n位小于等于binary_k，然后取这n位配合上前面所有的0。一个简单的证明是此时如果不舍弃掉最后n位中的数，那么就不能将前面的1加入到答案中，否则必然会出现一个以1开头且长度大于n的后缀。反之，如果为了添加前面的1而舍弃最后n为中的数明显是不赚的，并不会使得最后的子序列长度变得更长。

于是可以判断s最后n位是否小于等于binary_k，如果满足，那么答案就是n加上前面所有0的数量。若不满足，那么此时最优解就是n - 1加上前面所有0的数量，即取最后n为中的任意n - 1个数，配合上前面所有的0就行了。

最后附上python代码：

```python
class Solution(object):
    def longestSubsequence(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        m = len(s)
        binary_k = []
        while k:
            binary_k.append(k % 2)
            k /= 2
        
        n = len(binary_k)
        binary_k.reverse()
        if m < n:
            return m
        
        p = m - n
        flag = False
        for index, num in enumerate(binary_k):
            if str(num) < s[index + p]:
                flag = True
                break
            elif str(num) > s[index + p]:
                break
        
        if flag:
            res = n - 1
        else:
            res = n

        for index in range(p):
            if s[index] == '0':
                res += 1
        
        return res
```
