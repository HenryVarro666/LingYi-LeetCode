---
title: "1878. 矩阵中最大的三个菱形和"
aliases: ["yiduobo的每日leetcode 1878.矩阵中最大的三个菱形和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/476085238"
zhihu_id: "476085238"
zhihu_title: "yiduobo的每日leetcode 1878.矩阵中最大的三个菱形和"
question_id: "1878"
question: "矩阵中最大的三个菱形和"
problem_url: "https://leetcode.cn/problems/get-biggest-three-rhombus-sums-in-a-grid/"
difficulty: "Medium"
rating: 1898
created: "2022-03-05T00:41:35+08:00"
updated: "2022-03-05T00:41:35+08:00"
upvotes: 0
comments: 0
---

# 1878. 矩阵中最大的三个菱形和

> **[yiduobo的每日leetcode 1878.矩阵中最大的三个菱形和](https://zhuanlan.zhihu.com/p/476085238) · 知乎 · 2022-03-05 · 赞同 0**
> 力扣：[1878. 矩阵中最大的三个菱形和](https://leetcode.cn/problems/get-biggest-three-rhombus-sums-in-a-grid/) · Medium · 灵茶山艾府：[斜向前缀和（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1878.矩阵中最大的三个菱形和

[阻断页面](https://leetcode-cn.com/problems/get-biggest-three-rhombus-sums-in-a-grid/)

题目中菱形和的定义是构成一个正菱形的四条斜边经过的各个格子上的数之和。

其中斜边分为左右两种，同一条左斜边经过的格子满足横纵坐标之后相等，而同一条右斜边经过的格子满足横纵坐标之差相等。题目要求的斜边上经过的格子上的数之和实际上可以认为是某种区间和，因此在这里可以利用前缀和来进行优化，即针对每一条左斜边和右斜边都计算出前缀和，然后对于菱形的边，通过起始格子横纵坐标先得到当前是哪一条斜边，然后再利用前缀和之差计算出区间和。

题目在这里需要计算每个菱形的和，感觉应该有某种可以通过较小菱形和来求解较大菱形和的方法，但是没有什么思路，只能老老实实枚举所有的菱形。我在这里采取的是枚举菱形中心点的做法，然后从中心点开始向上下左右四个方向扩张，得到菱形的四个顶点。若这些顶点没有出界，那么就利用上面的斜边前缀和求解菱形和。需要注意的是，菱形的四个顶点都被计算了两次，因此需要分别减去对应格子上的数值各一次。

枚举过程中，使用三个变量维护当前菱形和的前三名并根据枚举到的菱形进行更新即可。

最后附上python代码：

```python
class Solution(object):
    def getBiggestThree(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[int]
        """

        m = len(grid)
        n = len(grid[0])

        left_s = [[0] * max(m, n) for _ in range(m + n - 1)]
        right_s = [[0] * max(m, n) for _ in range(m + n - 1)]

        for i in range(m):
            for j in range(n):
                left_pos = i + j
                left_s[left_pos][i] = grid[i][j]
                if i > 0:
                    left_s[left_pos][i] += left_s[left_pos][i - 1]
                
                right_pos = i - j + n - 1
                right_s[right_pos][i] = grid[i][j]
                if i > 0:
                    right_s[right_pos][i] += right_s[right_pos][i - 1]
        
        first = second = third = 0
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                first, second, third = self.check(first, second, third, grid[i][j])
                l = 1
                while True:
                    angle_pos = []
                    now = 0
                    for index in range(4):
                        x = i + dx[index] * l
                        y = j + dy[index] * l
                        if x >= 0 and x < m and y >= 0 and y < n:
                            angle_pos.append([x, y])
                            now -= grid[x][y]
                        else:
                            break

                    if len(angle_pos) < 4:
                        break

                    now += self.get_s(left_s, angle_pos[0][0] + angle_pos[0][1], angle_pos[0][0], angle_pos[3][0])
                    now += self.get_s(left_s, angle_pos[1][0] + angle_pos[1][1], angle_pos[1][0], angle_pos[2][0])
                    now += self.get_s(right_s, angle_pos[0][0] - angle_pos[0][1] + n - 1, angle_pos[0][0], angle_pos[1][0])
                    now += self.get_s(right_s, angle_pos[3][0] - angle_pos[3][1] + n - 1, angle_pos[3][0], angle_pos[2][0])

                    first, second, third = self.check(first, second, third, now)
                    l += 1
        
        if third > 0:
            return [first, second, third]
        elif second > 0:
            return [first, second]
        else:
            return [first]

    def check(self, first, second, third, now):
        if now > first:
            first, second, third = now, first, second
        elif now > second and now != first:
            second, third = now, second
        elif now > third and now != first and now != second:
            third = now
        
        return first, second, third
    
    def get_s(self, s, s_pos, start, end):
        res = s[s_pos][end]
        if start > 0:
            res -= s[s_pos][start - 1]
        return res
```
