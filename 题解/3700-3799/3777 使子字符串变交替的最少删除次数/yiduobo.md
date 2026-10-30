---
title: "3777. 使子字符串变交替的最少删除次数"
aliases: ["yiduobo的每日leetcode 3777.使子字符串变交替的最少删除次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/segment-tree", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1984018223700648322"
zhihu_id: "1984018223700648322"
zhihu_title: "yiduobo的每日leetcode 3777.使子字符串变交替的最少删除次数"
question_id: "3777"
question: "使子字符串变交替的最少删除次数"
problem_url: "https://leetcode.cn/problems/minimum-deletions-to-make-alternating-substring/"
difficulty: "Hard"
rating: 2202
created: "2025-12-17T01:48:47+08:00"
updated: "2025-12-17T01:48:55+08:00"
upvotes: 2
comments: 0
---

# 3777. 使子字符串变交替的最少删除次数

> **[yiduobo的每日leetcode 3777.使子字符串变交替的最少删除次数](https://zhuanlan.zhihu.com/p/1984018223700648322) · 知乎 · 2025-12-17 · 赞同 2**
> 力扣：[3777. 使子字符串变交替的最少删除次数](https://leetcode.cn/problems/minimum-deletions-to-make-alternating-substring/) · Hard · 灵茶山艾府：[三种方法：线段树 / 树状数组 / 有序集合（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3777.使子字符串变交替的最少删除次数

[3777. 使子字符串变交替的最少删除次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-deletions-to-make-alternating-substring/description/)

题目给出一个长度为n的字符串s，其中仅包含字符'A'和'B'。

另外给出一个长度为q的二维整数数组queries，其中每个queries[index]是一下形式之一：

- [1, p]，表示反转s中下标为p的字符，记从'A'变为'B'，或者从'B'变为'A'。这个操作会修改s，并影响后续的所有查询。
- [2, left, right]，表示需要查询将s[left]到s[right]这个子串变为交替字符串所需的最小字符删除数。交替字符串指的是任意两个相邻字符都不同的字符串。长度为1的子字符串也被认为是交替字符串。这个操作不会修改s，s的长度保持为n。

首先可以明确的是，由于题目只允许通过删除操作来得到交替字符串，那么连续出现的相同字符是需要全部删掉的。例如AAABBB，如果考虑得到ABAB形式的子串，那么前面的两个A以及后面的两个B都应该删除掉。理由也很简单，如果前两个A想和右侧的某个B配对就必须要把后续连续的A全部删掉，那么还不如保留最后那个A，删掉前面的所有A，需要执行的删除次数是相同的。

基于以上的结论，就可以发现，问题实际上就是询问一组[left, right]之间，相邻的AB以及相邻的BA的数量是多少，尽量保留下这些字符对，然后删掉其他的字符就行了。

这是一个动态的区间次数查询问题，可以将其转化为前缀次数之差，利用树状数组来解决。不过需要特别注意的是，在这里需要特别处理跨越左边界的字符对。

例如AABABB以及一组查询[left, right]，当right为5，同时区间左边界在2或者4这两个位置时，这个左边界会与其左侧的A可以形成AB对。这一组AB对会被记录在以right为边界的前缀中，但是不会记录在以left为边界的前缀中，因此通过前缀之差计算时会将这一组AB算进去，但是实际上应该不予计算。

另外，对于以AB开头的子串，若区间的右边界对应的字符为A，那么就可以在之前ABABAB...的基础上再添加上这个额外的A，可以使得字符串的长度再加上1。同理，对于BA开头的子串，若区间右边界对应的字符为B，也可以将其添加到子串末尾。

值得一提的是，对于AB开头的子串，在这里只需要考虑右边界对应的字符是否为A这种情况。理由是如果区间右边界对应的是B，那么子串一定是以AB结尾的，因为如果存在单独添加的A，其右侧要么紧接着一个B，要么就是形如AA..AAAB...的形式，也就是说，这个A后续必然存在还没有计入到子串中的AB，因此在这里这个单独的A不应该单独存在。同理，对于BA开头的子串，也只需要考虑右边界对应的字符是否为B。

在具体实现上，可以将A和B先转化为0和1，这样一来就可以开一个n \* 2的树状数组，更新时可以直接通过数值计算出应该具体更新哪一棵。

最后附上python代码：

```python
class Solution(object):
    def minDeletions(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        n = len(s)
        b = [ord(c) - 65 for c in s]

        f = [[0] * (n + 1) for _ in range(2)]

        def add(x, delta, v):
            while x <= n:
                f[v][x] += delta
                x += x & -x
        
        def get(x, v):
            cnt = 0
            while x:
                cnt += f[v][x]
                x -= x & -x
            return cnt

        for index in range(1, n):
            if b[index] != b[index - 1]:
                add(index, 1, b[index - 1])

        res = []
        for q in queries:
            if q[0] == 2:
                left, right = q[1], q[2]
                
                ma = 0
                for v in range(2):
                    pair = get(right, v) - get(left, v)
                    if left > 0 and b[left - 1] == v and b[left] == 1 - v:
                        pair -= 1
                    length = pair + pair
                    if b[right] == v:
                        length += 1
                    ma = max(ma, length)

                res.append(right - left + 1 - ma)
            
            else:
                p = q[1]
                if p > 0:
                    if b[p - 1] != b[p]:
                        add(p, -1, b[p - 1])
                    else:
                        add(p, 1, b[p - 1])

                if p + 1 < n:
                    if b[p] != b[p + 1]:
                        add(p + 1, -1, b[p])
                    else:
                        add(p + 1, 1, 1 - b[p])
                
                b[p] ^= 1

        return res
```
