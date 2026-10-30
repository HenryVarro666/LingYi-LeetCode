---
title: "2060. 同源字符串检测"
aliases: ["yiduobo的每日leetcode 2060.同源字符串检测"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/memoization", "leetcode/string", "leetcode/dynamic-programming", "leetcode/dfs", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/514138371"
zhihu_id: "514138371"
zhihu_title: "yiduobo的每日leetcode 2060.同源字符串检测"
question_id: "2060"
question: "同源字符串检测"
problem_url: "https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/"
difficulty: "Hard"
rating: 2804
created: "2022-05-14T00:21:58+08:00"
updated: "2022-05-14T00:21:58+08:00"
upvotes: 1
comments: 0
---

# 2060. 同源字符串检测

> **[yiduobo的每日leetcode 2060.同源字符串检测](https://zhuanlan.zhihu.com/p/514138371) · 知乎 · 2022-05-14 · 赞同 1**
> 力扣：[2060. 同源字符串检测](https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/) · Hard · 灵茶山艾府：[DFS + 分类讨论](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2060.同源字符串检测

[力扣](https://leetcode.cn/problems/check-if-an-original-string-exists-given-two-encoded-strings/)

经典的字符串动态规划问题，令f[i][j][k]表示s1的前i个字符和s2的前j个字符进行匹配，s1比s2多出k个可用字符是否可能出现。

在这里状态表示可能有点问题，因为单个字符串的长度可以达到40，其中可能存在10组三位数，使得题目中的k可能达到10000左右的规模，那么最终状态数就有40 \* 40 \* 10000这么多了，时间复杂度明显是不行的。

不过本题的最终目的是让两个字符串完全匹配，也就是说k最终是奔着0去的，因此在某一时刻k大于等于0时，这些数字始终是要被s2中的字符匹配掉的，因此在这里没必要继续考虑往里面添加s1的字符，而是尝试添加s2中的字符。反过来，当k小于等于0时，只需要考虑添加s1的字符，无需考虑s2中的字符。

这样一来，k的规模就从10000左右缩减到了1000左右，时空复杂度都在勉强在可以承受的范围之内的。

接下来讨论具体的状态转移。设s1的长度为m，s2的长度为n，对于状态f[i][j][k]：

1、若k > 0：

1-1）此时可以尝试用s2中的单个字符补位。

当j \< n且s2[j]不是数字时，就有f[i][j + 1][k - 1] \= True

1-2）此时也可以尝试使用s2中的数值来补位。

由于题目中数字的长度最大为3，那么此时就需要分别尝试将s2中从j开始的1、2、3个字符转化为数字来使用，即s2[j]，s2[j] \* 10 + s2[j + 1]以及s2[j] \* 100 + s2[j + 1] \* 10 + s2[j]。当然，这里有两个前提是数字的选取必须没有越界，且这些字符都是数字。

对于通过s2[j]到s2[j + l - 1]得到的数值now，就有f[i][j + l][k - now] \= True

2、若k \< 0：

2-1）与情况1-1类似，可以使用s1中的单个字符补位。

当i \< m且s1[i]不是数字时，就有f[i + 1][j][k + 1] \= True

2-2）与情况1-2类似，可以使用s2中的数值来补位。

同样是枚举s1[i]到s1[i + l - 1]得到的数值now，就有f[i + l][j][k + now] \= True

3、若k \= 0，此时两个字符串处于完全匹配的状态，那么可以先从任意字符串中拿出一部分来更新后续的状态：

3-1）与情况1-2完全相同。

对于通过s2[j]到s2[j + l - 1]得到的数值now，就有f[i][j + l][-now] \= True

3-2）与情况2-2完全相同。

对于通过s1[i]到s1[i + l - 1]得到的数值now，就有f[i + l][j][now] \= True

3-3）除了上面两种情况，还可能出当前遍历到的都是字符的情况，此时必须要两个字符完全一致，才能继续向下匹配，因此当i \< m、j \< n且s1[i] \= s2[j]时，就有f[i + 1][j + 1][0] \= True

动态规划完成后，最终结果就是f[m][n][0]。在具体实现上，由于在这里实际上覆盖不到-1000到1000中的所有情况，因此在这里可以使用f[i][j]储存一个set的形式，表示前s1中的前i个字符与s2中的前j个字符匹配的所有情况，最终只需要检测0是否出现在f[m][n]之内就行了。

最后附上python代码：

```python
class Solution(object):
    def possiblyEquals(self, s1, s2):
        """
        :type s1: str
        :type s2: str
        :rtype: bool
        """

        m = len(s1)
        n = len(s2)
        f = [[set() for _ in range(n + 1)] for _ in range(m + 1)]
        f[0][0].add(0)

        for i in range(m + 1):
            for j in range(n + 1):
                for k in f[i][j]:
                    if k > 0:
                        p = j
                        now = 0
                        while p < n and p < j + 3 and s2[p] >= '1' and s2[p] <= '9':
                            now = now * 10 + int(s2[p])
                            f[i][p + 1].add(k - now)
                            p += 1
                    
                        if j < n and (s2[j] < '1' or s2[j] > '9'):
                            f[i][j + 1].add(k - 1)

                    elif k < 0:
                        p = i
                        now = 0
                        while p < m and p < i + 3 and s1[p] >= '1' and s1[p] <= '9':
                            now = now * 10 + int(s1[p])
                            f[p + 1][j].add(k + now)
                            p += 1
                        
                        if i < m and (s1[i] < '1' or s1[i] > '9'):
                            f[i + 1][j].add(k + 1)
                    
                    else:
                        if i < m and j < n and s1[i] == s2[j] and k == 0:
                            f[i + 1][j + 1].add(0)
                        
                        p = i
                        now = 0
                        while p < m and p < i + 3 and s1[p] >= '1' and s1[p] <= '9':
                            now = now * 10 + int(s1[p])
                            f[p + 1][j].add(now)
                            p += 1
                        
                        p = j
                        now = 0
                        while p < n and p < j + 3 and s2[p] >= '1' and s2[p] <= '9':
                            now = now * 10 + int(s2[p])
                            f[i][p + 1].add(-now)
                            p += 1

        return 0 in f[m][n]
```
