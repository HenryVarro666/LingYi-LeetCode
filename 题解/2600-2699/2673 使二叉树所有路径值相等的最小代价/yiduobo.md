---
title: "2673. 使二叉树所有路径值相等的最小代价"
aliases: ["yiduobo的每日leetcode 2673.使二叉树所有路径值相等的最小代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/链表-二叉树与回溯", "题单/贪心算法", "题单/链表-二叉树与回溯/二-二叉树", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649067505"
zhihu_id: "649067505"
zhihu_title: "yiduobo的每日leetcode 2673.使二叉树所有路径值相等的最小代价"
question_id: "2673"
question: "使二叉树所有路径值相等的最小代价"
problem_url: "https://leetcode.cn/problems/make-costs-of-paths-equal-in-a-binary-tree/"
difficulty: "Medium"
rating: 1917
created: "2023-08-09T23:01:49+08:00"
updated: "2023-08-11T02:08:46+08:00"
upvotes: 0
comments: 0
---

# 2673. 使二叉树所有路径值相等的最小代价

> **[yiduobo的每日leetcode 2673.使二叉树所有路径值相等的最小代价](https://zhuanlan.zhihu.com/p/649067505) · 知乎 · 2023-08-09 · 赞同 0**
> 力扣：[2673. 使二叉树所有路径值相等的最小代价](https://leetcode.cn/problems/make-costs-of-paths-equal-in-a-binary-tree/) · Medium · 灵茶山艾府：[贪心，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2673.使二叉树所有路径值相等的最小代价

[力扣](https://leetcode.cn/problems/make-costs-of-paths-equal-in-a-binary-tree/description/)

不妨先考察所有互为兄弟节点的叶子节点对。对于一组叶子节点兄弟，这两个节点从二者共同的父节点开始，一直到整棵树的根节点的这条路径上，所经过的节点都是完全相同的，这也就意味着为了使得从根节点到这两个叶节点的路径值相等，就必须要让这两个节点值相同。于是可以先将所有互为兄弟节点的叶子节点对的值都调整成一致。

调整完毕后，对于一对兄弟节点的父节点，由于其两个孩子节点值都相同，那么可以将这两个孩子节点收缩到当前节点，同时将叶子节点的值累加到当前节点。这样一来，就相当于移除掉了整颗二叉树的最下层，而此时问题则变成了一个规模缩小一层的相同的问题，于是只需继续按照调整子节点值然后收缩的流程不断执行，直到只剩下整棵树的根节点为止。

在具体实现上，由于题目保证了这是一颗满二叉树，那么就意味着每一层的节点数量都是2的幂次，于是只需从后往前遍历cost数组，就可以根据每一轮收缩后的二叉树的层高，来确定叶子节点这一层中节点的数量，从而确定遍历的起点和终点。接下来以2为步长遍历区间中的节点，也就是一组兄弟节点，然后进行节点值的调整。在调整完节点值之后，则可以通过计算下标减1后除以2，来得到这一组兄弟节点的父节点对应的数组下标，从而完成收缩时节点值的累加这一步。

最后附上python代码：

```python
class Solution(object):
    def minIncrements(self, n, cost):
        """
        :type n: int
        :type cost: List[int]
        :rtype: int
        """

        tmp = n
        level = 0
        while tmp:
            level += 1
            tmp >>= 1
        
        pre_end = n - 1
        res = 0
        for i in range(level - 1, 0, -1):
            node_cnt = 1 << i
            for j in range(pre_end, pre_end - node_cnt, -2):
                if cost[j] < cost[j - 1]:
                    res += cost[j - 1] - cost[j]
                    cost[j] = cost[j - 1]
                else:
                    res += cost[j] - cost[j - 1]
                    cost[j - 1] = cost[j]
                
                cost[(j - 1) // 2] += cost[j]
            
            pre_end -= node_cnt

        return res
```
