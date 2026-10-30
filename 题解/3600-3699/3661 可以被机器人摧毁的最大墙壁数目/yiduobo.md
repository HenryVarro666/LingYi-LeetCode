---
title: "3661. 可以被机器人摧毁的最大墙壁数目"
aliases: ["yiduobo的每日leetcode 3661.可以被机器人摧毁的最大墙壁数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/two-pointers", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950282629669684391"
zhihu_id: "1950282629669684391"
zhihu_title: "yiduobo的每日leetcode 3661.可以被机器人摧毁的最大墙壁数目"
question_id: "3661"
question: "可以被机器人摧毁的最大墙壁数目"
problem_url: "https://leetcode.cn/problems/maximum-walls-destroyed-by-robots/"
difficulty: "Hard"
rating: 2525
created: "2025-09-16T00:55:00+08:00"
updated: "2025-09-16T00:55:02+08:00"
upvotes: 0
comments: 0
---

# 3661. 可以被机器人摧毁的最大墙壁数目

> **[yiduobo的每日leetcode 3661.可以被机器人摧毁的最大墙壁数目](https://zhuanlan.zhihu.com/p/1950282629669684391) · 知乎 · 2025-09-16 · 赞同 0**
> 力扣：[3661. 可以被机器人摧毁的最大墙壁数目](https://leetcode.cn/problems/maximum-walls-destroyed-by-robots/) · Hard · 灵茶山艾府：[教你一步步思考 DP：从记忆化搜索到递推到双指针优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3661.可以被机器人摧毁的最大墙壁数目

<https://leetcode.cn/problems/maximum-walls-destroyed-by-robots/description/>

一条无限长的直线上分布着一些机器人和墙壁。给出三个数组robots，distance以及walls，分别表示每个机器人的位置，每个机器人的子弹可以行进的最大距离，以及每一堵墙的位置。

每个机器人都只有一发子弹，可以向左侧或者右侧射击，子弹最远行进distance[index]米。子弹将摧毁其射程内路径上的所有墙壁，但是如果在到达墙壁前碰到了另一个机器人，子弹会在该机器人处停止无法继续前进，但是不会摧毁这个机器人。另外，如果墙壁和机器人在同一位置，那么这个机器人发出的子弹将摧毁这堵墙壁。

问最多可以摧毁多少堵墙壁。

每个机器人可以尝试向两个方向开枪，而且互相之间还有影响，比如挡住了另一个机器人发射的子弹，或者发射的子弹互相之间有覆盖，因此单纯的计算往哪一侧开枪，然后贪心选择打得最多的那一侧是不行的。

另一方面，正是由于机器人会挡住另一个机器人发射的子弹，也就是说如果按坐标的顺序决定机器人开枪的方向，那么当前的机器人只可能受前一个机器人的影响，也最多只会影响到下一个机器人。基于这一点，就可以使用动态规划进行求解。

将所有机器人按照下标位置从小到大排序，然后一趟遍历。令f[index]分别表示第0到第index个机器人开完枪，且最后这个机器人是向左开枪时可以摧毁的最多墙壁数目，而g[index]则表示最后这个机器人向右开枪时可以摧毁的最多墙壁。记r[index]和d[index]为第index个机器人所在的位置以及其子弹可以行进的距离，那么：

1、当index \= 0时：

此时向左开枪不会受其他机器人的影响，子弹向左最远可以到达r[index] - d[index]这个位置，所有位于这个区间内的墙壁都会被打掉。

为了计算被打掉的墙壁的数目，则可以将所有墙壁也按照位置从小到大进行排序，然后利用二分法进行求解。具体来说，对于覆盖范围为\[left, right\]的子弹区间，通过二分法找出所有墙壁中下标严格小于left的墙壁数目，以及所有墙壁中下标小于等于right的墙壁数目，二者相减即为区间中墙壁的数目。记cnt\[left, right\]为区间\[left, right\]之间墙壁的数目，那么在这里就有f\[0\] \= cnt\[r\[index\] - d\[index\], r\[index\]\]。

此时向右开枪则可能受到下一个机器人的影响，子弹向右理论上最远可以到达r[index] + d[index]，但是不能越过r[index + 1]，因此实际上最远只能到达min(r[index] + d[index], r[index + 1] - 1)，而g[0] \= cnt[r[index], min(r[index] + d[index], r[index + 1] - 1)]。

2、当index > 0时：

对于f[index]，其可能从f[index - 1]或者g[index - 1]转移过来。

若其从f\[index - 1\]转移过来，那么就说明上一个机器人也是向左开枪的，其子弹不会影响到当前机器人，也就是说当前机器人向左发射子弹最远可以到达max(r\[index - 1\] + 1, r\[index\] - d\[index\])，那么覆盖的墙壁数目就是cnt\[max(r\[index - 1\] + 1, r\[index\] - d\[index\]), r\[index\]\]，记为f_from_f。

若其从g\[index - 1\]转移过来，那么上一个机器人发射的子弹已经覆盖了r\[index - 1\]到r\[index\]之间的部分墙壁，当前机器人发射的子弹不应该再进入到这个区间中。更具体的，上一个机器人发射的子弹最远可以到达min(r\[index - 1\] + d\[index - 1\], r\[index\] - 1)，因此当前机器人向左发射子弹时，其最远可以到达的位置为max(min(r\[index - 1\] + d\[index - 1\], r\[index\] - 1) + 1, r\[index\] - d\[index\])，那么覆盖的墙壁数目就是cnt\[max(min(r\[index - 1\] + d\[index - 1\], r\[index - 1\]) + 1, r\[index\] - d\[index\]), r\[index\]\]，记为f_from_g。

综合以上两种情况，就有f[index] \= max(f[index - 1] + f_from_f, g[index - 1] + f_from_g)

而对于g[index]，其同样可能从f[index - 1]或者g[index - 1]转移过来。

无论其从哪个状态转移过来，其发射的子弹都不会受到上一个机器人的影响，而其发射的子弹最远可以到达min(r[index] + d[index], r[index + 1] - 1)，因此就有

g[index] \= max(f[index - 1], g[index - 1]) + cnt[r[index], min(r[index] + d[index], r[index + 1] - 1)]

这样一来，只需一趟遍历，计算出所有的f和g，然后取f[-1]和g[-1]中较大的那个作为最终答案即可。

注意到f和g每一列之和上一轮有关，因此在这里可以通过变量迭代省去f和g数组。

最后附上python代码：

```python
class Solution(object):
    def maxWalls(self, robots, distance, walls):
        """
        :type robots: List[int]
        :type distance: List[int]
        :type walls: List[int]
        :rtype: int
        """
        
        robot_info = sorted((r, d) for r, d in zip(robots, distance))
        walls.sort()
        robot_info.append((walls[-1] + 1, 0))

        def calc(start, end):
            if start > end:
                return 0
            
            if start > walls[-1] or end < walls[0]:
                return 0
            
            left = 0
            right = len(walls) - 1
            while left < right:
                mid = (left + right) // 2
                if walls[mid] >= start:
                    right = mid
                else:
                    left = mid + 1
            
            start_index = left

            left = 0
            right = len(walls) - 1
            while left < right:
                mid = (left + right + 1) // 2
                if walls[mid] <= end:
                    left = mid
                else:
                    right = mid - 1
            
            end_index = left

            return end_index - start_index + 1

        f, g = None, None
        for index in range(len(robot_info) - 1):
            r, d = robot_info[index]
            if index == 0:
                f = calc(max(0, r - d), r)
                g = calc(r, min(robot_info[index + 1][0] - 1, r + d))
            else:
                pre_f, pre_g = f, g
                f_from_f = calc(max(robot_info[index - 1][0] + 1, r - d), r)
                f_from_g = calc(max(robot_info[index - 1][0] + robot_info[index - 1][1] + 1, r - d), r)
                f = max(pre_f + f_from_f, pre_g + f_from_g)
                g = max(pre_f, pre_g) + calc(r, min(robot_info[index + 1][0] - 1, r + d))
        
        return max(f, g)
```
