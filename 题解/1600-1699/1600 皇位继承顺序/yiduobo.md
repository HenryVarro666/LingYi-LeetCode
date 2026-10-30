---
title: "1600. 皇位继承顺序"
aliases: ["yiduobo的每日leetcode 1600.皇位继承顺序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432310236"
zhihu_id: "432310236"
zhihu_title: "yiduobo的每日leetcode 1600.皇位继承顺序"
question_id: "1600"
question: "皇位继承顺序"
problem_url: "https://leetcode.cn/problems/throne-inheritance/"
created: "2021-11-13T16:33:18+08:00"
updated: "2021-11-13T16:33:18+08:00"
upvotes: 0
comments: 0
---

# 1600. 皇位继承顺序

> **[yiduobo的每日leetcode 1600.皇位继承顺序](https://zhuanlan.zhihu.com/p/432310236) · 知乎 · 2021-11-13 · 赞同 0**
> 力扣：[1600. 皇位继承顺序](https://leetcode.cn/problems/throne-inheritance/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1600.皇位继承顺序

[力扣](https://leetcode-cn.com/problems/throne-inheritance/)

这题目里面的继承顺序是对于当前皇帝，若其有孩子，那么其长子为继承人，否则其兄弟为继承人。

这摆明了就是多叉树的孩子兄弟表示法的运用。孩子兄弟表示法是一种经典的用二叉树表示多叉树的做法，其思路就是对于某个节点，其在二叉树中的左孩子为该节点在多叉树中的第一个孩子节点，而其在二叉树中的右孩子则为该节点在多叉树中的下一个兄弟节点。

那么对于一颗使用孩子兄弟表示法做出来的二叉树执行一次dfs，得到的恰好就是题目中的皇位继承顺序了。对于题目中存在节点死亡的可能性，由于题目表示不影响继承顺序，那么只需要使用哈希表过滤一下最终的答案即可。

在具体实现时，除了常规的孩子以及兄弟这两个指针外，还需要额外维护一个最小的孩子指针，这样做的好处是出现了新的孩子时，可以通过这个指针在O(1)的时间复杂度内完成新孩子节点的插入，而不需要遍历其他的所有孩子节点。

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self, name):
        self.name = name
        self.child = self.brother = self.little_child = None

class ThroneInheritance(object):

    def __init__(self, kingName):
        """
        :type kingName: str
        """
        self.root = TreeNode(kingName)
        self.death_set = set()
        self.node_dict = {}
        self.node_dict[kingName] = self.root

    def birth(self, parentName, childName):
        """
        :type parentName: str
        :type childName: str
        :rtype: None
        """
        new_child = TreeNode(childName)
        self.node_dict[childName] = new_child
        parent = self.node_dict[parentName]
        if parent.child is None:
            parent.child = new_child
            parent.little_child = new_child
        else:
            little_child = parent.little_child
            little_child.brother = new_child
            parent.little_child = new_child

    def death(self, name):
        """
        :type name: str
        :rtype: None
        """
        self.death_set.add(name)

    def getInheritanceOrder(self):
        """
        :rtype: List[str]
        """
        self.res = []
        self.dfs(self.root)
        return self.res

    def dfs(self, now):
        if now.name not in self.death_set:
            self.res.append(now.name)
        if now.child:
            self.dfs(now.child)
        if now.brother:
            self.dfs(now.brother)

# Your ThroneInheritance object will be instantiated and called as such:
# obj = ThroneInheritance(kingName)
# obj.birth(parentName,childName)
# obj.death(name)
# param_3 = obj.getInheritanceOrder()
```
