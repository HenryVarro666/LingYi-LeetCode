---
title: "741. 摘樱桃"
aliases: ["yiduobo的每日leetcode 741.摘樱桃"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/二-网格图-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336947732"
zhihu_id: "336947732"
zhihu_title: "yiduobo的每日leetcode 741.摘樱桃"
question_id: "741"
question: "摘樱桃"
problem_url: "https://leetcode.cn/problems/cherry-pickup/"
difficulty: "Hard"
created: "2020-12-14T23:57:47+08:00"
updated: "2020-12-14T23:57:47+08:00"
upvotes: 0
comments: 0
---

# 741. 摘樱桃

> **[yiduobo的每日leetcode 741.摘樱桃](https://zhuanlan.zhihu.com/p/336947732) · 知乎 · 2020-12-14 · 赞同 0**
> 力扣：[741. 摘樱桃](https://leetcode.cn/problems/cherry-pickup/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到空间优化！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

741.摘樱桃

[力扣](https://leetcode-cn.com/problems/cherry-pickup/)

很有意思的动态规划问题。题目是经典的往右下角走找一条最大的路径，但是这里要求走回来，且之前经过的节点权重置0。

首先可以明确的一点是，不能先从左上角通过动态规划走到右下角，然后修改权重后再用动态规划走回去，因为这里二阶段的地图被一阶段修改过了，整个过程实际上变成了贪心算法，无法得到最优解。

对于答案中的两端路径，有一个性质就是这两条路径可能重合，但是不会出现交叉的情况，因为所有交叉的情况都存在完全等价的不交叉情况，

例如3\*3的地图，向下的路径为

(0, 0) -> (1, 0) -> (1, 1) -> (1, 2) -> (2, 2)

向上的路径为

(2, 2) -> (2, 1) -> (1, 1) -> (0, 1) -> (0, 0)

这是两条交叉的路径，但是如果我们将左侧的部分归给向下的路径，将右侧的部分归给向上的路径，那么两条路径就变成了

(0, 0) -> (1, 0) -> (1, 1) -> (2, 1) -> (2, 2)

(2, 2) -> (1, 2) -> (1, 1) -> (0, 1) -> (0, 0)

这样两条路径就只于点(1, 1)重合，但是不存空间结构上的交叉。

换言之，最终的答案必然可以写成一左一右两条路径的形式。又注意到向上的路径虽然描述是要求从终点往上返回起点，但是实际上从起点出发往下走到终点是完全等价的。

综合上面这两个结论，就可以题目进行转化，将一来一回两条路径改为一左一右两条路径，同时从起点出发向下往终点走。当没有相遇时，则计算各自位置上的权重；当相遇时，则只计算相遇各自的权重一次。

如果我们将地图旋转45度，就得到一个正三角以及一个倒三角，例如样例，就可以看做

0

1 1

1 0 -1

1 -1

1

然后我们就是从最上层开始，一左一右两条路径往下，最终走到最下层。注意到两条路径走到每一层需要的步数是完全一致的，于是可以使用f[i][j][k]表示走了i步，左边的路径在当前层的第j个位置，右边的路径在当前层的第k个位置时的最大值。对于样例而言：

左侧的路径为0 -> 0 -> 0 -> 0 -> 0

右侧的路径为0 -> 1 -> 1 -> 0 -> 0

那么在f数组上的转移就是f[0][0][0] -> f[1][0][1] -> f[2][0][1] -> f[3][0][0] -> f[4][0][0]

到了这里，可以进一步拆解，将问题看做两个数字三角形的动态规划问题，不过这里是一正一倒。对于正三角的f[i][j][k]：

1、若grid[i - j][j]或grid[i - k][k]为-1，说明有一条路径没法往前走，于是有f[i][j][k] \= -1。

2、接下来判断j是否等于k，若相等，说明两条路径走到了同一个位置上，那么此时的权重只能计算一次，于是加权add为grid[i - j][j]，否则加权add为grid[i - j][j] + grid[i - k][k]。

3、再往后则需要找到所有能够到达状态f[i][j][k]的前置状态中最大的一个，记为tmp，此时需要根据j和k的值分几种情况讨论：

3-1、若j \= 0，且k \= 0，此时两条路径都位于最左侧。由于当前的题目是正三角形，因此这个位置只能从上一层最左侧的位置下来，于是有tmp \= f[i - 1][j][k]

3-2、若j \= 0，且k \= i，此时左侧的路径只能从上一层最左侧的位置下来，而右侧的路径只能从上一层最右侧的位置下俩，于是有tmp \= f[i - 1][j][k - 1]

3-3、若j \= 0，且k不等于0或i，此时左侧的路径只能从上一层最左侧的位置下来，右侧的路径则可以从第k - 1个位置或第k个位置下来，于是有tmp \= max(f[i - 1][j][k - 1], f[i - 1][j][k])

3-4、若j \= i，说明此时左侧路径在这一层的最右边，那么右侧路径也只能在同样的位置，该位置只能从上一层的最右边下来，于是有tmp \= f[i - 1][j - 1][k - 1]

3-5、若j不等于0或者i，且k等于i，此时情况与3-3正好相反，这次是左侧的路径可以从上一层的第j - 1个位置或者第j个位置下来，但是右侧的路径只能从上一层的最右边下来，于是就有tmp \= max(f[i - 1][j - 1][k - 1], f[i - 1][j][k - 1])

3-6、其他情况下，左侧和右侧的位置都可能从上一层的两个位置下来，于是有

tmp \= max(f[i - 1][j - 1][k - 1], f[i - 1][j - 1][k], f[i - 1][j][k - 1], f[i - 1][j][k])

计算完毕后，若tmp为-1，说明没有任何一条路径可以到达f[i][j][k]，于是有f[i][j][k] \= -1，否则就有f[i][j][k] \= tmp + add

完成正三角的计算之后，我们还需要计算倒三角的路径。倒三角的路径相对简洁一些，因为后一层的每个位置都可能从前一层的两个位置走到，不需要正三角步骤3里面的那些判断。不过需要注意的是，同一个位置的权重依然还是只能计算一次，于是对于f[i][j][k]：

1、若grid[i - j][j]或grid[i - k][k]为-1，说明有一条路径没法往前走，于是有f[i][j][k] \= -1。

2、接下来判断j是否等于k，若相等，说明两条路径走到了同一个位置上，那么此时的权重只能计算一次，于是加权add为grid[i - j][j]，否则加权add为grid[i - j][j] + grid[i - k][k]。

3、再往后则需要找到所有能够到达状态f[i][j][k]的前置状态中最大的一个，记为tmp，此时的tmp则比较直接，为

tmp \= max(f[i - 1][j - 1][k - 1], f[i - 1][j - 1][k], f[i - 1][j][k - 1], f[i - 1][j][k])

最后依然是判断tmp是否为-1，若是，则f[i][j][k] \= -1，否则f[i][j][k] \= tmp + add

全部完成后，最后的f[-1][-1][-1]与0取max就是最终答案。

注意到过程中每一步的值都只与上一层的值相关，因此可以使用滚动数组来优化空间，不过直接省去一维比较麻烦，因此我才用的是01滚动的方式。

最后附上python代码：

```python
class Solution(object):
    def cherryPickup(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """

        N = len(grid)
        f = [[[-1] * N for _ in range(N)] for _ in range(2)]
        f[0][0][0] = grid[0][0]
        flag = 0

        for i in range(1, N):
            flag ^= 1
            for j in range(i + 1):
                for k in range(j, i + 1):
                    f[flag][j][k] = -1
                    if grid[i - j][j] == -1 or grid[i - k][k] == -1:
                        continue

                    if j == k:
                        add = grid[i - j][j]
                    else:
                        add = grid[i - j][j] + grid[i - k][k]

                    if j == 0:
                        if k == 0:
                            tmp = f[1 - flag][j][k]
                        elif k == i:
                            tmp = f[1 - flag][j][k - 1]
                        else:
                            tmp = max(f[1 - flag][j][k], f[1 - flag][j][k - 1])
                    elif j == i:
                        tmp = f[1 - flag][j - 1][k - 1]
                    elif k == i:
                        tmp = max(f[1 - flag][j][k - 1], f[1 - flag][j - 1][k - 1])
                    else:
                        tmp = max(f[1 - flag][j][k], f[1 - flag][j - 1][k - 1], f[1 - flag][j][k - 1], f[1 - flag][j - 1][k])
                    
                    if tmp != -1:
                        f[flag][j][k] = tmp + add
        
        for i in range(N, N + N - 1):
            flag ^= 1
            for j in range(i - N + 1, N):
                for k in range(j, N):
                    f[flag][j][k] = -1
                    if grid[i - j][j] == -1 or grid[i - k][k] == -1:
                        continue
                    
                    if j == k:
                        add = grid[i - j][j]
                    else:
                        add = grid[i - j][j] + grid[i - k][k]
                    
                    tmp = max(f[1 - flag][j][k], f[1 - flag][j - 1][k - 1], f[1 - flag][j][k - 1], f[1 - flag][j - 1][k])
                    
                    if tmp != -1:
                        f[flag][j][k] = tmp + add

        return max(f[flag][-1][-1], 0)
```
