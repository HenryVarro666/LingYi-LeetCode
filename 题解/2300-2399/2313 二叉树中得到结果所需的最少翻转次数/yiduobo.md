---
title: "2313. 二叉树中得到结果所需的最少翻转次数"
aliases: ["yiduobo的每日leetcode 2313.二叉树中得到结果所需的最少翻转次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/629652557"
zhihu_id: "629652557"
zhihu_title: "yiduobo的每日leetcode 2313.二叉树中得到结果所需的最少翻转次数"
question_id: "2313"
question: "二叉树中得到结果所需的最少翻转次数"
problem_url: "https://leetcode.cn/problems/minimum-flips-in-binary-tree-to-get-result/"
created: "2023-05-16T02:38:12+08:00"
updated: "2023-05-16T02:38:12+08:00"
upvotes: 0
comments: 0
---

# 2313. 二叉树中得到结果所需的最少翻转次数

> **[yiduobo的每日leetcode 2313.二叉树中得到结果所需的最少翻转次数](https://zhuanlan.zhihu.com/p/629652557) · 知乎 · 2023-05-16 · 赞同 0**
> 力扣：[2313. 二叉树中得到结果所需的最少翻转次数](https://leetcode.cn/problems/minimum-flips-in-binary-tree-to-get-result/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2313.二叉树中得到结果所需的最少翻转次数

[力扣](https://leetcode.cn/problems/minimum-flips-in-binary-tree-to-get-result/)

经典的动态规划问题，令f[node][target]表示将以node为根节点的子树值变为target所需的最少翻转次数，那么对于f[node][target]：

1、若node的值为0或者1：

若此时的target为1，那么所需的操作次数就是1 - node.val，否则就是node.val

2、若node的值为OR操作符：

若此时的target为true，那么只需左右子树的结果中有一个为true就行了。于是有f[node][target] \= min(f[node.left][true], f[node.right][true])。

若此时的result为false，那么要求左右子树的结果都为false。于是有f[node][target] \= f[node.left][false] + f[node.right][false]。

3、若node的值为AND操作符：

若此时的result为true，那么要求左右子树的结果都为true。于是有f[node][target] \= f[node.left][true] + f[node.right][true]。

若此时的result为false，那么只需左右子树的结果中有一个false就行了。于是有f[node][target] \= min(f[node.left][false], f[node.right][false])。

4、若node的值为XOR操作符：

若此时的result为true，那么要求左右子树的结果不同。于是有f[node][target] \= min(f[node.left][true] + f[node.right][false], f[node.left][false] + f[node.right][true])。

若此时的result为false，那么要求左右子树的结果一致。于是有f[node][target] \= min(f[node.left][true] + f[node.right][true], f[node.left][false] + f[node.right][false])。

5、若node的值为NOT操作符：

这种情况最简单。若now存在左孩子，那么就有f[now][target] \= f[now.left][not target]，否则就有f[now][target] \= f[now.right][not target]。

根据上面的处理方法，从根节点向下求解f[root][result]即可。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def minimumFlips(self, root, result):
        """
        :type root: Optional[TreeNode]
        :type result: bool
        :rtype: int
        """

        f = {}

        def dfs(now, target):
            key = (now, target)
            if key not in f:

                if now.val == 0 or now.val == 1:
                    if target:
                        f[key] = 1 - now.val
                    else:
                        f[key] = now.val
                elif now.val == 2:
                    if target:
                        f[key] = min(dfs(now.left, True), dfs(now.right, True))
                    else:
                        f[key] = dfs(now.left, False) + dfs(now.right, False)
                elif now.val == 3:
                    if target:
                        f[key] = dfs(now.left, True) + dfs(now.right, True)
                    else:
                        f[key] = min(dfs(now.left, False), dfs(now.right, False))
                elif now.val == 4:
                    if target:
                        f[key] = min(dfs(now.left, True) + dfs(now.right, False), \
                               dfs(now.right, True) + dfs(now.left, False))
                    else:
                        f[key] = min(dfs(now.left, True) + dfs(now.right, True), \
                               dfs(now.left, False) + dfs(now.right, False))
                else:
                    if now.left:
                        f[key] = dfs(now.left, not target)
                    else:
                        f[key] = dfs(now.right, not target)

            return f[key]

        return dfs(root, result)
```
