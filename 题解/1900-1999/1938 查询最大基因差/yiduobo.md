---
title: "1938. 查询最大基因差"
aliases: ["yiduobo的每日leetcode 1938.查询最大基因差"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/trie", "题单/常用数据结构", "题单/常用数据结构/六-字典树-trie", "题单/常用数据结构/专题-离线算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/489139951"
zhihu_id: "489139951"
zhihu_title: "yiduobo的每日leetcode 1938.查询最大基因差"
question_id: "1938"
question: "查询最大基因差"
problem_url: "https://leetcode.cn/problems/maximum-genetic-difference-query/"
difficulty: "Hard"
rating: 2503
created: "2022-03-28T19:10:25+08:00"
updated: "2022-03-28T19:10:26+08:00"
upvotes: 0
comments: 0
---

# 1938. 查询最大基因差

> **[yiduobo的每日leetcode 1938.查询最大基因差](https://zhuanlan.zhihu.com/p/489139951) · 知乎 · 2022-03-28 · 赞同 0**
> 力扣：[1938. 查询最大基因差](https://leetcode.cn/problems/maximum-genetic-difference-query/) · Hard · 灵茶山艾府：[离线+字典树](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1938.查询最大基因差

[力扣](https://leetcode-cn.com/problems/maximum-genetic-difference-query/)

题目给出一棵树以及若干询问[node, v]。对于询问[node, v]，要求查询从树中根节点到node的路径中，与v异或结果的最大值。

对于这类若干个数求异或最值的问题，常规做法是将路径上的数的二进制表示加入到trie树中，然后根据v的二进制表示在trie树中行走，从而找出最大的结果。之前的1707题与本题比较类似，题解中比较详细地阐述了使用trie树求解结果的过程，这里就不展开了。

[yiduobo：yiduobo的每日leetcode 1707.与数组中元素的最大异或值](https://zhuanlan.zhihu.com/p/449610412)

但是在这里还存在一个问题是，题目要求的是树中根节点到node路径上的值与v的异或，因此对于每次询问，trie树的结构也可能不一样。如果每次都重新构造，那还不如不要trie树比较好。

注意到这里的使用的是根节点到node路径上的值构造trie树，那么对于node而言，设其父亲节点为fa，那么就可以在根节点到fa构造的trie树的基础上，再加入node自身二进制表示的结果，从而得到想要的从根节点到node的trie树。

为了有效利用父亲节点已经构造好的trie树，那么就有必要使用离线算法，先将所有的询问收集起来，并按node分别储存。接下来从根节点开始向下dfs，对于当前节点now：

1、首先将now.val的二进制表示加入到当前trie树中

2、接下来对于收集到的关于now的所有询问，分别在trie树中行走求解并更新对应询问的答案

3、递归求解now的所有孩子节点，此时的trie树也可以方便孩子节点的求解

4、递归回溯，此时需要注意的是其他节点的求解已经不应该继续使用now.val相关的信息了，因此需要将now.val的二进制表示从trie树中删去

最后附上python代码：

```python
class Trie(object):
    def __init__(self):
        self.child = [None, None]
        self.weight = 0

class Solution(object):
    def maxGeneticDifference(self, parents, queries):
        """
        :type parents: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(parents)
        root = None

        g = {x : set() for x in range(n)}
        for index, fa in enumerate(parents):
            if fa == -1:
                root = index
            else:
                g[fa].add(index)

        max_num = n
        query_dict = {}
        for index, [node, val] in enumerate(queries):
            if node not in query_dict:
                query_dict[node] = []
            query_dict[node].append([index, val])
            max_num = max(max_num, val)

        pow2 = [1]
        while pow2[-1] <= max_num:
            pow2.append(pow2[-1] + pow2[-1])
        pow2.reverse()
        
        res = [0] * len(queries)
        trie = Trie()
        self.dfs(root, g, trie, query_dict, res, pow2)
        return res
    
    def dfs(self, now, g, trie, query_dict, res, pow2):
        tmp = now
        p = trie
        for pow_val in pow2:
            if tmp >= pow_val:
                v = 1
                tmp -= pow_val
            else:
                v = 0
        
            if p.child[v] is None:
                p.child[v] = Trie()
            
            p = p.child[v]
            p.weight += 1
        
        if now in query_dict:
            for index, val in query_dict[now]:
                p = trie
                s = 0
                for pow_val in pow2:
                    if val >= pow_val:
                        v = 1
                        val -= pow_val
                    else:
                        v = 0
                    
                    if p.child[1 - v] is not None and p.child[1 - v].weight > 0:
                        s += pow_val
                        p = p.child[1 - v]
                    else:
                        p = p.child[v]
                
                res[index] = s
            
        for next in g[now]:
            self.dfs(next, g, trie, query_dict, res, pow2)
        
        tmp = now
        p = trie
        for pow_val in pow2:
            if tmp >= pow_val:
                v = 1
                tmp -= pow_val
            else:
                v = 0
            
            p = p.child[v]
            p.weight -= 1
```
