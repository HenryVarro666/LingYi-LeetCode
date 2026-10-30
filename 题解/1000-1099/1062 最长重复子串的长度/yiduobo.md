---
title: "1062. 最长重复子串"
aliases: ["yiduobo的每日leetcode 1062.最长重复子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/suffix-array", "题单/字符串", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/607671228"
zhihu_id: "607671228"
zhihu_title: "yiduobo的每日leetcode 1062.最长重复子串"
question_id: "1062"
question: "最长重复子串的长度"
problem_url: "https://leetcode.cn/problems/longest-repeating-substring/"
difficulty: "Medium"
rating: 1044
created: "2023-02-19T19:51:43+08:00"
updated: "2023-02-19T19:51:43+08:00"
upvotes: 0
comments: 0
---

# 1062. 最长重复子串

> **[yiduobo的每日leetcode 1062.最长重复子串](https://zhuanlan.zhihu.com/p/607671228) · 知乎 · 2023-02-19 · 赞同 0**
> 力扣：[1062. 最长重复子串的长度](https://leetcode.cn/problems/longest-repeating-substring/) · Medium · 灵茶山艾府：[O(N) 后缀数组做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1062.最长重复子串

[力扣](https://leetcode.cn/problems/longest-repeating-substring/)

最长重复子串最经典的做法是利用后缀数组，求解出height数组后最终结果就是height数组中的最大值。

由于本题的数据规模不大，我在这里采用的是其他的做法。

对于两个长度a和b，不妨设a \< b。若字符串中存在长度为b的重复子串，那么也必然存在长度为a的重复子串。最简单的理解就是对于长度为b的两个重复子串，取其长度为a的前缀，就得到了两个长度为a的重复子串。这也就意味着最长重复子串的长度符合二分的性质，在这里可以二分最终的结果res，然后判断字符串中是否存在两个长度为res的子串是完全相同的。

对于判断是否存在定长的重复子串的问题，则可以一趟遍历，使用rk算法计算每个长度为res的子串的哈希值，然后利用哈希表来判断是否存在重复子串。rk算法的具体实现可以参考

[yiduobo：yiduobo的每日leetcode 2156.查找给定哈希值的子串](https://zhuanlan.zhihu.com/p/531523744)

最后附上python代码：

```python
class Solution(object):
    def longestRepeatingSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        left = 0
        right = n - 1

        mod = 10 ** 9 + 7

        def check(length):
            p = 1
            now = 0

            for char in s[:length]:
                now = (now * 26 + ord(char) - 97) % mod
                p = p * 26 % mod
            
            vis = set([now])
            for index, char in enumerate(s[length:]):
                now = (now * 26 - (ord(s[index]) - 97) * p % mod + mod + ord(char) - 97) % mod
                if now in vis:
                    return True
                vis.add(now)
            
            return False

        while left < right:
            mid = (left + right + 1) / 2
            if check(mid):
                left = mid
            else:
                right = mid - 1
        
        return left
```
