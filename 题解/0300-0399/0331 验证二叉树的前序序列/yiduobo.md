---
title: "331. 验证二叉树的前序序列"
aliases: ["yiduobo的每日leetcode 331.验证二叉树的前序序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/161485048"
zhihu_id: "161485048"
zhihu_title: "yiduobo的每日leetcode 331.验证二叉树的前序序列"
question_id: "331"
question: "验证二叉树的前序序列"
problem_url: "https://leetcode.cn/problems/verify-preorder-serialization-of-a-binary-tree/"
created: "2020-07-18T15:13:29+08:00"
updated: "2020-07-18T15:13:29+08:00"
upvotes: 0
comments: 0
---

# 331. 验证二叉树的前序序列

> **[yiduobo的每日leetcode 331.验证二叉树的前序序列](https://zhuanlan.zhihu.com/p/161485048) · 知乎 · 2020-07-18 · 赞同 0**
> 力扣：[331. 验证二叉树的前序序列](https://leetcode.cn/problems/verify-preorder-serialization-of-a-binary-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

331.验证二叉树的前序序列<https://leetcode-cn.com/problems/verify-preorder-serialization-of-a-binary-tree/>

在这里我们并不需要考虑节点的数值，而只需要判断节点是否为空。对于每个非空的节点，其可以提供两个坑位，而除根节点之外的每个节点都需要消费掉一个坑位。换言之，我们只需要判断在前序遍历的过程中坑位是否足够即可。

由于前序遍历是根-左-右，那么在实现上可以直接从左往右扫描序列化字符串，然后判断当前坑位是否足够，并且根据当前节点是否为空来更新坑位信息。在这个过程中如果没有出现过坑位不足的情况，且最终的坑位数为0，那么就是合法的序列。

最后附上python代码：

```python
class Solution(object):
    def isValidSerialization(self, preorder):
        """
        :type preorder: str
        :rtype: bool
        """

        childs = None
        for char in preorder.split(','):
            if childs is not None:
                childs -=1
                if childs < 0:
                    return False
            else:
                childs = 0

            if char != '#':
                childs += 2

        return childs == 0
```
