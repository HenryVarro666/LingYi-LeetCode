---
title: "2440. 创造价值相同的连通块"
aliases: ["yiduobo的每日leetcode 2440.创造价值相同的连通块"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/tree", "leetcode/depth-first-search", "leetcode/math", "leetcode/enumeration", "leetcode/number-theory", "leetcode/dfs", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/三-一般树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584113374"
zhihu_id: "584113374"
zhihu_title: "yiduobo的每日leetcode 2440.创造价值相同的连通块"
question_id: "2440"
question: "创建价值相同的连通块"
problem_url: "https://leetcode.cn/problems/create-components-with-same-value/"
difficulty: "Hard"
rating: 2460
created: "2022-11-17T00:12:24+08:00"
updated: "2022-11-17T00:12:24+08:00"
upvotes: 0
comments: 0
---

# 2440. 创造价值相同的连通块

> **[yiduobo的每日leetcode 2440.创造价值相同的连通块](https://zhuanlan.zhihu.com/p/584113374) · 知乎 · 2022-11-17 · 赞同 0**
> 力扣：[2440. 创建价值相同的连通块](https://leetcode.cn/problems/create-components-with-same-value/) · Hard · 灵茶山艾府：[枚举答案 + DFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2440.创造价值相同的连通块

[力扣](https://leetcode.cn/problems/create-components-with-same-value/)

题目给出一棵树，要求将其分成若干个连通块，每个连通块中节点值之和相等。

注意到树中节点值都很小，整棵树所有节点之和最大也只有一百万，而在小于等于一百万的整数中，约数最多的应该是720720，总共也仅有240个约数，也就是说，在这里完全可以枚举最终树被切分成了多少块，然后计算出这种切分方式下每个块的值是多少并检测能否得到可行的切分方式。由于每个块的值必须相同，也就是说树中节点总和必须是块数的倍数，因此在这里检测的次数不会超过240次，只需要找出一种能在O(n)或者O(nlogn)时间内判断能否将树切分成指定块数的算法就行了。

接下来考虑如何切分。不妨设当前切分的目标是每个块中节点之和为target，那么对于树中的某个叶子节点now，一共有三种情况：

1、该节点的值nums[now] > target

这种情况下，不存在合法的切分

2、该节点的值nums[now] \= target

此时应该将now独立成块，然后考虑其他的节点

3、该节点的值nums[now] \< target

此时该节点必须并入其父节点所在的连通块，否则连通块中节点的值是不够的

根据上面对叶子节点的处理方式，就可以得到处理一般节点的方法。对于某个非叶子节点now，可以先递归求解其所有孩子节点。

若其中某个孩子所在连通块的节点值之和大于target，那么说明不存在合法的切分。

反之，若所有孩子所在连通块的节点值之和都小于等于target，那么就必须将所有节点值之和小于target的孩子所在连通块并入now所在的连通块，此时就可以通过nums[now]以及这些孩子节点所在连通块之和计算now所在连通块节点值之和，接下来根据这个和与target的关系，就对应回了处理叶子节点的三种情况中。

综合上面两种情况，就有了一种递归的做法。对于每个节点，先递归求解其所有孩子节点，通过其返回的连通块节点值之和判断其是否能独立成块，并将不能独立成块的孩子节点所在的连通块并入当前节点。接下来考虑当前节点所在的连通块能否独立成块，若可以，则向上返回0，否则返回当前节点所在连通块的节点值之和。

若最终返回的结果为0，说明找到了可行的切分方案，否则说明没有可行的方案，需要继续尝试下一种target。

最后附上python代码：

```python
class Solution(object):
    def componentValue(self, nums, edges):
        """
        :type nums: List[int]
        :type edges: List[List[int]]
        :rtype: int
        """

        s = sum(nums)
        n = len(nums)
        g = {index : set() for index in range(n)}
        for x, y in edges:
            g[x].add(y)
            g[y].add(x)

        def check(now, fa, v):
            val = nums[now]
            for next in g[now]:
                if next == fa:
                    continue
                
                rest = check(next, now, v)
                if rest + val > v:
                    return rest + val
                else:
                    val += rest
            
            if val == v:
                return 0
            else:
                return val

        for parts in range(n, 1, -1):
            if s % parts == 0:
                target = s / parts
                if check(0, -1, target) == 0:
                    return parts - 1
        
        return 0
```
