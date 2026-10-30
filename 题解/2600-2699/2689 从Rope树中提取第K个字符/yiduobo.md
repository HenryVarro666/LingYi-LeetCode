---
title: "2689. 从Rope树中提取第K个字符"
aliases: ["yiduobo的每日leetcode 2689.从Rope树中提取第K个字符"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650008292"
zhihu_id: "650008292"
zhihu_title: "yiduobo的每日leetcode 2689.从Rope树中提取第K个字符"
question_id: "2689"
question: "从Rope树中提取第K个字符"
problem_url: "https://leetcode.cn/problems/extract-kth-character-from-the-rope-tree/"
created: "2023-08-14T21:07:27+08:00"
updated: "2023-08-14T21:07:27+08:00"
upvotes: 0
comments: 0
---

# 2689. 从Rope树中提取第K个字符

> **[yiduobo的每日leetcode 2689.从Rope树中提取第K个字符](https://zhuanlan.zhihu.com/p/650008292) · 知乎 · 2023-08-14 · 赞同 0**
> 力扣：[2689. 从Rope树中提取第K个字符](https://leetcode.cn/problems/extract-kth-character-from-the-rope-tree/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2689.从Rope树中提取第K个字符

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/extract-kth-character-from-the-rope-tree/description/)

首先，若当前的root.len等于0，那么说明当前是一个叶子节点，其对应的第k个字符自然就是root.val[k - 1]。否则的话说明这是一个内部节点，此时就需要在其左子树或者右子树中递归求解。

若当前节点没有左孩子，那么说明答案一定位于右子树中，因此在root.right中递归求解第k个字符就行了。

若其有左孩子，则需要判断k与其左孩子包含的字符数量的大小。设左子树中包含的字符数量为p，那么当k小于等于p时，问题就变成了在root.left中递归求解第k个字符，否则就是在root.right中递归求解第k - p个字符。

另外关于左子树中字符数量的判断，则可以取root.left.len以及len(root.left.val)中的较大值。当root.left为叶子节点时，root.left.len为0，而len(root.left.val)则表示其对应字符串的长度。反过来，当root.left为内部节点是，root.left.val为空，因此len(root.left.val)为0，而root.left.len则表示其表示字符串的长度。

最后附上python代码：

```python
# Definition for a rope tree node.
# class RopeTreeNode(object):
#     def __init__(self, len=0, val="", left=None, right=None):
#         self.len = len
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def getKthCharacter(self, root, k):
        """
        :type root: Optional[RopeTreeNode]
        :type k: int
        :rtype: str
        """

        if root.len == 0:
            return root.val[k - 1]
        
        if root.left:
            if max(root.left.len, len(root.left.val)) >= k:
                return self.getKthCharacter(root.left, k)
            else:
                return self.getKthCharacter(root.right, k - max(root.left.len, len(root.left.val)))
        else:
            return self.getKthCharacter(root.right, k)
```
