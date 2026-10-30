---
title: "LCP 64. 二叉树灯饰"
aliases: ["yiduobo的每日leetcode LCP64.二叉树灯饰"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/binary-tree", "leetcode/dp", "leetcode/dp-2", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/链表-二叉树与回溯/二-二叉树", "题单/动态规划/十二-树形-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/579548088"
zhihu_id: "579548088"
zhihu_title: "yiduobo的每日leetcode LCP64.二叉树灯饰"
question_id: "LCP 64"
question: "二叉树灯饰"
problem_url: "https://leetcode.cn/problems/U7WvvU/"
difficulty: "Medium"
created: "2022-11-02T02:53:59+08:00"
updated: "2022-11-02T02:53:59+08:00"
upvotes: 1
comments: 0
---

# LCP 64. 二叉树灯饰

> **[yiduobo的每日leetcode LCP64.二叉树灯饰](https://zhuanlan.zhihu.com/p/579548088) · 知乎 · 2022-11-02 · 赞同 1**
> 力扣：[LCP 64. 二叉树灯饰](https://leetcode.cn/problems/U7WvvU/) · Medium · 灵茶山艾府：[树形 DP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP64.二叉树灯饰

[力扣](https://leetcode.cn/problems/U7WvvU/)

对于一颗以now为根节点的子树而言，树中灯泡受祖先节点的影响可能出现四种状态：

1、没有因为祖先节点的操作受到任何影响

2、now的所有祖先节点一共操作了奇数次开关2

3、now的父亲节点操作了开关3

4、now的所有祖先节点一共操作了奇数次开关2，同时now的父亲节点操作了开关3

那么可以将这四种情况做成一个两位的二进制编码，其中低位为开关2的使用情况，高位为开关3的使用情况。

接下来，令f[now][state]表示以now为根的子树，当前受影响状态为state时，将树中灯泡全部打开最少需要的操作次数。对于f[now][state]，首先可以通过state分离出当前state是否受开关2和开关3的影响，分别记为switch_root和switch_all。接下来，可以根据switch_root和switch_all更新当前now的开关情况，然后对更新后的开关情况进行讨论。有一点可以明确的是，对于now而言，不会对同一个开关操作两次，因此同一个开关操作两次相当于什么都没干。

1、如果当前now是亮着的：

1-1）不进行任何操作：

此时就有f[now][state] \= f[now.left][switch_all] + f[now.right][switch_all]。由于本次没有进行操作，所以now.left和now.right对应的swtich_root都是0，新的编码就只有从上面传下来的switch_all

1-2）同时操作开关1和开关2：

此时就有f[now][state] \= f[now.left][1 - switch_all] + f[now.right][1 - switch_all] + 2。这里的1 - switch_all表示因为now这里也操作了开关2，因此switch_all需要取反。另外，这里的switch_root也是0，因此新的编码就是1 - switch_all。最后的加2则是这两次操作的次数

1-3）同时操作开关1和开关3：

此时就有f[now][state] \= f[now.left][2 + switch_all] + f[now.right][2 + switch_all] + 2。这里的2 + switch_all表示受now操作开关3的影响，now.left和now.right的switch_root应该为1，而switch_all则不受影响，因此直接在二进制编码中加上了2。最后的加2同样是这两次操作的次数

1-4）同时操作开关2和开关3：

此时就有f[now][state] \= f[now.left][3 - switch_all] + f[now.right][3 - switch_all] + 2。这里的3 - switch_all可以拆分成2 + (1 - switch_all)，与情况2和情况3中对switch_root和switch_all的操作一一对应。最后的2依然是这两次操作的次数

2、如果当前now是灭的：

2-1）可以在1-1)的基础上，操作开关1：

此时就有f[now][state] \= f[now.left][switch_all] + f[now.right][switch_all] + 1

2-2）可以在1-2)的基础上，不操作开关1，即只操作开关2：

此时就有f[now][state] \= f[now.left][1 - switct_all] + f[now.right][1 - switch_all] + 1

2-3）可以在1-3)的基础上，不操作开关1，即只操作开关3：

此时就有f[now][state] \= f[now.left][2 + switct_all] + f[now.right][2 + switch_all] + 2

2-4）可以在1-4)的基础上，操作开关1：

此时就有f[now][state] \= f[now.left][3 - switch_all] + f[now.right][3 - swtich_all] + 3

可以发现，由于开关1不会影响now.left和now.right，那么完全可以将其单独剥离出来，只讨论开关2和开关3的组合，然后更加组合情况以及now当前的亮灭状态来决定是否需要操作开关1。

不妨设变量v表示当前now的亮灭状态，当v \= 1时表示now亮着，当v \= 0时表示now灭了，那么就有

f[now][state] \= min(

f[now.left][switch_all] + f[now.right][switch_all] + v，

f[now.left][1 - switch_all] + f[now.right][1 - switch_all] + 2 - v，

f[now.left][3 - switch_all] + f[now.right][3 - switch_all] + 2 - v，

f[now.left][3 - switch_all] + f[now.right][3 - swtich_all] + 2 + v)

具体实现上，依然是记忆化搜索的方式，从f[root][0]开始递归求解，求解完毕后f[root][0]就是最终答案。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution(object):
    def closeLampInTree(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        f = {}

        def dfs(now, state):
            if not now:
                return 0
            
            if now not in f or state not in f[now]:
                switch_root = state / 2
                switch_all = state % 2
                v = now.val
                if switch_root == 1:
                    v = 1 - v
                if switch_all == 1:
                    v = 1 - v
            
                t1 = dfs(now.left, switch_all) + dfs(now.right, switch_all) + v
                t2 = dfs(now.left, 1 - switch_all) + dfs(now.right, 1 - switch_all) + 2 - v
                t3 = dfs(now.left, 2 + switch_all) + dfs(now.right, 2 + switch_all) + 2 - v
                t4 = dfs(now.left, 3 - switch_all) + dfs(now.right, 3 - switch_all) + 2 + v

                if now not in f:
                    f[now] = {}
                f[now][state] = min(t1, t2, t3, t4)

            return f[now][state]
        
        return dfs(root, 0)
```
