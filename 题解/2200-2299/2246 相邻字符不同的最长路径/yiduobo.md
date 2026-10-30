---
title: "2246. 相邻字符不同的最长路径"
aliases: ["yiduobo的每日leetcode 2246.相邻字符不同的最长路径"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/dynamic-programming", "leetcode/dfs", "leetcode/dp-on-trees", "leetcode/dp", "leetcode/dp-2", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/三-一般树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/546098623"
zhihu_id: "546098623"
zhihu_title: "yiduobo的每日leetcode 2246.相邻字符不同的最长路径"
question_id: "2246"
question: "相邻字符不同的最长路径"
problem_url: "https://leetcode.cn/problems/longest-path-with-different-adjacent-characters/"
difficulty: "Hard"
rating: 2126
created: "2022-07-26T01:50:42+08:00"
updated: "2022-07-26T01:50:42+08:00"
upvotes: 1
comments: 0
---

# 2246. 相邻字符不同的最长路径

> **[yiduobo的每日leetcode 2246.相邻字符不同的最长路径](https://zhuanlan.zhihu.com/p/546098623) · 知乎 · 2022-07-26 · 赞同 1**
> 力扣：[2246. 相邻字符不同的最长路径](https://leetcode.cn/problems/longest-path-with-different-adjacent-characters/) · Hard · 灵茶山艾府：[经典题：树的直径（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2246.相邻字符不同的最长路径

[力扣](https://leetcode.cn/problems/longest-path-with-different-adjacent-characters/)

对于以节点root为根节点的子树来说，这颗数中的最长路径可能有两种情况。第一种是出现在更深的子树当中，通常的做法是递归求解。另一种则是由至多两条以root某个孩子为端点的树链，与root拼接起来形成的路径。题目中有相邻字符不同的要求，因此这里的某个孩子必须与root不同才能使用这条树链。

根据上面的结论，在递归的过程中需要求出两个值，分别为当前子树中最长的合法路径的长度res，以及当前子树根节点作为其中一端的最长树链长度chain。

接下来从0号结点开始递归。对于当前节点now：

1、首先考虑边界情况。若now是一个叶子节点，那么其对应的res和chain都是1

2、接下来是一般情况。此时应该先遍历now的所有孩子节点，设当前遍历到child：

2-1）首先递归求解child，得到以child为根节点的子树对应的res和chain，分别记为r和c。

2-2）使用r来更新答案res

2-3）若child.val与now.val不同，那么就可能通过以child为端点的树链拼接出新的合法路径。现有的最长合法树链的长度为chain，那么拼接后就是chain + c，需要用这个值来更新答案。另外，还需要使用c + 1来更新chain。这里的加1表示将now纳入到树链当中

递归结束后，整棵树的res就是最终答案了。

最后附上python代码：

```python
class Solution(object):
    def longestPath(self, parent, s):
        """
        :type parent: List[int]
        :type s: str
        :rtype: int
        """

        childs = {}
        for index, p in enumerate(parent):
            if index > 0:
                if p not in childs:
                    childs[p] = set()
                childs[p].add(index)

        def dfs(now):
            res = 1
            chain = 1

            for child in childs.get(now, set()):
                r, c = dfs(child)
                res = max(res, r)
                if s[now] != s[child]:
                    res = max(res, chain + c)
                    chain = max(chain, c + 1)

            return res, chain
        
        return dfs(0)[0]
```
