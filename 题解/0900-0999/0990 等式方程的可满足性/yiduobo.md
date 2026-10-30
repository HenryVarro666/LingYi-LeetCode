---
title: "990. 等式方程的可满足性"
aliases: ["yiduobo的每日leetcode 990.等式方程的可满足性"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/364617717"
zhihu_id: "364617717"
zhihu_title: "yiduobo的每日leetcode 990.等式方程的可满足性"
question_id: "990"
question: "等式方程的可满足性"
problem_url: "https://leetcode.cn/problems/satisfiability-of-equality-equations/"
created: "2021-04-13T22:10:04+08:00"
updated: "2021-04-13T22:10:04+08:00"
upvotes: 0
comments: 0
---

# 990. 等式方程的可满足性

> **[yiduobo的每日leetcode 990.等式方程的可满足性](https://zhuanlan.zhihu.com/p/364617717) · 知乎 · 2021-04-13 · 赞同 0**
> 力扣：[990. 等式方程的可满足性](https://leetcode.cn/problems/satisfiability-of-equality-equations/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

990.等式方程的可满足性

[力扣](https://leetcode-cn.com/problems/satisfiability-of-equality-equations/)

对于等式和不等式，首先可以明确的一点是等式可以传递但是不等式不行，例如我们可以通过a\=b和b\=c推导出a\=c，但是不能通过a!\=b和b!\=c推导出a!\=c。

那么对于本题，我们应该利用等式的传递性，优先处理所有等式，获取到哪些变量是相等的。这一步可以通过并查集来做。

接下来，遍历所有的不等式，若当前不等式两侧的遍历在并查集中的父亲是同一个，说明二者是相等的，此时直接返回false。若能成功遍历完所有不等式，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def equationsPossible(self, equations):
        """
        :type equations: List[str]
        :rtype: bool
        """

        fa = range(26)
        check_pair = []
        for equation in equations:
            x = ord(equation[0]) - 97
            y = ord(equation[3]) - 97
            if equation[1] == '=':
                self.union(x, y, fa)
            else:
                check_pair.append([x, y])
        
        for x, y in check_pair:
            if self.find(x, fa) == self.find(y, fa):
                return False

        return True

    def find(self, x, fa):
        if x != fa[x]:
            fa[x] = self.find(fa[x], fa)
        
        return fa[x]
    
    def union(self, x, y, fa):
        fa_x = self.find(x, fa)
        fa_y = self.find(y, fa)
        if fa_x < fa_y:
            fa[fa_y] = fa_x
        else:
            fa[fa_x] = fa_y
```
