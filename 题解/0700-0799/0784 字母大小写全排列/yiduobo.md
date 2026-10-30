---
title: "784. 字母大小写全排列"
aliases: ["yiduobo的每日leetcode 784.字母大小写全排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/340764441"
zhihu_id: "340764441"
zhihu_title: "yiduobo的每日leetcode 784.字母大小写全排列"
question_id: "784"
question: "字母大小写全排列"
problem_url: "https://leetcode.cn/problems/letter-case-permutation/"
created: "2020-12-31T00:00:41+08:00"
updated: "2020-12-31T00:00:41+08:00"
upvotes: 0
comments: 0
---

# 784. 字母大小写全排列

> **[yiduobo的每日leetcode 784.字母大小写全排列](https://zhuanlan.zhihu.com/p/340764441) · 知乎 · 2020-12-31 · 赞同 0**
> 力扣：[784. 字母大小写全排列](https://leetcode.cn/problems/letter-case-permutation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

这里直接跳过了783题，因为783题与之前做过的530题是一样的题目。具体解法可以参考

[yiduobo：yiduobo的每日leetcode 530.二叉搜索树的最小绝对差](https://zhuanlan.zhihu.com/p/261167895)

784.字母大小写全排列

[力扣](https://leetcode-cn.com/problems/letter-case-permutation/)

可以使用传统的dfs，也可以利用python强悍的生成方法来处理。我在这里还是用的传统的dfs和回溯。dfs的过程比较简单，就是从头开始往后逐位进行，首先对当前字符执行一次，然后若当前字符为小写字符，则需要对当前字符的大写版本执行一次；若当前字符为大写字符，则需要对当前字符的小写版本执行一次。

最后附上python代码：

```python
class Solution(object):
    def letterCasePermutation(self, S):
        """
        :type S: str
        :rtype: List[str]
        """

        self.res = []

        l = len(S)
        self.dfs(S, 0, [], l)
        return [''.join(x) for x in self.res]

    def dfs(self, s, depth, now, l):
        if depth == l:
            self.res.append(now[:])
            return

        now.append(s[depth])
        self.dfs(s, depth + 1, now, l)
        if ord(s[depth]) >= 97:
            now[-1] = chr(ord(s[depth]) - 32)
            self.dfs(s, depth + 1, now, l)
        elif ord(s[depth]) >= 65:
            now[-1] = chr(ord(s[depth]) + 32)
            self.dfs(s, depth + 1, now, l)
        now.pop()
```
