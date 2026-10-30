---
title: "2923. 找到冠军I & 2924. 找到冠军II"
aliases: ["yiduobo的每日leetcode 2923.找到冠军I && 2924.找到冠军II", "2923. 找到冠军I", "2924. 找到冠军II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li", "leetcode/medium", "leetcode/graph"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/690067450"
zhihu_id: "690067450"
zhihu_title: "yiduobo的每日leetcode 2923.找到冠军I && 2924.找到冠军II"
question_id: ["2923", "2924"]
question: ["找到冠军 I", "找到冠军 II"]
problem_url: ["https://leetcode.cn/problems/find-champion-i/", "https://leetcode.cn/problems/find-champion-ii/"]
difficulty: ["Easy", "Medium"]
created: "2024-03-31T23:57:25+08:00"
updated: "2024-03-31T23:57:25+08:00"
upvotes: 3
comments: 0
---

# 2923. 找到冠军I & 2924. 找到冠军II

> **[yiduobo的每日leetcode 2923.找到冠军I && 2924.找到冠军II](https://zhuanlan.zhihu.com/p/690067450) · 知乎 · 2024-03-31 · 赞同 3**
> 力扣：[2923. 找到冠军 I](https://leetcode.cn/problems/find-champion-i/) · Easy · 灵茶山艾府：[从 O(n^2) 到 O(n)（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[2924. 找到冠军 II](https://leetcode.cn/problems/find-champion-ii/) · Medium · 灵茶山艾府：[[灵茶山艾府题解/solutions/2924 找到冠军 II · 不在 edges-i-1- 中的唯一编号（Python-Java-C++-C-Go-JS-Rust）|不在 edges[i][1] 中的唯一编号（Python/Java/C++/C/Go/JS/Rust）]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2923.找到冠军I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-champion-i/description/)

题目保证了所有不同队伍之间都进行过比赛，同时胜负关系存在传递性，因此一定存在一个冠军。同样也是因为这个传递性，只需一趟遍历，不断对比当前队伍以及候选冠军的胜负关系就能找到冠军队伍。具体来说，若候选冠军获胜，那么则继续向后比较；反之若当前队伍获胜，那么根据传递性，当前队伍一定也胜过了之前的所有队伍，因此只需将候选冠军更新为当前队伍，然后继续向后比较就行了。

最后附上python代码：

```python
class Solution(object):
    def findChampion(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        res = 0
        for index in range(1, len(grid)):
            if grid[index][res] == 1:
                res = index
        
        return res
```

2924.找到冠军II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-champion-ii/description/)

上一题的加强版。本题中队伍的胜负关系同样存在传递性，但是不保证每两支队伍间都进行过比赛。

在这里可以统计图中每个节点的入度，这个入度的含义是当前队伍被几只队伍击败过。若只有一支队伍没被击败过，那么由于传递性的存在，这支队伍一定是冠军。若存在多支队伍没有被击败过，说明这些队伍之间没有进行过比赛，也没法通过传递性确定这些队伍的胜负关系，也就是说不存在冠军。

最后附上python代码：

```python
class Solution(object):
    def findChampion(self, n, edges):
        """
        :type n: int
        :type edges: List[List[int]]
        :rtype: int
        """

        ind = [0] * n
        for x, y in edges:
            ind[y] += 1
        
        res = None
        for index in range(n):
            if ind[index] == 0:
                if res is None:
                    res = index
                else:
                    res = -1
                    break
        
        return res
```
