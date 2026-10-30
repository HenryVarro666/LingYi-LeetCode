---
title: "666. 路径总和IV"
aliases: ["yiduobo的每日leetcode 666.路径总和IV"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/603674658"
zhihu_id: "603674658"
zhihu_title: "yiduobo的每日leetcode 666.路径总和IV"
question_id: "666"
question: "路径总和IV"
problem_url: "https://leetcode.cn/problems/path-sum-iv/"
created: "2023-02-05T18:06:23+08:00"
updated: "2023-02-05T18:06:23+08:00"
upvotes: 0
comments: 0
---

# 666. 路径总和IV

> **[yiduobo的每日leetcode 666.路径总和IV](https://zhuanlan.zhihu.com/p/603674658) · 知乎 · 2023-02-05 · 赞同 0**
> 力扣：[666. 路径总和IV](https://leetcode.cn/problems/path-sum-iv/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

666.路径总和IV

[力扣](https://leetcode.cn/problems/path-sum-iv/)

题目对于树中节点的描述为第d层的第p个节点值为v，其中p是按照满二叉树的位置编号排布的。由于在这里要体现出满二叉树的节点位置次序，因此使用数组来模拟树是比较合适的做法。即使用数组中的元素来表示单个的节点，同时通过数组下标来体现树中的父子关系。具体来说，数组中下标0的元素表示整棵树的根节点，而对于下标i而言，其左孩子的下标为i \* 2 + 1，右孩子的下标则为i \* 2 + 2。

对于一颗满二叉树，其第i层的节点数目为2^(i - 1)，那么前i层的节点总数就是2^i - 1，因此对于第d层的节点，前d - 1层一共有2^(d - 1) - 1个节点，因此第d层节点的下标就应该从2^(d - 1) - 1开始计算，那么第d层的第p个节点在数组中的下标就是2^(d - 1) - 1 + p - 1。

有了这个结论，就可以一趟遍历，就所有数字转化成数组中的元素，将树构造出来了。

接下来，从根节点向下进行dfs。对于当前节点now：

1、若其存在左孩子，那么递归求解其左孩子，也就是now + now + 1，左子树中的路径总和left_s，以及叶子节点的数目left_cnt。反之，若其不存在左孩子，那么置left_s和left_cnt都为0

2、与情况1对称，按同样的方式计算now的右孩子对应的right_s以及right_cnt

3、此时就有以now为根节点的子树中叶子节点的总数为leaf_cnt \= left_cnt + right_cnt。

若leaf_cnt为0，说明now自身就是一个叶子节点，此时返回now的值以及1，即以now为根节点的子树的路径总和为now自身的值，其中的叶子节点数目为1。

若leaf_cnt不为0，那么以now为根节点的子树中就一共有leaf_cnt条从根节点到叶子节点的路径，因此now自身为最终结果带来的价值为now的值乘以leaf_cnt，此时就应该返回这个乘积加上left_s和right_s，以及树中叶子节点的总数leaf_cnt

dfs计算完成后，返回值的第一项就是题目要求的路径总和。

最后附上python代码：

```python
class Solution(object):
    def pathSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        f = [-1] * 31
        for num in nums:
            d = num / 100
            p = num / 10 % 10
            v = num % 10
            f[(1 << (d - 1)) - 1 + p - 1] = v
        
        def dfs(now):
            if f[now + now + 1] != -1:
                left_s, left_cnt = dfs(now + now + 1)
            else:
                left_s, left_cnt = 0, 0
            
            if f[now + now + 2] != -1:
                right_s, right_cnt = dfs(now + now + 2)
            else:
                right_s, right_cnt = 0, 0
            
            leaf_cnt = left_cnt + right_cnt
            if leaf_cnt == 0:
                return f[now], 1
            else:
                return f[now] * leaf_cnt + left_s + right_s, leaf_cnt

        return dfs(0)[0]
```
