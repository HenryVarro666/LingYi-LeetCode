---
title: "2021. 街上最亮的位置"
aliases: ["yiduobo的每日leetcode 2021.街上最亮的位置"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/625232880"
zhihu_id: "625232880"
zhihu_title: "yiduobo的每日leetcode 2021.街上最亮的位置"
question_id: "2021"
question: "街上最亮的位置"
problem_url: "https://leetcode.cn/problems/brightest-position-on-street/"
difficulty: "Medium"
created: "2023-04-27T02:00:48+08:00"
updated: "2023-04-27T02:00:48+08:00"
upvotes: 0
comments: 0
---

# 2021. 街上最亮的位置

> **[yiduobo的每日leetcode 2021.街上最亮的位置](https://zhuanlan.zhihu.com/p/625232880) · 知乎 · 2023-04-27 · 赞同 0**
> 力扣：[2021. 街上最亮的位置](https://leetcode.cn/problems/brightest-position-on-street/) · Medium · 灵茶山艾府：[Go 差分数组+排序+位运算压缩状态](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

2021.街上最亮的位置

[力扣](https://leetcode.cn/problems/brightest-position-on-street/)

如果将街道视为一个数组，那么每盏灯就都可以视为将数组中某个区间的亮度加上1，问最终数组上的最大值是多少，于是又得到了一个差分数组的问题。只需将每个区间的两个端点从小到大排序，然后一趟遍历，统计每个位置最多出现在几个区间内，取其中的最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def brightestPosition(self, lights):
        """
        :type lights: List[List[int]]
        :rtype: int
        """

        points = []
        for pos, range in lights:
            left = pos - range
            right = pos + range
            points.append(left * 2)
            points.append(right * 2 + 1)
        
        cnt = 0
        res = 0
        ma = 0
        for p in sorted(points):
            if p % 2 == 0:
                cnt += 1
                if cnt > ma:
                    ma = cnt
                    res = p / 2
            else:
                cnt -= 1
        
        return res
```
