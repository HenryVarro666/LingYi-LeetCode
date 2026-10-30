---
title: "2211. 统计道路上的碰撞次数"
aliases: ["yiduobo的每日leetcode 2211.统计道路上的碰撞次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/540433839"
zhihu_id: "540433839"
zhihu_title: "yiduobo的每日leetcode 2211.统计道路上的碰撞次数"
question_id: "2211"
question: "统计道路上的碰撞次数"
problem_url: "https://leetcode.cn/problems/count-collisions-on-a-road/"
difficulty: "Medium"
rating: 1581
created: "2022-07-11T23:52:43+08:00"
updated: "2022-07-11T23:52:43+08:00"
upvotes: 0
comments: 0
---

# 2211. 统计道路上的碰撞次数

> **[yiduobo的每日leetcode 2211.统计道路上的碰撞次数](https://zhuanlan.zhihu.com/p/540433839) · 知乎 · 2022-07-11 · 赞同 0**
> 力扣：[2211. 统计道路上的碰撞次数](https://leetcode.cn/problems/count-collisions-on-a-road/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2211.统计道路上的碰撞次数

[力扣](https://leetcode.cn/problems/count-collisions-on-a-road/)

由于有静止的车辆这一说，因此只有两侧向外开的车不会发生碰撞，其他车辆要么一开始是静止状态，要么就会撞上别的车。

题目碰撞次数的计算是对于还在动的车撞了就计算一次，因此在去除掉两侧向外开的车辆后，再去掉静止的车辆后，剩余所有的车辆都将贡献一次碰撞，也就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def countCollisions(self, directions):
        """
        :type directions: str
        :rtype: int
        """

        n = len(directions)
        l = 0
        while l < n and directions[l] == 'L':
            l += 1
        
        if l == n:
            return 0
        
        r = n - 1
        while r >= 0 and directions[r] == 'R':
            r -= 1
        
        if r == -1:
            return 0
        
        res = r - l + 1
        for d in directions[l : r + 1]:
            if d == 'S':
                res -= 1
        
        return res
```
