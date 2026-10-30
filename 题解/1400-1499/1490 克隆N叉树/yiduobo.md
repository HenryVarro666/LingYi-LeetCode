---
title: "1490. 克隆N叉树"
aliases: ["yiduobo的每日leetcode 1490.克隆N叉树"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/616832090"
zhihu_id: "616832090"
zhihu_title: "yiduobo的每日leetcode 1490.克隆N叉树"
question_id: "1490"
question: "克隆N叉树"
problem_url: "https://leetcode.cn/problems/clone-n-ary-tree/"
created: "2023-03-24T23:20:33+08:00"
updated: "2023-03-24T23:20:33+08:00"
upvotes: 0
comments: 0
---

# 1490. 克隆N叉树

> **[yiduobo的每日leetcode 1490.克隆N叉树](https://zhuanlan.zhihu.com/p/616832090) · 知乎 · 2023-03-24 · 赞同 0**
> 力扣：[1490. 克隆N叉树](https://leetcode.cn/problems/clone-n-ary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1490.克隆N叉树

[力扣](https://leetcode.cn/problems/clone-n-ary-tree/)

与之前的1485题类似，同样是通过哈希表辅助建立父子关系。我在这里依然是采用bfs来进行处理。

最后附上python代码：

```python
"""
# Definition for a Node.
class Node(object):
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []
"""

class Solution(object):
    def cloneTree(self, root):
        """
        :type root: Node
        :rtype: Node
        """

        if not root:
            return None

        mapping = {}
        q = [root]
        mapping[root] = Node(root.val)

        head, tail = 0, 1
        while head < tail:
            now = q[head]
            head += 1
            for child in now.children:
                mapping[child] = Node(child.val)
                mapping[now].children.append(mapping[child])
                q.append(child)
                tail += 1

        return mapping[root]
```
