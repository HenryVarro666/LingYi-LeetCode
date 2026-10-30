---
title: "2002. 两个回文子序列长度的最大乘积"
aliases: ["yiduobo的每日leetcode 2002.两个回文子序列长度的最大乘积"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/backtracking", "leetcode/search", "leetcode/bao-li", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/502749099"
zhihu_id: "502749099"
zhihu_title: "yiduobo的每日leetcode 2002.两个回文子序列长度的最大乘积"
question_id: "2002"
question: "两个回文子序列长度的最大乘积"
problem_url: "https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/"
difficulty: "Medium"
rating: 1869
created: "2022-04-21T22:34:58+08:00"
updated: "2022-04-21T22:34:58+08:00"
upvotes: 0
comments: 0
---

# 2002. 两个回文子序列长度的最大乘积

> **[yiduobo的每日leetcode 2002.两个回文子序列长度的最大乘积](https://zhuanlan.zhihu.com/p/502749099) · 知乎 · 2022-04-21 · 赞同 0**
> 力扣：[2002. 两个回文子序列长度的最大乘积](https://leetcode.cn/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/) · Medium · 灵茶山艾府：[Go 暴搜](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2002.两个回文子序列长度的最大乘积

[力扣](https://leetcode-cn.com/problems/maximum-product-of-the-length-of-two-palindromic-subsequences/)

注意到字符串的长度n非常小，那么完全可以找出所有的将字符划分成两个部分的划分方式。由于n最大是12，那么最多也只有4096种不同的划分方式。对于每种方式都找出两个部分中最长的回文子序列，然后用二者的乘积更新答案即可。

对于字符的划分，使用常规的dfs即可。对于各个部分中的最长回文子序列，由于规模很小，使用暴力法或者动态规划都可以。

最后附上python代码：

```python
class Solution(object):
    def maxProduct(self, s):
        """
        :type s: str
        :rtype: int
        """

        self.res = 0
        self.dfs(0, [], [], s)
        return self.res

    def dfs(self, now, part1, part2, s):
        if now == len(s):
            self.res = max(self.res, self.dp(part1) * self.dp(part2))
            return
        
        part1.append(s[now])
        self.dfs(now + 1, part1, part2, s)
        part1.pop()

        part2.append(s[now])
        self.dfs(now + 1, part1, part2, s)
        part2.pop()
    
    def dp(self, s):
        n = len(s)
        if n == 0:
            return 0
        f = [[0] * n for _ in range(n)]
        for l in range(1, n + 1):
            for left in range(n - l + 1):
                right = left + l - 1
                if left == right:
                    f[left][right] = 1
                elif s[left] == s[right]:
                    f[left][right] = f[left + 1][right - 1] + 2
                else:
                    f[left][right] = max(f[left + 1][right], f[left][right - 1])
        
        return f[0][n - 1]
```
