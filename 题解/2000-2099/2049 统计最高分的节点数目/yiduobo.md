---
title: "2049. 统计最高分的节点数目"
aliases: ["yiduobo的每日leetcode 2049.统计最高分的节点数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/binary-tree", "leetcode/dfs", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/511856451"
zhihu_id: "511856451"
zhihu_title: "yiduobo的每日leetcode 2049.统计最高分的节点数目"
question_id: "2049"
question: "统计最高分的节点数目"
problem_url: "https://leetcode.cn/problems/count-nodes-with-the-highest-score/"
difficulty: "Medium"
rating: 1912
created: "2022-05-10T00:11:29+08:00"
updated: "2022-05-10T00:11:30+08:00"
upvotes: 1
comments: 0
---

# 2049. 统计最高分的节点数目

> **[yiduobo的每日leetcode 2049.统计最高分的节点数目](https://zhuanlan.zhihu.com/p/511856451) · 知乎 · 2022-05-10 · 赞同 1**
> 力扣：[2049. 统计最高分的节点数目](https://leetcode.cn/problems/count-nodes-with-the-highest-score/) · Medium · 灵茶山艾府：[DFS 的同时计算分数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2049.统计最高分的节点数目

[力扣](https://leetcode.cn/problems/count-nodes-with-the-highest-score/)

对于二叉树中的节点，将其从树中去除掉之后，可能会剩下三个非空的子树，分别是该节点的左子树、右子树，以及剩余的其他节点构成的以整棵树原始根节点为根节点的子树。当然，在这里去除的节点可能没有左孩子或者右孩子，那么对应的左子树和右子树自然为空。另外，除了整棵树的原始根节点外，去除其他任意节点都会有上面提到的剩余的其他节点构成的子树。

题目中对于树的大小的定义是子树内节点的数目，设原始树中总共有n个节点，那么可以从根节点开始向下进行dfs，对于当前处理的节点now：

1、若now没有左孩子和右孩子，那么以now为根节点的子树的大小就是1，同时去除now之后其他剩下的所有n - 1个节点构成了一颗子树，因此可以得到去除now的分数为n - 1

2、若now有孩子，那么先递归求解now的孩子节点，同时统计对应子树的大小，那么以now为根节点的子树大小就是其子树的大小之和再加上1，记为cnt。去除now之后，除了now的左右子树之外，其他剩余的节点数目就是n - cnt，因此可以使用左右子树的大小以及now - cnt计算得到去除now的分数

这样一来，就可以通过一趟dfs求出去除所有节点后的得分了。在求解过程中顺便更新最大得分以及最终答案。

最后附上python代码：

```python
class Solution(object):
    def countHighestScoreNodes(self, parents):
        """
        :type parents: List[int]
        :rtype: int
        """

        n = len(parents)
        self.max_score = 0
        self.res = 0

        childs = {}
        for index in range(1, n):
            fa = parents[index]
            if fa not in childs:
                childs[fa] = set()
            childs[fa].add(index)

        self.dfs(0, childs, n)
        return self.res

    def dfs(self, now, childs, n):
        if now not in childs:
            cnt = 1
            score = n - 1
        else:
            cnt = 1
            score = 1
            for child in childs[now]:
                child_cnt = self.dfs(child, childs, n)
                cnt += child_cnt
                score *= child_cnt
        
            if n != cnt:
                score *= (n - cnt)
        
        if score > self.max_score:
            self.res = 1
            self.max_score = score
        elif score == self.max_score:
            self.res += 1

        return cnt
```
