---
title: "22. 括号生成"
aliases: ["yiduobo的每日leetcode 22.括号生成"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/链表-二叉树与回溯/四-回溯", "题单/LeetCode-热题-100/回溯", "题单/面试经典-150-题/回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/115647095"
zhihu_id: "115647095"
zhihu_title: "yiduobo的每日leetcode 22.括号生成"
question_id: "22"
question: "括号生成"
problem_url: "https://leetcode.cn/problems/generate-parentheses/"
difficulty: "Medium"
created: "2020-03-23T23:02:48+08:00"
updated: "2020-03-23T23:02:48+08:00"
upvotes: 0
comments: 0
---

# 22. 括号生成

> **[yiduobo的每日leetcode 22.括号生成](https://zhuanlan.zhihu.com/p/115647095) · 知乎 · 2020-03-23 · 赞同 0**
> 力扣：[22. 括号生成](https://leetcode.cn/problems/generate-parentheses/) · Medium · 灵茶山艾府：[两种基本回溯思想：选或不选 / 枚举选哪个（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

22.括号生成<https://leetcode-cn.com/problems/generate-parentheses/>

题目要求把所有情况都给打出来而不是给出结果的数量，因此只能老老实实用动态规划去做。

f[i]表示使用i组括号能形成的所有答案，那么对于f[i]，显然所有的答案都是左括号起头，可以写成 (xxx...xx)yyy...yy 的形式，且括号内的x和括号外的y都必须是合法的。

这样一来，就可以理解成第一个左括号形成的括号对将整个结果分成了两个部分，其中括号内的 x 对应 j 对括号，括号右侧的 y 对应 i - j - 1 对括号。枚举f[j]中的所有解left，以及f[i - j - 1]中的所有解right，此时的f[i]就可以写成 (left)right 的形式，当然 j 也可以等于0或i - 1，分别对应的就是left为空，或者right为空的情况，即 ()right 和 (left) 这两种情况。

对于所有的f[i]，我们只需要枚举j以及每一对left，right，然后按上面这种方式生成结果就行了。

注意边界条件，f[0]为空，f[1]为一对括号。

这里的时间复杂度不太好判断，除了外层的枚举i以及枚举j这两部操作为O(n^2)的复杂度之外，内部还需要枚举left和right，因此最终时间复杂度应该也跟解的数量挂钩。

最后附上python代码：

```python
class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        f = []
        f.append([''])
        f.append(['()'])

        for i in range(2, n + 1):
            now = []
            for j in range(i):
                for left in f[j]:
                    for right in f[i - j - 1]:
                        now.append('(' + left + ')' + right)
            f.append(now)

        return f[n]
```
