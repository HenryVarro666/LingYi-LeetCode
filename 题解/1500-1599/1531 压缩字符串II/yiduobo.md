---
title: "1531. 压缩字符串II"
aliases: ["yiduobo的每日leetcode 1531.压缩字符串II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/423383521"
zhihu_id: "423383521"
zhihu_title: "yiduobo的每日leetcode 1531.压缩字符串II"
question_id: "1531"
question: "压缩字符串II"
problem_url: "https://leetcode.cn/problems/string-compression-ii/"
created: "2021-10-19T23:54:55+08:00"
updated: "2021-10-19T23:54:55+08:00"
upvotes: 1
comments: 1
---

# 1531. 压缩字符串II

> **[yiduobo的每日leetcode 1531.压缩字符串II](https://zhuanlan.zhihu.com/p/423383521) · 知乎 · 2021-10-19 · 赞同 1**
> 力扣：[1531. 压缩字符串II](https://leetcode.cn/problems/string-compression-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1531.压缩字符串II

[力扣](https://leetcode-cn.com/problems/string-compression-ii/)

经典的动态规划问题，令f[i][j]表示s[0]到s[i]这些字符中，删去j个字符可以得到的最小压缩长度，那么对于f[i][j]：

1、当j >\= i + 1时，整个字符串都是可以全部删掉的，因此有f[i][j] \= 0

2、当j \< i + 1，且i \= 0时，此时的j也显然为0，于是有f[i][j] \= 1，即对于s[0]这个字符不进行任何操作

3、当j \< i + 1，且i > 0时：

3-1）此时可以选择删去s[i]，那么就有f[i][j] \= f[i - 1][j - 1]

3-1）此时也可以保留s[i]，那么这里可以考虑让s[i]与之前相同的字符进行压缩，这样的话就需要删去其中的某些字符。

可以明确的一点是，这里选取与s[i]相同的字符必然是从i开始向前连续选择的，因为若删去了其中位置p上与s[i]相同的字符s[p]，而选择与更靠前的位置q上与s[i]相同的字符s[q]进行合并，那么此时前者对应的转移方程应该是

f[i][j] \= min(f[i][j], f[p - 1][k1] + zip_cost(same_cnt))

而后者的转移方程则为

f[i][j] \= min(f[i][j], f[q - 1][k2] + zip_cost(same_cnt))

这里的zip_cost(same_cnt)是完全一致的，而对于f[p - 1][k1]以及f[q - 1][k2]而言，显然有

k2 \= k1 + p - q

这里p - q表示的是删去了p到q + 1这一段中的所有字符，包括s[p]

那么很容易的值f[p - 1][k1]的上界就是f[q - 1][k2]，因为对于f[p - 1][k1]而言，一种可行的处理方法就是将p - 1到q这些字符全部删去，这里字符的数目同样是p - q，也就相当于此时变成了f[q - 1][k2]，即f[p - 1][k1]的上界就是f[q - 1][k2]。

根据上面的结论，f[q - 1][k2] >\= f[p - 1][k1]，因此对于上面两种情况的转移方程而言，情况而是无需考虑的，也就是说对于与s[i]相同字符的选取必然是从后向前连续选取的。

因此可以首先一趟扫描进行预处理，得到每个字符上一次出现的位置，记为prev_pos，那么对于f[i][j]，从i开始向前迭代prev_pos，对于当前prev_pos对应的值pos，就有

f[i][j] \= min(f[i][j], f[pos - 1][i - pos - 1 - rnd] + zip_cost(rnd + 1))

其中rnd表示当前prev_pos迭代的轮次，而zip_cost则是合并若干字符的代价

动态规划完成后，f[n - 1][k]就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def getLengthOfOptimalCompression(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        n = len(s)
        prev_pos = [-1] * n
        last_pos = {}
        for index, char in enumerate(s):
            if char in last_pos:
                prev_pos[index] = last_pos[char]
            
            last_pos[char] = index
        
        f = [[n + 1] * (k + 1) for _ in range(n)]
        for i in range(n):
            for j in range(k + 1):
                if j >= i + 1:
                    f[i][j] = 0
                elif i == 0:
                    f[i][j] = 1
                else:
                    if j > 0:
                        f[i][j] = f[i - 1][j - 1]
                    
                    now = i
                    merge_cnt = 0
                    del_cnt = 0
                    while now != -1 and del_cnt <= j:
                        merge_cnt += 1
                        if merge_cnt == 1:
                            zip_len = 1
                        elif merge_cnt <= 9:
                            zip_len = 2
                        elif merge_cnt <= 99:
                            zip_len = 3
                        else:
                            zip_len = 4

                        if now == 0:
                            f[i][j] = min(f[i][j], zip_len)
                        else:
                            f[i][j] = min(f[i][j], f[now - 1][j - del_cnt] + zip_len)
                        
                        del_cnt += now - prev_pos[now] - 1
                        now = prev_pos[now]
        
        return f[-1][-1]
```
