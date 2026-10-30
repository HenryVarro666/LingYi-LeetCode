---
title: "3206. 交替组I"
aliases: ["yiduobo的每日leetcode 3206.交替组I"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/dynamic-programming", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/707737191"
zhihu_id: "707737191"
zhihu_title: "yiduobo的每日leetcode 3206.交替组I"
question_id: "3206"
question: "交替组 I"
problem_url: "https://leetcode.cn/problems/alternating-groups-i/"
difficulty: "Easy"
created: "2024-07-08T21:07:50+08:00"
updated: "2024-07-08T21:07:50+08:00"
upvotes: 0
comments: 0
---

# 3206. 交替组I

> **[yiduobo的每日leetcode 3206.交替组I](https://zhuanlan.zhihu.com/p/707737191) · 知乎 · 2024-07-08 · 赞同 0**
> 力扣：[3206. 交替组 I](https://leetcode.cn/problems/alternating-groups-i/) · Easy · 灵茶山艾府：[O(n) 做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3206.交替组I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/alternating-groups-i/)

题目给出一个由01组成的数组colors，表示环形瓷砖的颜色。其中colors[i]等于0时表示第i块瓷砖的颜色为红色，等于1时则表示第i块瓷砖的颜色为蓝色。如果数组中连续三块瓷砖的颜色是交替颜色，也就是说中间瓷砖的颜色和两边的不同，那么这就是一个交替组。问一共有多少个交替组。

交替组需要检测的是当前位置所在瓷砖的颜色以及其两侧的颜色，那么只需遍历所有的瓷砖，检测以当前遍历到的瓷砖作为中心瓷砖时能否构成交替组。对于位置index的瓷砖，其左侧的位置为(index - 1 + n) % n，而其右侧的位置则为(index + 1) % n，若左侧位置瓷砖的颜色以及右侧位置瓷砖的颜色都不等于当前的颜色，就更新答案。

最后附上python代码：

```python
class Solution(object):
    def numberOfAlternatingGroups(self, colors):
        """
        :type colors: List[int]
        :rtype: int
        """

        res = 0
        n = len(colors)
        for index in range(n):
            pre = (index - 1 + n) % n
            nxt = (index + 1) % n
            if colors[pre] != colors[index] and colors[index] != colors[nxt]:
                res += 1
        
        return res
```
