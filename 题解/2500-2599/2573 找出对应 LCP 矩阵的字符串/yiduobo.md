---
title: "2573. 找出对应LCP矩阵的字符串"
aliases: ["yiduobo的每日leetcode 2573.找出对应LCP矩阵的字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/dynamic-programming", "题单/贪心算法", "题单/字符串", "题单/贪心算法/六-构造题", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/641762146"
zhihu_id: "641762146"
zhihu_title: "yiduobo的每日leetcode 2573.找出对应LCP矩阵的字符串"
question_id: "2573"
question: "找出对应 LCP 矩阵的字符串"
problem_url: "https://leetcode.cn/problems/find-the-string-with-lcp/"
difficulty: "Hard"
rating: 2682
created: "2023-07-06T01:18:26+08:00"
updated: "2023-07-06T01:18:26+08:00"
upvotes: 0
comments: 0
---

# 2573. 找出对应LCP矩阵的字符串

> **[yiduobo的每日leetcode 2573.找出对应LCP矩阵的字符串](https://zhuanlan.zhihu.com/p/641762146) · 知乎 · 2023-07-06 · 赞同 0**
> 力扣：[2573. 找出对应 LCP 矩阵的字符串](https://leetcode.cn/problems/find-the-string-with-lcp/) · Hard · 灵茶山艾府：[[灵茶山艾府题解/solutions/2573 找出对应 LCP 矩阵的字符串 · 从 s-0- 开始思考，带你破解这道题！（Python-Java-C++-C-Go-JS-Rust）|从 s[0] 开始思考，带你破解这道题！（Python/Java/C++/C/Go/JS/Rust）]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2573.找出对应LCP矩阵的字符串

[力扣](https://leetcode.cn/problems/find-the-string-with-lcp/)

首先不妨先对一些特殊情况进行讨论。

1、对于lcp[i][i]而言，实际上是从i开始的后缀与其自身进行对比，因此lcp[i][i]必然等于这个后缀的长度，也就是n - i，若不等于，则可以直接返回空字符串。

2、对于lcp[i][j]和lcp[j][i]，对比的是相同的两个后缀，因此必然有lcp[i][j] \= lcp[j][i]。若出现了不等于的情况，则可以直接返回空字符串。另一方面，后续的检测中就只需要检测所有i \< j的lcp[i][j]是否合法即可。

3、对于i \< j的lcp[i][j]，其最长的长度只能是以j开头的后缀的长度，也就是n - j。那么若某个lcp[i][j] > n - j，则可以直接返回空字符串。

4、对于i \< j且j \< n - 1的lcp[i][j]，若其大于1，那么必然有lcp[i][j] \= lcp[i + 1][j + 1] + 1，也就是以i开头的后缀与以j开头的后缀都去掉首字符，就是lcp[i + 1][j + 1]，其最长公共前缀的长度就应该是lcp[i][j]减去1。若不满足，则可以直接返回空字符串。另一方面，这也意味着对于每个非0的lcp[i][j]，只需要为word[i]和word[j]建立相等关系，而无需考虑后续的字符，因为这些字符会在遍历lcp[i + 1][j + 1]、lcp[i + 2][j + 2]等其他的后续lcp数组值时被考虑到。

除了上述的几种情况之外，根据情况4中关于lcp[i][j]为word[i]和word[j]点到点建立相等关系的处理方法，很容想到使用并查集来维护字符相等的下标位置。那么对于一组lcp[i][j] \= 0，若i和j属于同一个连通块，说明其通过其他lcp值建立起了相等关系，此时的lcp[i][j]就不能等于0，于是可以直接返回空字符串。

需要特别注意的是，对于0的检测必须在所有非0的lcp都处理完之后才能进行，因为如果先处理0的话可能当前的i和j也可能通过之后遍历到的其他非0的中间lcp建立相等关系。

最后，由于只有26个字符可用，那么若存在超过26个连通块，说明同样无解，也是返回空字符串，否则就按照下标的先后顺序依次选择a到z作为连通块对应的字符，并生成最终答案。

最后附上python代码：

```python
class Solution(object):
    def findTheString(self, lcp):
        """
        :type lcp: List[List[int]]
        :rtype: str
        """

        n = len(lcp)
        fa = range(n)

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        check_list = []
        for i in range(n):
            for j in range(n):
                if i == j:
                    if lcp[i][j] != n - i:
                        return ""
                    continue
                
                if j < i:
                    if lcp[i][j] != lcp[j][i]:
                        return ""
                    continue
                
                if lcp[i][j] == 0:
                    check_list.append([i, j])
                else:
                    if j + 1 < n and lcp[i][j] - 1 != lcp[i + 1][j + 1]:
                        return ""

                    if lcp[i][j] > n - j:
                        return ""

                    fa_i = find(i)
                    fa_j = find(j)
                
                    if fa_i < fa_j:
                        fa[fa_j] = fa_i
                    else:
                        fa[fa_i] = fa_j

        for i, j in check_list:
            if find(i) == find(j):
                return ""

        res = []
        now = 0
        mapping = {}
        for i in range(n):
            if find(i) == i:
                if now < 26:
                    mapping[i] = chr(now + 97)
                    now += 1
                else:
                    return ""
            
            res.append(mapping[fa[i]])
        
        return ''.join(res)
```
