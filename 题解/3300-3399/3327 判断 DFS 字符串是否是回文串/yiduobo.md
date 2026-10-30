---
title: "3327. 判断DFS字符串是否是回文串"
aliases: ["yiduobo的每日leetcode 3327.判断DFS字符串是否是回文串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/string", "题单/链表-二叉树与回溯", "题单/字符串", "题单/链表-二叉树与回溯/三-一般树", "题单/字符串/三-Manacher-算法-回文串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2782213686"
zhihu_id: "2782213686"
zhihu_title: "yiduobo的每日leetcode 3327.判断DFS字符串是否是回文串"
question_id: "3327"
question: "判断 DFS 字符串是否是回文串"
problem_url: "https://leetcode.cn/problems/check-if-dfs-strings-are-palindromes/"
difficulty: "Hard"
rating: 2454
created: "2024-10-24T00:11:00+08:00"
updated: "2024-10-24T00:11:00+08:00"
upvotes: 0
comments: 0
---

# 3327. 判断DFS字符串是否是回文串

> **[yiduobo的每日leetcode 3327.判断DFS字符串是否是回文串](https://zhuanlan.zhihu.com/p/2782213686) · 知乎 · 2024-10-24 · 赞同 0**
> 力扣：[3327. 判断 DFS 字符串是否是回文串](https://leetcode.cn/problems/check-if-dfs-strings-are-palindromes/) · Hard · 灵茶山艾府：[【模板】DFS 时间戳 + Manacher 算法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3327.判断DFS字符串是否是回文串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-dfs-strings-are-palindromes/description/)

给出一颗n个节点的树，节点的编号为0到n - 1，根节点为节点0。这棵树由一个长度为n的数组parent表示，其中parent[i]为节点i的父节点，特别的，parent[0] \= -1。另外给出一个长度为n的字符串s，其中s[i]表示节点i对应的节点。

接下来，定义一个空字符串dfsStr，然后从根节点开始向下dfs。对于当前遍历到的节点x，先按照节点编号升序遍历x的所有孩子y，并递归调用dfs(y)，然后将s[x]添加到dfsStr的末尾。

现在需要求出一个长度为n的布尔数组answer，对于0到n - 1之间的每个下标i，需要先清空dfsStr并调用dfs(i)重新填充dfsStr，若此时的dfsStr是回文串，那么answer[i]为true，否则answer[i]为false。

题目的数据规模非常大，不可能真的对于每个节点都清空dfsStr然后再次做dfs填充dfsStr，那么在这里就需要先考察每个节点的dfsStr与整颗树的dfsStr的关系。

根据dfsStr的定义可以发现，以每个节点开始的dfsStr的长度必然为以这个节点为根的子树中节点的数量，另外在对当前节点进行dfs的过程中，节点遍历的顺序与dfs整颗树进行dfs时节点遍历的顺序是一致的，也就是说对于任意节点x，通过dfs(x)形成的dfsStr必然是通过dfs(0)形成的dfsStr的一个子串。

换言之，问题就转化成了对于dfs(0)生成的字符串dfsStr，其中某个特定子串是否为回文串的问题。对于这个问题，可以参考之前的第5题，通过马拉车算法先计算出dfsStr中以每个字符为中心的最长回文半径。需要注意这里可能存在长度为偶数的回文串，因此需要先对dfsStr做一些调整。

[yiduobo：yiduobo的每日leetcode 5.最长回文子串](https://zhuanlan.zhihu.com/p/113060786)

接下来对于树中的某个节点x，可以在dfs过程中记录每个节点在dfsStr中对应的位置left[x]，以及以x为根节点的子树中的节点数量size[x]，那么dfs(x)对应的dfsStr就是整棵树的dfsStr中起点在left[x]，终点在left[x] + size[x] - 1这个子串。计算出这个字符串的中心位置，然后判断对应的回文半径是否覆盖住整个子串即可。

最后附上python代码：

```python
class Solution(object):
    def findAnswer(self, parent, s):
        """
        :type parent: List[int]
        :type s: str
        :rtype: List[bool]
        """
        
        n = len(parent)
        childs = [[] for _ in range(n)]
        root = None
        size = [0] * n
        left = [0] * n
        dfs_list = []

        for index in range(n - 1, -1, -1):
            fa = parent[index]
            if fa == -1:
                root = index
            else:
                childs[fa].append(index)
        
        def dfs(now):
            size[now] += 1
            left[now] = len(dfs_list)
            dfs_list.append(s[now])
            for c in childs[now]:
                dfs(c)
                size[now] += size[c]
            
            print now, size[now]
        
        dfs(root)
        
        expand_list = ['!']
        for char in dfs_list:
            expand_list.append(char)
            expand_list.append('#')
        expand_list[-1] = '@'

        f = [0]
        mid = 0
        right = 0
        for index in range(1, len(expand_list) - 1):
            if index < right:
                f.append(min(f[2 * mid - index], right - index))
            else:
                f.append(1)
            
            while expand_list[index - f[index]] == expand_list[index + f[index]]:
                f[index] += 1
            if right < index + f[index]:
                right = index + f[index]
                mid = index

        res = []
        for index in range(n):
            left_in_expand = left[index] * 2 + 1
            right_in_expand = (left[index] + size[index] - 1) * 2 + 1
            mid_in_expand = (left_in_expand + right_in_expand) // 2
            if mid_in_expand - f[mid_in_expand] + 1 <= left_in_expand:
                res.append(True)
            else:
                res.append(False)
        
        return res
```
