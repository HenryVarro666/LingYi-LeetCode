---
title: "2509. 查询树中环的长度"
aliases: ["yiduobo的每日leetcode 2509.查询树中环的长度"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/链表-二叉树与回溯", "题单/位运算", "题单/链表-二叉树与回溯/二-二叉树", "题单/位运算/八-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/634314615"
zhihu_id: "634314615"
zhihu_title: "yiduobo的每日leetcode 2509.查询树中环的长度"
question_id: "2509"
question: "查询树中环的长度"
problem_url: "https://leetcode.cn/problems/cycle-length-queries-in-a-tree/"
difficulty: "Hard"
rating: 1948
created: "2023-06-04T21:48:00+08:00"
updated: "2023-06-04T21:48:00+08:00"
upvotes: 0
comments: 0
---

# 2509. 查询树中环的长度

> **[yiduobo的每日leetcode 2509.查询树中环的长度](https://zhuanlan.zhihu.com/p/634314615) · 知乎 · 2023-06-04 · 赞同 0**
> 力扣：[2509. 查询树中环的长度](https://leetcode.cn/problems/cycle-length-queries-in-a-tree/) · Hard · 灵茶山艾府：[最近公共祖先 + 位运算优化时间复杂度（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2509.查询树中环的长度

[力扣](https://leetcode.cn/problems/cycle-length-queries-in-a-tree/)

题目给出一系列的询问，对于每个询问中的两个节点，在二者之间添加一条边的话，求形成的环的长度是多少，然后再将这条边删去，也就是将树恢复原状。

对于一组询问(a, b)，观察题目中环的组成，可以将其拆分成三个部分，分别为新添加的这条边，从a到二者lca的树链，以及从b到二者lca的树链构成。而对于这两条树链的长度，则可以通过lca的在树中的层级与a和b在树中的层级分别作差得到。

到了这里，问题就转化成了给出若干组询问，求解询问中两点的lca。对于这个问题，则可以套用经典的dfs计算欧拉序，然后将其转化为区间查询问题利用线段树或者st算法进行求解。

不过对于本题，还存在更巧妙的处理方法。注意题目给出的是一颗完全二叉树，这也就意味着题目给出的树中所有节点是根据其编号唯一确定的。

基于这一点，不妨思考一下树中两个编号分别为x、y的节点的lca应该如何求解，在这里先假设x \< y。

首先，y在这里的层级必然是大于等于x的层级的，注意题目给出的树中节点的编号与层级的关系，可以发现，第k层节点的二进制表示的位数恰好就是其所在的层级数，那么在这里就可以先将y往上移动若干层，直到x与这个新的y位于同一层。

另一方面，每个节点的父节点其二进制表示恰好就是当前节点二进制表示右移一位，因此将y往上提升k层，就相当于将y右移k位，这里的k等于y的二进制表示长度减去x的二进制表示长度。到了这里，x和y就位于同一层级了。

若此时的x与y相同，说明当前节点就是二者的lca，而最终环的长度就是y向上移动的这k层，再加上1，表示额外添加的这条边。

若x与y不同，则需要继续将x和y向上移动，直到来动同一个节点。当然，在这里不能模拟这个移动过程，否则时间复杂度就太高了，不妨继续从二进制的角度来考虑问题。从x除最高位外的首位开始向后遍历，同时使用一个指针从根节点开始向下移动。若当前位为0，就相当于指针向左子树行走，否则就相当于指针向右子树行走。

可以发现，每个节点在树中的位置完全取决于其数值的二进制表示，而这些节点的祖先节点则恰好是二进制表示的某个前缀。到了这里，lca问题就变成了最长公共前缀的问题。

对于本题，同样也无需真正求解lca，而是只需知道其长度，就可以通过对x或y执行右移操作来得到这个lca。具体来说，可以执行一次异或操作，那么公共前缀将会变成0消失掉，而对于剩下的位数就是x或y需要消除掉的。此时只需将x或y右移之前异或结果的位数，就得到了二者的lca。

最后，计算lca的二进制表示长度与x以及y二进制长度之差，再加上y向上移动的这k层，以及额外添加的边的1，就得到了环的长度。

最后附上python代码：

```python
class Solution(object):
    def cycleLengthQueries(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        res = []
        for x, y in queries:
            if x > y:
                x, y = y, x
            
            len_diff = len(bin(y)) - len(bin(x))
            res.append(len_diff + 1)

            y >>= len_diff

            if x == y:
                lca = x
            else:
                lca = x >> (len(bin(x ^ y)) - 2)
            res[-1] += (len(bin(x)) - len(bin(lca))) * 2
        
        return res
```
