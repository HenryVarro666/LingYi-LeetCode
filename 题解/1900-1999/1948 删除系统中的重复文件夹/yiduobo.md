---
title: "1948. 删除系统中的重复文件夹"
aliases: ["yiduobo的每日leetcode 1948.删除系统中的重复文件夹"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/trie", "leetcode/hash-table", "leetcode/backtracking", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/491707586"
zhihu_id: "491707586"
zhihu_title: "yiduobo的每日leetcode 1948.删除系统中的重复文件夹"
question_id: "1948"
question: "删除系统中的重复文件夹"
problem_url: "https://leetcode.cn/problems/delete-duplicate-folders-in-system/"
difficulty: "Hard"
rating: 2534
created: "2022-04-01T21:08:56+08:00"
updated: "2022-04-01T21:08:56+08:00"
upvotes: 0
comments: 0
---

# 1948. 删除系统中的重复文件夹

> **[yiduobo的每日leetcode 1948.删除系统中的重复文件夹](https://zhuanlan.zhihu.com/p/491707586) · 知乎 · 2022-04-01 · 赞同 0**
> 力扣：[1948. 删除系统中的重复文件夹](https://leetcode.cn/problems/delete-duplicate-folders-in-system/) · Hard · 灵茶山艾府：[括号表示法 + 字典树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1948.删除系统中的重复文件夹

[力扣](https://leetcode-cn.com/problems/delete-duplicate-folders-in-system/)

题目非常贴心地用树形表示了文件路径，那么很自然可以想到使用trie树来组织这些文件夹，然后转化成树中重复子树的问题。

构建trie树的过程比较常规，这里就略过了。

对于树中重复子树的问题，之前也遇到过一个简化版本的，是关于二叉树的重复子树问题。

[yiduobo：yiduobo的每日leetcode 652.寻找重复的子树](https://zhuanlan.zhihu.com/p/278508148)

需要注意的是，本题是一颗多叉树，而且树中节点值是字符串，因此在构造子树表示的时候需要按一定的顺序将子树的值组织起来。

具体做法与上面这题类似，从根节点开始向下dfs，先递归构造子树的表示并收集起来。接下来按照孩子节点值排序后将子树的表示组织成一个完整的字符串，用来表示当前的树。

全部构造完成后，使用哈希表判断哪些子树重复了，并将这些子树标记好。

最后从根节点开始进行bfs。对于当前节点，遍历其孩子节点，若其已经被标记过，那么就跳过该节点，否则将其加入bfs队列中并更新答案。

最后附上python代码：

```
class Trie(object):

    def __init__(self):
        self.childs = {}

class Solution(object):
    def deleteDuplicateFolder(self, paths):
        """
        :type paths: List[List[str]]
        :rtype: List[List[str]]
        """

        root = Trie()
        for path in paths:
            now = root
            for val in path:
                if val not in now.childs:
                    now.childs[val] = Trie()
                now = now.childs[val]

        tree_dict = {}
        self.res = []
        self.dfs(root, tree_dict)
        remove_set = set()
        for key in tree_dict:
            if len(tree_dict[key]) > 1:
                for node in tree_dict[key]:
                    remove_set.add(node)
        
        q = [[root, []]]
        l = 0
        r = 1
        res = []
        while l < r:
            now, path = q[l]
            l += 1
            for child, next in now.childs.items():
                if next not in remove_set:
                    tmp = path[:]
                    tmp.append(child)
                    q.append([next, tmp])
                    r += 1
                    res.append(tmp)
        
        return res

    def dfs(self, now, tree_dict):
        tree_key = {}
        for child in now.childs:
            tree_key[child] = self.dfs(now.childs[child], tree_dict)

        if tree_key != {}:
            key_str = '(' + ''.join([tree_key[key] + key for key in sorted(tree_key.keys())]) + ')'
            if key_str not in tree_dict:
                tree_dict[key_str] = []
            tree_dict[key_str].append(now)
            return key_str

        return ''
```
