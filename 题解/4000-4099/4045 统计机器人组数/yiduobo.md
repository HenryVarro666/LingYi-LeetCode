---
title: "4045. 统计机器人组数"
aliases: ["yiduobo的每日leetcode 4045.统计机器人组数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/常用数据结构/三-栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2080412055299953057"
zhihu_id: "2080412055299953057"
zhihu_title: "yiduobo的每日leetcode 4045.统计机器人组数"
question_id: "4045"
question: "统计机器人组数"
problem_url: "https://leetcode.cn/problems/count-robot-groups/"
difficulty: "Medium"
rating: 1888
created: "2026-09-07T22:04:57+08:00"
updated: "2026-09-07T22:05:01+08:00"
upvotes: 0
comments: 0
---

# 4045. 统计机器人组数

> **[yiduobo的每日leetcode 4045.统计机器人组数](https://zhuanlan.zhihu.com/p/2080412055299953057) · 知乎 · 2026-09-07 · 赞同 0**
> 力扣：[4045. 统计机器人组数](https://leetcode.cn/problems/count-robot-groups/) · Medium · 灵茶山艾府：[两种方法：正序遍历+栈 / 倒序遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4045.统计机器人组数

<https://leetcode.cn/problems/count-robot-groups/description/>

题目给出一个严格递增的整数数组position，其中position[index]是第index个机器人(下标从0开始)在时间t \= 0时的初始位置。

另外给出一个整数数组speed以及一个整数distance，其中speed[index]是第index个机器人的恒定速度，单位为单位每秒。

时间是连续的，以秒为单位。速度为v的机器人或机器人组在任意t秒的时间间隔内向右移动v \* t个单位。

每当两个机器人或组之间的距离至多为distance时，它们就会合并成一个机器人组。

若多个机器人或机器人组在同一时间满足合并条件，那么所有合并将同时发生。具体来说，就是任意向量位置相差不超过distance的相连机器人或组都会合并为一个机器人组。

合并完成后，生成的机器人组将继承该组中最右侧机器人的当前位置与速度。一旦合并，机器人将永不分离。

问所有合并发生后剩余的组数。

直观来看，对于两个相邻的机器人或组，若左侧的速度和右侧的速度相同，或者比右侧的慢，那么二者的距离只会越来越远，导致合并无法发生。但是这个结论是不完全，因为右侧的机器人或组可能与更右侧的发生合并，导致速度变慢，是的左侧的机器人或组有机会追上来。

换言之，只有当确定了右侧机器人的速度已经固定下来后，才能判断是否会发生合并。基于这一点，从后往前遍历就是很自然的想法了。

首先最右侧的机器人的速度一定是不会改变的，而对于靠前的机器人，则可以分为两种情况。

第一种是与右侧的机器人发生合并。对于这种情况，实际上就相当于当前这个机器人被移除掉了，因为合并后保留下来的是右侧的那一个。

第二种则是无法与右侧的机器人发生合并。对于这种情况，无论当前机器人左侧的机器人如何进行合并，最终都不会影响当前机器人的速度，也就是说当前机器人是不可能与右侧发生合并的。此时就可以将右侧机器人累加到答案中，然后以当前机器人的速度为标准继续向左考虑。

另外需要注意在一开始就可能有些机器人可以合并，因此在倒序遍历之前需要先遍历一次，执行初始状态下的合并。

最后附上python代码：

```python
class Solution(object):
    def countGroups(self, position, speed, distance):
        """
        :type position: List[int]
        :type speed: List[int]
        :type distance: int
        :rtype: int
        """
        
        r = [(position[0], speed[0])]
        for p, s in zip(position[1:], speed[1:]):
            if p - r[-1][0] <= distance:
                r[-1] = (p, s)
            else:
                r.append((p, s))
        
        res = 1
        s = r[-1][1]
        for index in range(len(r) - 2, -1, -1):
            if r[index][1] <= s:
                res += 1
                s = r[index][1]
        
        return res
```
