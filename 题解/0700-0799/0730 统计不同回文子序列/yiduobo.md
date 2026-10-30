---
title: "730. 统计不同回文子序列"
aliases: ["yiduobo的每日leetcode 730.统计不同回文子序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/335830644"
zhihu_id: "335830644"
zhihu_title: "yiduobo的每日leetcode 730.统计不同回文子序列"
question_id: "730"
question: "统计不同回文子序列"
problem_url: "https://leetcode.cn/problems/count-different-palindromic-subsequences/"
created: "2020-12-10T23:03:45+08:00"
updated: "2020-12-10T23:03:45+08:00"
upvotes: 0
comments: 0
---

# 730. 统计不同回文子序列

> **[yiduobo的每日leetcode 730.统计不同回文子序列](https://zhuanlan.zhihu.com/p/335830644) · 知乎 · 2020-12-10 · 赞同 0**
> 力扣：[730. 统计不同回文子序列](https://leetcode.cn/problems/count-different-palindromic-subsequences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

730.统计不同回文子序列

[力扣](https://leetcode-cn.com/problems/count-different-palindromic-subsequences/)

拿到题目第一时间就想到使用经典的两侧状态表示的动态规划。设f[l][r]表示s中l到r这一段可以形成多少组回文子序列，那么此时最大的问题就是如何去重。

对于形如X.....X.....X的字符串，若某个回文子序列以中间的X为边界，其必然会与以两侧的X为边界的某个回文串重复。

例如abaca，我们去除第一个a和b得到aca，去除c和第三个a得到aba。但是我们如果去除b和第二个a，同样可以得到aca，去除第二个a和c，同样可以得到aba。

这说明，对于所有形如X...X...X的字符串，中间的这个X不能作为当前字符串的回文子序列的端点，反过来，我们就可以枚举当前区间最左边和最右边的a、b、c、d分别在哪里，组合之后形成端点，然后递归求解子区间。

具体来说，对于f[l][r]，方便起见我们认为空字符为合法的回文子序列，那么：

1、若l > r，此时有f[l][r] \= 1，表示空字符串

2、若l \= r，此时有f[l][r] \= 2，表示当前字符本身，以及空字符

3、其他情况下，我们一次枚举a、b、c、d在l到r之间的最左位置以及最右位置，记为next_pos以及prev_pos。

若next_pos不为空，那么我们将f[l][r]加上1，表示直接选择next_pos上的这个字符作为一个回文子序列。

若next_pos和prev_pos都不为空，那么我们可以将next_pos以及prev_pos上的字符作为回文子序列的两端，然后递归求解在next_pos + 1到prev_pos - 1之间的回文子序列，与两端进行组，于是有f[l][r] +\= f[next_pos + 1][prev_pos - 1]。

求解完f[0][n - 1]后，由于我们额外计算了一次空字符，因此最终答案应该是f[0][n - 1] - 1。

另外，由于字符串是固定的，因此我们可以通过一趟正向的扫描以及一趟反向的扫描，预先求出每个位置，从该位置开始往前的第一个a、b、c、d以及从该位置开始往后的第一个a、b、c、d的下标，从而在动态规划的过程中可以高效得到next_pos以及prev_pos。

最后，还有一个小细节是，由于题目要求答案模上10^9 + 7，那么若最终的f[0][n - 1]取模之后为0，那么答案应该是10^9 + 6而不是-1。

最后附上python代码：

```python
class Solution(object):
    def countPalindromicSubsequences(self, S):
        """
        :type S: str
        :rtype: int
        """

        mod = 10 ** 9 + 7
        n = len(S)

        pos_dict = {}
        prev_pos_list = []
        for index in range(n):
            pos_dict[S[index]] = index
            prev_pos_list.append(pos_dict.copy())
        
        pos_dict = {}
        next_pos_list = []
        for index in range(n - 1, -1, -1):
            pos_dict[S[index]] = index
            next_pos_list.append(pos_dict.copy())
        next_pos_list.reverse()
        
        f = [[None] * n for _ in range(n)]

        res = self.dfs(0, n - 1, f, next_pos_list, prev_pos_list, mod)
        if res == 0:
            return mod - 1
        else:
            return res - 1
        
    
    def dfs(self, l, r, f, next_pos_list, prev_pos_list, mod):
        if l > r:
            return 1
        if l == r:
            return 2

        if f[l][r] is None:
            f[l][r] = 1
            for char in ['a', 'b', 'c', 'd']:
                next_pos = next_pos_list[l].get(char, None)
                prev_pos = prev_pos_list[r].get(char, None)
                if next_pos is not None and l <= next_pos and next_pos <= r:
                    f[l][r] += 1
                if next_pos is not None and next_pos < prev_pos:
                    f[l][r] += self.dfs(next_pos + 1, prev_pos - 1, f, next_pos_list, prev_pos_list, mod)
                f[l][r] %= mod

        return f[l][r]
```
