---
title: "839. 相似字符串组"
aliases: ["yiduobo的每日leetcode 839.相似字符串组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/346828254"
zhihu_id: "346828254"
zhihu_title: "yiduobo的每日leetcode 839.相似字符串组"
question_id: "839"
question: "相似字符串组"
problem_url: "https://leetcode.cn/problems/similar-string-groups/"
created: "2021-01-26T12:07:22+08:00"
updated: "2021-01-26T12:07:22+08:00"
upvotes: 0
comments: 0
---

# 839. 相似字符串组

> **[yiduobo的每日leetcode 839.相似字符串组](https://zhuanlan.zhihu.com/p/346828254) · 知乎 · 2021-01-26 · 赞同 0**
> 力扣：[839. 相似字符串组](https://leetcode.cn/problems/similar-string-groups/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

839.相似字符串组

[力扣](https://leetcode-cn.com/problems/similar-string-groups/)

感觉没有什么太好的思路，好在这里字符串的数量和长度都比较小，且所有字符串都是字母异位词。这意味着若两个字符串中有不超过两个位置上的字符不同，那么这两个字符串就是相似的。基于这一点，直接两两枚举所有的字符串，若两个字符串相似，那么使用并查集来进行合并。对比完成后，检查有多少字符串的最终父亲是其自身，这个数目即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def numSimilarGroups(self, strs):
        """
        :type strs: List[str]
        :rtype: int
        """

        n = len(strs)
        m = len(strs[0])
        fa = [x for x in range(n)]
        for i in range(n - 1):
            for j in range(i + 1, n):
                cnt = 0
                for index in range(m):
                    if strs[i][index] != strs[j][index]:
                        cnt += 1
                        if cnt > 2:
                            break
                if cnt <= 2:
                    fa_i = self.find(i, fa)
                    fa_j = self.find(j, fa)
                    if fa_i < fa_j:
                        fa[fa_j] = fa_i
                    else:
                        fa[fa_i] = fa_j
        
        res = 0
        for index in range(n):
            if self.find(index, fa) == index:
                res += 1
        
        return res

    def find(self, now, fa):
        if fa[now] != now:
            tmp = self.find(fa[now], fa)
            fa[now] = tmp
        return fa[now]
```
