---
title: "1530. 好叶子节点对的数量"
aliases: ["yiduobo的每日leetcode 1530.好叶子节点对的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/422968292"
zhihu_id: "422968292"
zhihu_title: "yiduobo的每日leetcode 1530.好叶子节点对的数量"
question_id: "1530"
question: "好叶子节点对的数量"
problem_url: "https://leetcode.cn/problems/number-of-good-leaf-nodes-pairs/"
created: "2021-10-19T00:25:41+08:00"
updated: "2021-10-19T00:25:41+08:00"
upvotes: 0
comments: 0
---

# 1530. 好叶子节点对的数量

> **[yiduobo的每日leetcode 1530.好叶子节点对的数量](https://zhuanlan.zhihu.com/p/422968292) · 知乎 · 2021-10-19 · 赞同 0**
> 力扣：[1530. 好叶子节点对的数量](https://leetcode.cn/problems/number-of-good-leaf-nodes-pairs/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1530.好叶子节点的数量

[力扣](https://leetcode-cn.com/problems/number-of-good-leaf-nodes-pairs/)

首先可以明确的一点是，对于以now为根节点的子树而言，所有经过now的合法路径的起点和终点不可能出现在now的同一侧子树当中。证明也很简单，因为若某条合法路径的起点和终点出现在now的同一侧子树当中，那么只有两种情况，即同时出现在左子树中或同时出现在右子树中。这样的话，这里起点到终点的最短路径就必然不可能经过now。以起点和终点同时出现在now的左子树中为例，此时从起点出发向上走，最晚走到now.left时就可以开始向下走去找终点了，而不需要继续上升到now，对于同时出现在右子树中时也是同样的道理。

有了上面的结论，就可以设计出一种递归的算法。对于当前节点now，只计算以now为根节点的子树中，所有经过now的合法路径条数，而对于不经过now的合法路径，则可以通过递归求解now.left以及now.right来得到。

乍一看这里可能要用树分治来处理，不过注意到distance最大值为10，因此可以对于每个节点而言，都只需要维护以该节点为根节点的子树中，与该节点距离为0到9之间的叶子节点数目。那么对于节点now：

1、若now既没有左孩子也没有右孩子：

说明now是一个叶子节点，因此对于now而言，dis[0] \= 1，而dis[1]到dis[9]都为0，而此时以now为根节点的子树中合法路径数目显然为0，因此返回0和dis

2、若now只有左孩子：

此时可以先递归求解now.left，得到左子树中的合法路径条数l_res，以及以now.left为根节点的子树中与now.left距离在0到9之间的叶子节点数目数组l_dis。由于多出了now.left到now这一步，因此以now为根节点的子树中与now距离在0到9之间的叶子节点数目dis[index] \= l_dis[index - 1]

此时以now为根节点的子树中合法路径的数目就是l_res，因此返回l_res以及dis

3、若now只有右孩子：

与情况2类似，优先递归求解now.right，得到r_res以及r_dis。同样地，有dis[index] \= r_dis[index - 1]

此时以now为根节点的子树中合法路径的数目就是r_res，因此返回r_res以及dis

4、若now同时具有左孩子和右孩子：

此时的前期处理与情况2和情况3类似，都是优先递归求解now.left以及now.right，然后通过l_dis以及r_dis来更新dis。

除此之外，还需要计算经过now的合法路径数目。在这里直接两重循环枚举l_dis以及r_dis是可行的，当然也可以使用单调性来进行优化。对于右子树中与根节点距离为k的节点而言，必须选择左子树中与根节点距离为1到disntance - k之间的节点，因此可以从大到小枚举k，并计算左子树中距离为1到disntance - k之间的节点数目s。当k变小时，只需要在原有基础上将l_dis[distance - k]加入到s中即可。记这里计算出来的合法路径数目为now_res。

此时以now为根节点的子树中合法路径的数目就是l_res + r_res + now_res，因此返回这三个res之和以及dis。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def countPairs(self, root, distance):
        """
        :type root: TreeNode
        :type distance: int
        :rtype: int
        """

        return self.dfs(root, distance)[0]
    
    def dfs(self, now, distance):
        if not now.left:
            if not now.right:
                res = 0
                dis = [0] * distance
                dis[0] = 1
            else:
                res, right_dis = self.dfs(now.right, distance)
                dis = [0] + [x for x in right_dis[:distance - 1]]
        elif not now.right:
            res, left_dis = self.dfs(now.left, distance)
            dis = [0] + [x for x in left_dis[:distance - 1]]
        else:
            left_res, left_dis = self.dfs(now.left, distance)
            right_res, right_dis = self.dfs(now.right, distance)
            
            for index in range(distance - 1, 0, -1):
                left_dis[index] = left_dis[index - 1]
                right_dis[index] = right_dis[index - 1]
            left_dis[0] = right_dis[0] = 0

            res = left_res + right_res
            s = 0
            for index in range(distance - 1, 0, -1):
                s += left_dis[distance - index]
                res += s * right_dis[index]
            
            dis = [0] * distance
            for index in range(distance):
                dis[index] += left_dis[index] + right_dis[index]
            
        return res, dis
```
