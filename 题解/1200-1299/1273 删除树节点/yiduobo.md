---
title: "1273. 删除树节点"
aliases: ["yiduobo的每日leetcode 1273.删除树节点"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615598598"
zhihu_id: "615598598"
zhihu_title: "yiduobo的每日leetcode 1273.删除树节点"
question_id: "1273"
question: "删除树节点"
problem_url: "https://leetcode.cn/problems/delete-tree-nodes/"
created: "2023-03-20T22:24:28+08:00"
updated: "2023-03-20T22:24:29+08:00"
upvotes: 0
comments: 0
---

# 1273. 删除树节点

> **[yiduobo的每日leetcode 1273.删除树节点](https://zhuanlan.zhihu.com/p/615598598) · 知乎 · 2023-03-20 · 赞同 0**
> 力扣：[1273. 删除树节点](https://leetcode.cn/problems/delete-tree-nodes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1273.删除树节点

[力扣](https://leetcode.cn/problems/delete-tree-nodes/)

对于树中的某个节点node，若以其某个祖先节点asc为根节点的子树中的节点值之和为0，那么此时只需删除掉以asc为根节点的子树，无需再考虑这颗子树中的具体内容。换言之，本题就应该从根节点向下进行层序遍历，将上层的节点值之和为0的子树删除，对于删除的子树则无需继续往下进行遍历。

到了这里，问题就变成了计算子树中节点值之和。对于这个问题，则可以从根节点向下递归求解。对于当前处理到的节点now，先递归求解now的所有子树中的节点值之和，将这些和累加起来，再加上now自身的值，就是以now为根节点的子树节点值之和了。

到了这里，就得到了一种做法：

1、遍历parent数组，完成建树并找出树的根节点root

2、从root开始向下递归求解以树中每个节点为根节点的子树节点值之和

3、从root开始向下层序遍历，只遍历子树节点值之和不为0的节点

最终层序遍历队列的长度即为最终答案。需要特别注意的是，上面算法没有考虑到整颗数节点值之和为0的情况，在这种情况下不需要执行步骤3，直接返回0即可。

最后附上python代码：

```python
class Solution(object):
    def deleteTreeNodes(self, nodes, parent, value):
        """
        :type nodes: int
        :type parent: List[int]
        :type value: List[int]
        :rtype: int
        """

        childs = {index : set() for index in range(nodes)}
        for index, fa in enumerate(parent):
            if fa == -1:
                root = index
            else:
                childs[fa].add(index)
        
        f = [0] * nodes

        def dfs(now):
            f[now] = value[now]
            for c in childs[now]:
                dfs(c)
                f[now] += f[c]

        dfs(root)
        
        if f[root] == 0:
            return 0
        
        q = [root]
        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for c in childs[now]:
                if f[c] != 0:
                    q.append(c)
                    tail += 1
        
        return len(q)
```
