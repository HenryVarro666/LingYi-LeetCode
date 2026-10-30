---
title: "1766. 互质树"
aliases: ["yiduobo的每日leetcode 1766.互质树"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/math", "leetcode/backtracking", "leetcode/number-theory", "题单/链表-二叉树与回溯", "题单/数学算法", "题单/链表-二叉树与回溯/三-一般树", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460771611"
zhihu_id: "460771611"
zhihu_title: "yiduobo的每日leetcode 1766.互质树"
question_id: "1766"
question: "互质树"
problem_url: "https://leetcode.cn/problems/tree-of-coprimes/"
difficulty: "Hard"
rating: 2232
created: "2022-01-22T22:32:33+08:00"
updated: "2022-01-22T22:32:34+08:00"
upvotes: 0
comments: 0
---

# 1766. 互质树

> **[yiduobo的每日leetcode 1766.互质树](https://zhuanlan.zhihu.com/p/460771611) · 知乎 · 2022-01-22 · 赞同 0**
> 力扣：[1766. 互质树](https://leetcode.cn/problems/tree-of-coprimes/) · Hard · 灵茶山艾府：[DFS 中记录节点值的深度和编号，回溯写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1766.互质树

[力扣](https://leetcode-cn.com/problems/tree-of-coprimes/)

题目要求对于树中每个节点node，找出与其距离最近的祖先节点fa，满足nums[node]与nums[fa]互质。

注意到题目中每个节点的数值范围都小于等于50，那么可以从根节点向下bfs，维护从根节点到当前节点这条树链上1到50这些数值最后一次出现的位置。由于是bfs，那么出现的时间越靠后就意味着该节点的深度越深，可以满足题目找出最近祖先节点的需要。

对于当前遍历到的节点，则需要检测该节点值与1到50中的每个数是否互质，如果互质，那么就用这个数字对应的最后一次出现的位置来更新当前节点的答案。全部检测完成后，还需要将该节点也加入到这个1到50的位置数组当中，然后继续向下bfs。

另外，对于50这个范围而言，其中的所有数字都可以写成2^a \* 3^b \* 5^c \* 7^d \* p，其中a、b、c、d为自然数，p等于1或者p是质数。这也就意味着对于1到50中的数，都可以使用5个因子来进行表示，而后续检测互质时就只需要检测这5个因子的共现情况就好了。这里的p取值范围依然有很多，那么在这里就应该将2、3、5、7固定下来。一个自然的想法就是使用4位二进制来表示当前的数是否具有2、3、5、7这个因子，那么一共就有16种情况。而对于p的处理，由于题目要求的是深度最深的祖先节点，因此可以使用一个哈希表candidate来储存当前因子状态为state时可用的候选答案。这里的候选答案的因子状态与state按位与应该等于0。

不过需要特别注意的是，当p不等于1时，若当前数的p与candidate中的p一样，那么也不是互质的。例如22和33，二者的因子状态分别为1000与0100，看上去是互质的，但是由于p都等于11，因此实际上二者并不互质。在这里的处理方法就是对于candidate[state]而言，保留两个p不用的备选答案first和second，其中first的深度大于second的深度。这样一来，对于当前节点而言，若其p值等于first的p值，那么其p值必然不等于second的p值，于是second就是当前节点对应的答案；若其p值不等于first的p值，那么first就是其对应的答案。

有了candidate，就无需再枚举1到50，而是可以直接从candidate中得到答案了。

不过这个优化并不彻底，因为对于candidate的更新依然需要枚举0到15全部的状态。若枚举到的状态index与当前节点的state按位与等于0，说明当前节点可以作为candidate[index]的备选答案。由于当前节点的深度必然是最深的，因此当前节点必然成为新的first。在这里不能直接用老的first作为新的second，因为在这里依然可能出现p值相等的问题，因此还需要检测当前节点的p值与现有老的first的p值是否相同，若相同，那么沿用老的second来作为新的second，否则使用老的first来作为新的second。

这样一来，枚举的复杂度就从50次优化到了16次，也算是比较可观的优化了。实际上，因子的组合并没有16种，因为组合[2, 5, 7]、[3, 5, 7]以及[2, 3, 5, 7]都超出了50的范围，不过我在这里偷懒就没有把这个优化加上了。

最后附上python代码：

```python
class Solution(object):
    def getCoprimes(self, nums, edges):
        """
        :type nums: List[int]
        :type edges: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums)
        g = [set() for _ in range(n)]
        root_candidate = set(range(n))
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        state = [0] * 51
        p = range(51)
        for index in range(1, 51):
            # state[index]表示index是否具有因子2、3、5、7
            if index % 2 == 0:
                state[index] += 1
            if index % 3 == 0:
                state[index] += 2
            if index % 5 == 0:
                state[index] += 4
            if index % 7 == 0:
                state[index] += 8
            tmp = index
            while tmp % 2 == 0:
                tmp /= 2
            while tmp % 3 == 0:
                tmp /= 3
            while tmp % 5 == 0:
                tmp /= 5
            while tmp % 7 == 0:
                tmp /= 7
            p[index] = tmp #计算p值

        # f[i][j]表示i和j的p值是否大于1且相同
        f = [[True] * 51 for _ in range(51)]
        for i in range(1, 50):
            if p[i] > 1:
                for j in range(i, 51):
                    if p[i] == p[j]:
                        f[i][j] = f[j][i] = False

        candidate = {}
        for index in range(16):
            if index & state[nums[0]] == 0:
                candidate[index] = [0, None]
            else:
                candidate[index] = [None, None]

        res = [None] * n
        l = 0
        r = 1
        q = [[0, candidate]]
        res[0] = -1
        while l < r:
            for now_node, candidate in q[l : r]:
                for next_node in g[now_node]:
                    if res[next_node] is not None:
                        continue
                    res[next_node] = -1
                    next_candidate = candidate.copy()
                    first, second = candidate[state[nums[next_node]]]
                    if first is not None:
                        if not f[nums[first]][nums[next_node]]:
                            # first的p值与当前节点的p值相同，因此考虑使用second作为答案
                            if second is not None:
                                res[next_node] = second
                        else:
                            res[next_node] = first

                    for index in range(16):
                        if state[nums[next_node]] & index == 0:
                            first, second = next_candidate[index]
                            if first is not None and not f[nums[first]][nums[next_node]]:
                                # 老first的p值与当前节点的p值相同，那么沿用老的second
                                next_candidate[index] = [next_node, second]
                            else:
                                next_candidate[index] = [next_node, first]
                    
                    q.append([next_node, next_candidate])
            
            l, r = r, len(q)

        return res
```
