---
title: "2791. 树中可以形成回文的路径数"
aliases: ["yiduobo的每日leetcode 2791.树中可以形成回文的路径数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/tree", "leetcode/depth-first-search", "leetcode/bitmask", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/一-前缀和", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/656832093"
zhihu_id: "656832093"
zhihu_title: "yiduobo的每日leetcode 2791.树中可以形成回文的路径数"
question_id: "2791"
question: "树中可以形成回文的路径数"
problem_url: "https://leetcode.cn/problems/count-paths-that-can-form-a-palindrome-in-a-tree/"
difficulty: "Hard"
rating: 2677
created: "2023-09-18T06:03:35+08:00"
updated: "2023-09-18T06:03:35+08:00"
upvotes: 0
comments: 0
---

# 2791. 树中可以形成回文的路径数

> **[yiduobo的每日leetcode 2791.树中可以形成回文的路径数](https://zhuanlan.zhihu.com/p/656832093) · 知乎 · 2023-09-18 · 赞同 0**
> 力扣：[2791. 树中可以形成回文的路径数](https://leetcode.cn/problems/count-paths-that-can-form-a-palindrome-in-a-tree/) · Hard · 灵茶山艾府：[状态压缩+两数异或（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2791.树中可以形成回文的路径数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-paths-that-can-form-a-palindrome-in-a-tree/)

首先，异构回文问题存在一个经典的转化，因为异构回文串只需保证字符串中出现次数为奇数的字符数量不超过1个，那么就可以通过奇偶性编码，将其进行状态压缩。

更具体的，对于一个字符串，使用大小为2^26的编码来表示这个字符串中每种字符的奇偶性，其中'a'对应到第0位，'b'对应到第1位，依次类推。而某个字符如果出现了奇数次，那么对应位上就是1，否则就是0。

对于这样的二进制编码，就可以通过按位异或的操作来计算两个字符串拼接后各个字符出现次数的奇偶性。另一方面，对于编码为2的幂的串，则说明这是一个异构回文串，也就是题目要找的合法路径。

除此之外，本题的路径也可以从常规的两点之间的路径，变更为一个点到根节点，再到另一个点的路径。具体来说，常规的两点间路径是x - lca(x, y) - y，而对于本题，则可以变为x - lca(x, y) - root - lca(x, y) - y，其中多出了一正一反两段lca(x, y)与root之间的路径，但是由于经过的字母都是成对出现，因此不会影响最终答案。

根据上面两个结论，问题就可以转化成对于树中所有从根节点到某个节点的路径形成的字符串对应的状态编码，求在树中还存在多少个相同，或者仅有一个二进制位上不同的，从根节点到另一个节点的路径形成的字符串对应的状态编码。

文字描述看上去比较绕，具体实现上，只需从根节点出发向下进行dfs，并使用一个哈希表储存当前已遍历过的所有路径形成的编码以及出现次数。

对于当前节点now，遍历now的所有孩子节点child：

1、通过now到child这条边上的字符char以及根节点到now的字符串对应的编码v，计算出根节点到child的字符串对应的编码next_v

2、从哈希表中查找next_v出现的次数并更新答案

3、枚举落单字符'a'到'z'并计算next_v与其异或后的结果，并查找这个结果在哈希表中出现的次数然后更新答案

4、更新哈希表中next_v出现的次数

5、递归求解子节点child，需要注意此时child对应的v应该是next_v

最后附上pyton代码：

```python
class Solution(object):
    def countPalindromePaths(self, parent, s):
        """
        :type parent: List[int]
        :type s: str
        :rtype: int
        """

        n = len(parent)
        g = {index : set() for index in range(n)}
        for index in range(1, n):
            g[parent[index]].add(index)

        global res
        res = 0

        cnt = {0 : 1}

        def dfs(now, v):
            global res
            for child in g[now]:
                next_v = v ^ (1 << (ord(s[child]) - 97))
                res += cnt.get(next_v, 0)
                for single in range(26):
                    res += cnt.get(next_v ^ (1 << single), 0)
                cnt[next_v] = cnt.get(next_v, 0) + 1
                dfs(child, next_v)
        
        dfs(0, 0)
        return res
```
