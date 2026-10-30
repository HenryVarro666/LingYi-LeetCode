---
title: "642. 设计搜索自动补全系统"
aliases: ["yiduobo的每日leetcode 642.设计搜索自动补全系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/602999450"
zhihu_id: "602999450"
zhihu_title: "yiduobo的每日leetcode 642.设计搜索自动补全系统"
question_id: "642"
question: "设计搜索自动补全系统"
problem_url: "https://leetcode.cn/problems/design-search-autocomplete-system/"
created: "2023-02-02T22:46:30+08:00"
updated: "2023-02-02T22:46:30+08:00"
upvotes: 0
comments: 0
---

# 642. 设计搜索自动补全系统

> **[yiduobo的每日leetcode 642.设计搜索自动补全系统](https://zhuanlan.zhihu.com/p/602999450) · 知乎 · 2023-02-02 · 赞同 0**
> 力扣：[642. 设计搜索自动补全系统](https://leetcode.cn/problems/design-search-autocomplete-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

642.设计搜索自动补全系统

[力扣](https://leetcode.cn/problems/design-search-autocomplete-system/)

题目的搜索自动补全是基于字符串前缀来做的，因此在这里可以使用trie树来维护这些字符串。

对于trie树中的节点，除了最常规的哈希表childs用来记录孩子节点外，还需要以下组件：

1、weight，用来记录当前字符串被搜索的次数

2、s，用来记录当前节点对应的字符串

3、fa，用来记录当前节点的父亲节点。在这里需要fa的原因是在input时，只有当某个字符串被输入完之后才会更新trie树。对于这个更新过程如果想自底向上来执行的话就需要记录每个节点的父亲节点。

自底向上相比于自顶向下更新有一个好处是当出现当前输入的字符串的搜索次数排不进前三的时，就无须继续向上更新了。

4、top，用来记录当前节点为前缀的被搜索次数最多的三个字符串对应的节点。在这里也可以直接记录具体的字符串以及搜索次数，不过在这里记录节点更新起来会稍微方便点

接下来，对于补全系统的各个操作：

1、初始化：

首先，初始化trie树的根节点root。

接下来按下标对应的关系遍历所有的sentences和times，对于当前遍历到的sentences[i]，将其加入到trie树中，同时使用times[i]来更新其末尾字符对应的节点。处理完成后，从某尾节点开始自底向上更新路径上节点对应的top。

需要注意的是，在使用当前字符串和搜索次数更新祖先节点的top时，可能出现当前符串已经出现在top中的情况，需要注意具体的调整方法。

处理完所有字符串后，还需要初始化一个变量p指向root，这里的p是用来记录处理当前的input操作时位于trie树中的哪个节点

2、input：

若当前输入的字符为\#，说明当前字符串已经到头，此时应该将p对应的weight加上1，然后从p开始向上更新top，最后将p重新指回到root并返回空数组

若当前输入的字符不是\#，那么就将p迭代到p对应字符的孩子节点，若不存在对应的节点则需要额外创建出这个节点。接下来，将p的top对应的s加入到答案中并返回

最后附上python代码：

```python
class TreeNode(object):

    def __init__(self, s, fa):
        self.s = s
        self.childs = {}
        self.top = [None, None, None]
        self.fa = fa
        self.weight = 0

class AutocompleteSystem(object):

    def __init__(self, sentences, times):
        """
        :type sentences: List[str]
        :type times: List[int]
        """
        self.root = TreeNode('', None)
        self.p = self.root
        for s, t in zip(sentences, times):
            now = self.root
            for char in s:
                if char not in now.childs:
                    tmp = TreeNode(now.s + char, now)
                    now.childs[char] = tmp
                now = now.childs[char]
            
            now.weight += t
            self.update(now)

    def update(self, now):
        p = now
        while now != None:
            if now.top[0] == p:
                pass
            elif now.top[1] == p:
                if now.top[0].weight < p.weight or (now.top[0].weight == p.weight and now.top[0].s > p.s):
                    now.top[0], now.top[1] = now.top[1], now.top[0]
            elif now.top[2] == p:
                if now.top[0].weight < p.weight or (now.top[0].weight == p.weight and now.top[0].s > p.s):
                    now.top[0], now.top[1], now.top[2] = now.top[2], now.top[0], now.top[1]
                elif now.top[1].weight < p.weight or (now.top[1].weight == p.weight and now.top[1].s > p.s):
                    now.top[1], now.top[2] = now.top[2], now.top[1]
            elif now.top[0] is None or now.top[0].weight < p.weight or (now.top[0].weight == p.weight and now.top[0].s > p.s):
                now.top[0], now.top[1], now.top[2] = p, now.top[0], now.top[1]
            elif now.top[1] is None or now.top[1].weight < p.weight or (now.top[1].weight == p.weight and now.top[1].s > p.s):
                now.top[1], now.top[2] = p, now.top[1]
            elif now.top[2] is None or now.top[2].weight < p.weight or (now.top[2].weight == p.weight and now.top[2].s > p.s):
                now.top[2] = p
            else:
                break
            
            now = now.fa
            
    def input(self, c):
        """
        :type c: str
        :rtype: List[str]
        """
        if c == '#':
            self.p.weight += 1
            self.update(self.p)
            self.p = self.root
            return []
        else:
            if c not in self.p.childs:
                tmp = TreeNode(self.p.s + c, self.p)
                self.p.childs[c] = tmp
            self.p = self.p.childs[c]

            res = []
            for node in self.p.top:
                if node is not None:
                    res.append(node.s)
            
            return res

# Your AutocompleteSystem object will be instantiated and called as such:
# obj = AutocompleteSystem(sentences, times)
# param_1 = obj.input(c)
```
