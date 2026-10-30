---
title: "2005. 斐波那契树的移除子树游戏"
aliases: ["yiduobo的每日leetcode 2005.斐波那契树的移除子树游戏"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/624944107"
zhihu_id: "624944107"
zhihu_title: "yiduobo的每日leetcode 2005.斐波那契树的移除子树游戏"
question_id: "2005"
question: "斐波那契树的移除子树游戏"
problem_url: "https://leetcode.cn/problems/subtree-removal-game-with-fibonacci-tree/"
created: "2023-04-26T03:22:01+08:00"
updated: "2023-04-26T03:22:01+08:00"
upvotes: 0
comments: 0
---

# 2005. 斐波那契树的移除子树游戏

> **[yiduobo的每日leetcode 2005.斐波那契树的移除子树游戏](https://zhuanlan.zhihu.com/p/624944107) · 知乎 · 2023-04-26 · 赞同 0**
> 力扣：[2005. 斐波那契树的移除子树游戏](https://leetcode.cn/problems/subtree-removal-game-with-fibonacci-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2005.斐波那契树的移除子树游戏

[力扣](https://leetcode.cn/problems/subtree-removal-game-with-fibonacci-tree/)

又是sg函数相关的问题，不过本题与常规的sg函数题目有所不同，是在一颗树上进行游戏。对于树上sg函数相关的问题，通常需要用到克朗定理，具体来说就是对于一棵树而言，其各个树链可以合并成为一条单链，而这条单链的长度则是各个支链上的边数的异或和。另一方面，由于长度为k的单链sg函数值就是k，那么在这里也可以认为是各个支链的sg函数异或和。

对于本题，由于拿到根节点的人会输，因此在这里可以转化成对于左右两颗子树，谁可以拿走最后的节点，那么另一个人就只能拿走根节点了。令sg(i)表示order(i)这棵树的sg函数值，那么就有sg(i) \= sg(i - 1) ^ sg(i - 2) + 1，而最终答案就是sg(n - 1) ^ sg(n - 2)。

最后附上python代码：

```python
class Solution(object):
    def findGameWinner(self, n):
        """
        :type n: int
        :rtype: bool
        """

        sg = []
        sg.append(0)
        sg.append(1)
        for index in range(2, n):
            sg.append((sg[index - 1] ^ sg[index - 2]) + 1)
        
        if n == 1:
            return False

        res = sg[n - 1] ^ sg[n - 2]
        return res > 0
```
