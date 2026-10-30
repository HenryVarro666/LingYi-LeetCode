---
title: "3331. 修改后子树的大小"
aliases: ["yiduobo的每日leetcode 3331.修改后子树的大小"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/tree", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/backtracking", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/24372187842"
zhihu_id: "24372187842"
zhihu_title: "yiduobo的每日leetcode 3331.修改后子树的大小"
question_id: "3331"
question: "修改后子树的大小"
problem_url: "https://leetcode.cn/problems/find-subtree-sizes-after-changes/"
difficulty: "Medium"
rating: 2046
created: "2025-02-17T23:03:06+08:00"
updated: "2025-02-17T23:03:21+08:00"
upvotes: 0
comments: 0
---

# 3331. 修改后子树的大小

> **[yiduobo的每日leetcode 3331.修改后子树的大小](https://zhuanlan.zhihu.com/p/24372187842) · 知乎 · 2025-02-17 · 赞同 0**
> 力扣：[3331. 修改后子树的大小](https://leetcode.cn/problems/find-subtree-sizes-after-changes/) · Medium · 灵茶山艾府：[两种方法：两次 DFS / 一次 DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3331.修改后子树的大小

[3331. 修改后子树的大小 - 力扣（LeetCode）](https://leetcode.cn/problems/find-subtree-sizes-after-changes/description/)

题目给出一颗编号为0到n - 1，且根节点为0号节点的树。另外给出一个长度为n的字符串s，其中s[i]表示节点i对应的字符。接下来对于节点1到节点n - 1中的每个节点x，同时执行一下操作一次：

找到距离x最近的祖先节点y，且s[x] \= s[y]。若y不存在，则无事发生，否则将x的父亲节点变为y。

操作完成后，要求对于每个节点计算以每个节点为根节点的子树的大小。

题目的要求可以分为两步，首先需要根据s修改树的结构，接下来对于修改后的树，计算以每个节点为根节点的子树的大小。

其中后面这一步是经典问题，只需从根节点向下一次dfs，对于某个节点x，先递归计算以x的每个孩子为根节点的子树的大小，然后将值累加起来，再加上1即为以x为根节点的子树的大小。

而对于前面这一步，同样可以利用dfs进行求解。为了适配s值相等这一条件，在dfs的过程中可以使用一个哈希表last记录在当前dfs序中，s中的每种字符对应的节点。更具体的说，last的key为每种字符，value为栈，栈中储存的则是当前dfs序中所有s值为key的节点。在dfs的过程中，将x加入到last\[s\[x\]\]的顶部，而当回溯到x时，则将其从last\[s\[x\]\]顶部弹出。

这样一来，对于节点x，last\[s\[x\]\]的栈顶节点就是x最近的且s值相等的节点，此时就可以构造新的树边了。另外需要注意的是，若last\[s\[x\]\]为空，那么说明不存在对应的y，此时应该保留老的树边。

最后附上python代码：

```python
class Solution(object):
    def findSubtreeSizes(self, parent, s):
        """
        :type parent: List[int]
        :type s: str
        :rtype: List[int]
        """
        
        n = len(parent)
        childs = [[] for _ in range(n)]
        for i, fa in enumerate(parent):
            if fa != -1:
                childs[fa].append(i)
        
        new_childs = [[] for _ in range(n)]
        last = {}

        def dfs(now, last, new_childs):
            if s[now] in last and len(last[s[now]]) > 0:
                new_childs[last[s[now]][-1]].append(now)
            else:
                if parent[now] != -1:
                    new_childs[parent[now]].append(now)
                last[s[now]] = []

            last[s[now]].append(now)
            for c in childs[now]:
                dfs(c, last, new_childs)
            last[s[now]].pop()

        dfs(0, last, new_childs)
        
        answer = [0] * n
        def new_dfs(now, answer):
            answer[now] += 1
            for c in new_childs[now]:
                new_dfs(c, answer)
                answer[now] += answer[c]
        
        new_dfs(0, answer)
        return answer
```
