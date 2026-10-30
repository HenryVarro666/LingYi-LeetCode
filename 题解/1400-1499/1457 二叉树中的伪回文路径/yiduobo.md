---
title: "1457. 二叉树中的伪回文路径"
aliases: ["yiduobo的每日leetcode 1457.二叉树中的伪回文路径"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/二-二叉树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/412251205"
zhihu_id: "412251205"
zhihu_title: "yiduobo的每日leetcode 1457.二叉树中的伪回文路径"
question_id: "1457"
question: "二叉树中的伪回文路径"
problem_url: "https://leetcode.cn/problems/pseudo-palindromic-paths-in-a-binary-tree/"
difficulty: "Medium"
rating: 1405
created: "2021-09-20T16:20:54+08:00"
updated: "2021-09-20T16:20:54+08:00"
upvotes: 0
comments: 0
---

# 1457. 二叉树中的伪回文路径

> **[yiduobo的每日leetcode 1457.二叉树中的伪回文路径](https://zhuanlan.zhihu.com/p/412251205) · 知乎 · 2021-09-20 · 赞同 0**
> 力扣：[1457. 二叉树中的伪回文路径](https://leetcode.cn/problems/pseudo-palindromic-paths-in-a-binary-tree/) · Medium · 灵茶山艾府：[一步步优化：从数组到位运算（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1457.二叉树中的伪回文路径

[力扣](https://leetcode-cn.com/problems/pseudo-palindromic-paths-in-a-binary-tree/)

根据伪回文路径的定义，需要满足路径中出现次数为奇数次的数字数目小于等于1。由于这里只有9个数字，因此可以进行二进制编码，即使用一个9位二进制数来表示当前路径中数字的奇偶性。

接下来从根节点开始执行一次bfs。对于当前节点now，首先将now.val加入到编码当中，然后判断当前编码中1出现的数目。若这个数目小于等于1，那么说明从根节点到now的路径是伪回文路径，将答案加上1。接下来根据当前节点是否有孩子节点，将对应的孩子节点以及当前编码加入到队列中即可。

具体实现上，更新编码时可以使用异或操作，而判断1的个数则可以使用lowbit操作。

最后附上python代码：

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def pseudoPalindromicPaths (self, root):
        """
        :type root: TreeNode
        :rtype: int
        """

        q = [[root, 0]]
        l = 0
        r = 1
        res = 0
        while l < r:
            now, state = q[l]
            l += 1
            state ^= (1 << (now.val - 1))
            if now.left is None and now.right is None:
                tmp = state
                cnt = 0
                while tmp:
                    cnt += 1
                    tmp -= tmp & - tmp
                
                if cnt <= 1:
                    res += 1
            else:
                if now.left:
                    q.append([now.left, state])
                    r += 1
                if now.right:
                    q.append([now.right, state])
                    r += 1
        
        return res
```
