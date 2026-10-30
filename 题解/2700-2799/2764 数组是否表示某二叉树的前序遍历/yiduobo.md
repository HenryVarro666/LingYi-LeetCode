---
title: "2764. 数组是否表示某二叉树的前序遍历"
aliases: ["yiduobo的每日leetcode 2764.数组是否表示某二叉树的前序遍历"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/654763469"
zhihu_id: "654763469"
zhihu_title: "yiduobo的每日leetcode 2764.数组是否表示某二叉树的前序遍历"
question_id: "2764"
question: "数组是否表示某二叉树的前序遍历"
problem_url: "https://leetcode.cn/problems/is-array-a-preorder-of-some-binary-tree/"
created: "2023-09-07T05:23:29+08:00"
updated: "2023-09-07T05:23:29+08:00"
upvotes: 0
comments: 0
---

# 2764. 数组是否表示某二叉树的前序遍历

> **[yiduobo的每日leetcode 2764.数组是否表示某二叉树的前序遍历](https://zhuanlan.zhihu.com/p/654763469) · 知乎 · 2023-09-07 · 赞同 0**
> 力扣：[2764. 数组是否表示某二叉树的前序遍历](https://leetcode.cn/problems/is-array-a-preorder-of-some-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2764.数组是否表示某二叉树的前序遍历

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/is-array-a-preorder-of-some-binary-tree/)

前序遍历是按照根-左-右的顺序进行，恰好能与标准的搜索回溯完全对应上，也就是说题目相当于给出了dfs序，那么只需使用一个栈模拟搜索回溯的过程。

初始情况下，栈中只有树的根节点node[0][0]，接下来从下标1开始向后遍历dfs序。对于当前遍历到的节点id，其父节点为pid，那么若此时栈顶元素不等于pid，那么说明当前栈顶这颗子树已经搜索完毕，此时应该回溯，也就是将栈顶元素从栈中弹出。重复此过程直到栈为空或者栈顶元素等于pid。若此时的栈为空，说明dfs有问题，此时直接返回false即可，否则说明以及回溯到了当前节点的父节点，此时只需将当前节点加入到栈中表示向当前子树中开始进行搜索，然后继续向后遍历dfs即可。

若能成功遍历完dfs序，说明这是一颗合法的树，此时返回true。

最后附上python代码：

```python
class Solution(object):
    def isPreorder(self, nodes):
        """
        :type nodes: List[List[int]]
        :rtype: bool
        """

        if nodes[0][1] != -1:
            return False
        
        stack = [nodes[0][0]]
        for nid, pid in nodes[1:]:
            while stack and stack[-1] != pid:
                stack.pop()
            
            if stack:
                stack.append(nid)
            else:
                return False
        
        return True
```
