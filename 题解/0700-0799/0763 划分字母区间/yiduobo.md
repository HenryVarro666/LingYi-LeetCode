---
title: "763. 划分字母区间"
aliases: ["yiduobo的每日leetcode 763.划分字母区间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/LeetCode-热题-100", "题单/贪心算法/二-区间贪心", "题单/LeetCode-热题-100/贪心算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/338855833"
zhihu_id: "338855833"
zhihu_title: "yiduobo的每日leetcode 763.划分字母区间"
question_id: "763"
question: "划分字母区间"
problem_url: "https://leetcode.cn/problems/partition-labels/"
difficulty: "Medium"
rating: 1443
created: "2020-12-23T00:34:01+08:00"
updated: "2020-12-23T00:34:01+08:00"
upvotes: 0
comments: 0
---

# 763. 划分字母区间

> **[yiduobo的每日leetcode 763.划分字母区间](https://zhuanlan.zhihu.com/p/338855833) · 知乎 · 2020-12-23 · 赞同 0**
> 力扣：[763. 划分字母区间](https://leetcode.cn/problems/partition-labels/) · Medium · 灵茶山艾府：[本质是合并区间，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

763.划分字母区间

[力扣](https://leetcode-cn.com/problems/partition-labels/)

题目要求同一个字母只能出现在同一个区间内，如果我们从头到尾进行划分的话，只需要关注每个字母最后一次出现的位置last_pos。那么可以首先从头到尾进行一趟扫描，预处理出每个字母最后出现的位置。

预处理完成后，维护两个变量l和r表示当前区间的左右边界开始进行划分，其初始值都为0。

对于S\[l\]，我们必须将l到last_pos\[S\[l\]\]之间的所有字符都划分进来，于是更新r为last_pos\[S\[l\]\]，然后逐个l + 1到r之间所有字符最后一次出现的位置。若其中某个字符最后出现的位置大于r，那么就要将r往右移动至该位置。当确定l到r之间所有字符都满足条件之后，区间\[l, r\]就是一个合法的划分，接下来则需要从l \= r + 1开始对后续的字符串继续进行划分直到S的末尾。

最后附上python代码：

```python
class Solution(object):
    def partitionLabels(self, S):
        """
        :type S: str
        :rtype: List[int]
        """

        last_pos = {}
        for index, char in enumerate(S):
            last_pos[char] = index

        l = 0
        res = []
        while l < len(S):
            r = last_pos[S[l]]
            pos = l + 1
            while pos < r:
                if last_pos[S[pos]] > r:
                    r = last_pos[S[pos]]
                pos += 1
            res.append(r - l + 1)
            l = r + 1
        
        return res
```
