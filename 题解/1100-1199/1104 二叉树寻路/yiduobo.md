---
title: "1104. 二叉树寻路"
aliases: ["yiduobo的每日leetcode 1104.二叉树寻路"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374475443"
zhihu_id: "374475443"
zhihu_title: "yiduobo的每日leetcode 1104.二叉树寻路"
question_id: "1104"
question: "二叉树寻路"
problem_url: "https://leetcode.cn/problems/path-in-zigzag-labelled-binary-tree/"
difficulty: "Medium"
rating: 1545
created: "2021-05-22T23:06:28+08:00"
updated: "2021-05-22T23:06:28+08:00"
upvotes: 0
comments: 0
---

# 1104. 二叉树寻路

> **[yiduobo的每日leetcode 1104.二叉树寻路](https://zhuanlan.zhihu.com/p/374475443) · 知乎 · 2021-05-22 · 赞同 0**
> 力扣：[1104. 二叉树寻路](https://leetcode.cn/problems/path-in-zigzag-labelled-binary-tree/) · Medium · 灵茶山艾府：[递归三行解决此题](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1104.二叉树寻路

[力扣](https://leetcode-cn.com/problems/path-in-zigzag-labelled-binary-tree/)

首先，由于这颗二叉树是满的，那么每一层节点的数量都可以很快计算出来，具体来说就是第k层中一个有2^(k - 1)个节点，k从1开始计数。

有了这一点，我们就可以很快得到前k层的节点数量，为2^k - 1，然后就可以判断出label对应的节点位于第几层从左向右数第几个了。设label位于第l层，那么前l - 1层一共有2 ^ l - 1个节点，前l层一共有2 ^ (l + 1) - 1个节点，那么这里必须满足

2 ^ l - 1 \< label \<\= 2 ^ (l + 1) - 1

通过这个不等式找到l之后，可以顺便求出label是第l层的第p \= label - 2^l个节点。

接下来，对于第l层第p个节点而言，其父亲节点为第l - 1层的第p / 2个节点，根据这一点我们就可以从label对应的节点开始倒推回root，找到题目要求的这条路径。

最后，题目要求的节点编号顺序跟层数的奇偶性相关，在计算时需要特别处理一下。

最后附上python代码：

```python
class Solution(object):
    def pathInZigZagTree(self, label):
        """
        :type label: int
        :rtype: List[int]
        """

        cnt_list = [1]
        while cnt_list[-1] < label:
            cnt_list.append(cnt_list[-1] + cnt_list[-1] + 1)
        
        res = []
        level = len(cnt_list) - 1
        if level % 2 == 0:
            if level == 0:
                pos = 1
            else:
                pos = label - cnt_list[-2] - 1
        else:
            pos = cnt_list[-1] - label

        while level > 0:
            if level % 2 == 0:
                res.append(cnt_list[level - 1] + 1 + pos)
            else:
                res.append(cnt_list[level] - pos)
            level -= 1
            pos /= 2
        
        res.append(1)
        res.reverse()
        return res
```
