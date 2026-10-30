---
title: "1361. 验证二叉树"
aliases: ["yiduobo的每日leetcode 1361.验证二叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/399568239"
zhihu_id: "399568239"
zhihu_title: "yiduobo的每日leetcode 1361.验证二叉树"
question_id: "1361"
question: "验证二叉树"
problem_url: "https://leetcode.cn/problems/validate-binary-tree-nodes/"
created: "2021-08-13T21:12:40+08:00"
updated: "2021-08-13T21:12:40+08:00"
upvotes: 1
comments: 0
---

# 1361. 验证二叉树

> **[yiduobo的每日leetcode 1361.验证二叉树](https://zhuanlan.zhihu.com/p/399568239) · 知乎 · 2021-08-13 · 赞同 1**
> 力扣：[1361. 验证二叉树](https://leetcode.cn/problems/validate-binary-tree-nodes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1361.验证二叉树

[力扣](https://leetcode-cn.com/problems/validate-binary-tree-nodes/)

一颗n个节点的树中，这n个节点必须互相连通，且其中有一个节点的入度为0，其他n - 1个节点的入度都为1。

对于以上条件，度数可以直接遍历所有的边统计出来，另外还需要想办法判断是否连通。不判断连通的话可能出现一颗合法二叉树加一个环这种组合。

我在这里的做法是首先找出根节点，然后从根据点开始进行bfs。若中途某个节点已经被访问过，那么答案为false。若bfs完成后bfs队列的长度不为n，说明不满足连通性，同样返回false。

最后附上python代码：

```python
class Solution(object):
    def validateBinaryTreeNodes(self, n, leftChild, rightChild):
        """
        :type n: int
        :type leftChild: List[int]
        :type rightChild: List[int]
        :rtype: bool
        """

        child_set = set()
        for child in leftChild:
            child_set.add(child)
        for child in rightChild:
            child_set.add(child)
        
        root = None
        for index in range(n):
            if index not in child_set:
                if root is None:
                    root = index
                else:
                    return False
        
        if root is None:
            return False

        q = [root]
        l = 0
        r = 1
        used = [False] * n
        used[root] = True
        while l < r:
            now = q[l]
            l += 1
            if leftChild[now] != -1:
                if used[leftChild[now]]:
                    return False
                used[leftChild[now]] = True
                q.append(leftChild[now])
                r += 1
            if rightChild[now] != -1:
                if used[rightChild[now]]:
                    return False
                used[rightChild[now]] = True
                q.append(rightChild[now])
                r += 1

        return len(q) == n
```
