---
title: "2322. 从树中删除边的最小分数"
aliases: ["yiduobo的每日leetcode 2322.从树中删除边的最小分数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/enumeration", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/557488726"
zhihu_id: "557488726"
zhihu_title: "yiduobo的每日leetcode 2322.从树中删除边的最小分数"
question_id: "2322"
question: "从树中删除边的最小分数"
problem_url: "https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/"
difficulty: "Hard"
rating: 2392
created: "2022-08-24T23:22:26+08:00"
updated: "2022-08-24T23:22:26+08:00"
upvotes: 0
comments: 0
---

# 2322. 从树中删除边的最小分数

> **[yiduobo的每日leetcode 2322.从树中删除边的最小分数](https://zhuanlan.zhihu.com/p/557488726) · 知乎 · 2022-08-24 · 赞同 0**
> 力扣：[2322. 从树中删除边的最小分数](https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/) · Hard · 灵茶山艾府：[DFS 时间戳——处理树上问题的有力工具（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2322.从树中删除边的最小分数

[力扣](https://leetcode.cn/problems/minimum-score-after-removals-on-a-tree/)

在一棵树中删除两条边之后，树一定会被分成三个部分。除了原始根节点所在的这一部分外，还会得到另外两个新的子树。

对于本题，枚举删除的两条边需要对两条边是否具有公共节点进行特殊判断，相对比较麻烦，不妨直接枚举最终新多出来的两棵树的根节点再计算分数。

不妨设新多出来的两棵树的根节点分别为x和y，那么有三种情况：

1、在原始的树中，y位于以x为根节点的子树中。

对于这种情况，拆分后以y为根节点的新树与原始树中以y为根节点的子树完全一致。

以x为根节点的新树则相当于原始树中以x为根节点的子树，再去除掉以y为根节点的子树。

例如在样例2中，在x等于1，y等于2时，以y为根节点的新树就是

2 - 5

而以x为根节点的新树则是在原始的子树

1

/ \\

2 3

/ \\

5 4

的基础上去掉了左边的2 - 5，剩下的是1 - 3 - 4

最后，原始的树则还剩下去除掉以x为根节点的部分。

令f[i]表示在原始的树中，以i为根节点的子树中所有节点的异或值，那么以y为根节点的新子树的异或值不变，还是f[y]。以x为根节点的新子树的异或值则应该在f[x]的基础上去掉f[y]，也就是f[x] ^ f[y]。最后，原始的树剩下的部分的异或值就是f[0] ^ f[x] ^ f[y]。

此时的得分就是三者中的最大值减去最小值。

2、在原始的树中，x位于以y为根节点的子树中。

此时与情况1完全对称，三个新子树的异或值分别为f[x]、f[x] ^ f[y]、f[0] ^ f[x] ^ f[y]

3、在原始的树中，x和y都不在以另一方为根节点的子树中。

对于这种情况，以x和y为根节点的新子树与原始的子树完全一致，而原始的树剩下的部分则是去除掉以x和y的为根节点的子树后剩下的部分，那么三棵新子树的异或值分别为f[x]、f[y]、f[0] ^ f[x] ^ f[y]

到了这里，就基本上有算法的雏形了，但是还有两个问题需要解决。第一个是f应该如何计算得到，第二个是如何高效判断x和y是否位于以另一方为根节点的子树中。

首先是第一个问题，如何计算f。

在这里可以使用经典的树形动态规划。对于f[now]，先分别递归求解now的左右子树，得到f[now.left]以及f[now.right]，那么f[now]就等于f[now.left] ^ f[now.right] ^ nums[now]

接下来是第二个问题，如果判断x和y是否位于以另一方为根节点的子树中。

对于这个问题，可以先引入一个概念dfs序。例如样例2中的树，如果假设在节点1时先对节点2进行了dfs，那么最终的dfs序就是

0->1->2->5->5->2->3->4->4->3->1->0

也就是说，在进行dfs时，首次来到某个节点，以及从某个节点离开时，都将这个节点加入到这个序列中，最终得到的一个节点序列。

可以发现，在这个序列中每个节点都出现了两次，分别使用left和right表示，那么对于x而言，在left[x]和right[x]之间的序列中的所有节点，必然都属于以x为根节点的子树。那么对于判断y是否属于以x为根节点的子树，就只需要判断left[y]是否满足left[x] \< left[y] \< right[x]即可。同样的，如果要判断x是否属于以y为根节点的子树，只需要判断left[x]是否满足left[y] \< left[x] \< right[y]。

而为了得到这个dfs序，则可以在递归计算f的同时顺便进行计算。

到了这里，就得到完整的算法。

令f[i]表示以i为根节点的子树中所有节点值的异或值，left[i]和right[i]表示节点i在dfs序中第一次和最后一次出现的位置。接下来从0节点开始递归求解f，在过程中顺便求解left和right。

求解完成后，枚举新子树的根节点x和y，通过left[x]、right[x]、left[y]、right[y]四者的大小关系判断x和y是否属于以对方为根节点的子树，然后根据具体的情况计算三棵新子树对应的异或值并计算分数。取所有分数中的最小值作为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minimumScore(self, nums, edges):
        """
        :type nums: List[int]
        :type edges: List[List[int]]
        :rtype: int
        """

        n = len(nums)
        g = {}
        for x, y in edges:
            if x not in g:
                g[x] = set()
            if y not in g:
                g[y] = set()
            g[x].add(y)
            g[y].add(x)
        
        used = set([0])
        f = nums[:]
        left = [0] * n
        right = [0] * n

        self.timestamp = 0
        def dfs(now):
            self.timestamp += 1
            left[now] = self.timestamp

            for next in g.get(now, set()):
                if next not in used:
                    used.add(next)
                    dfs(next)
                    f[now] ^= f[next]
            
            self.timestamp += 1
            right[now] = self.timestamp

        dfs(0)
        
        res = None
        for x in range(1, n - 1):
            for y in range(x + 1, n):
                if left[x] < left[y]:
                    if left[y] < right[x]:
                        part1 = f[y]
                        part2 = f[x] ^ f[y]
                        part3 = f[0] ^ f[x]
                    else:
                        part1 = f[x]
                        part2 = f[y]
                        part3 = f[0] ^ f[x] ^ f[y]
                elif left[x] < right[y]:
                    part1 = f[x]
                    part2 = f[x] ^ f[y]
                    part3 = f[0] ^ f[y]
                else:
                    part1 = f[x]
                    part2 = f[y]
                    part3 = f[0] ^ f[x] ^ f[y]

                diff = max(part1, part2, part3) - min(part1, part2, part3)
                if res is None or res > diff:
                    res = diff
        
        return res
```
