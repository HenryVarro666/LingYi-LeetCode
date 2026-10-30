---
title: "1732. 找到最高海拔"
aliases: ["yiduobo的每日leetcode 1732.找到最高海拔"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/prefix-sum"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452473148"
zhihu_id: "452473148"
zhihu_title: "yiduobo的每日leetcode 1732.找到最高海拔"
question_id: "1732"
question: "找到最高海拔"
problem_url: "https://leetcode.cn/problems/find-the-highest-altitude/"
difficulty: "Easy"
created: "2022-01-01T23:21:02+08:00"
updated: "2022-01-01T23:21:03+08:00"
upvotes: 0
comments: 0
---

# 1732. 找到最高海拔

> **[yiduobo的每日leetcode 1732.找到最高海拔](https://zhuanlan.zhihu.com/p/452473148) · 知乎 · 2022-01-01 · 赞同 0**
> 力扣：[1732. 找到最高海拔](https://leetcode.cn/problems/find-the-highest-altitude/) · Easy · 灵茶山艾府：[最大前缀和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1732.找到最高海拔

[力扣](https://leetcode-cn.com/problems/find-the-highest-altitude/)

由于每个位置的海拔都可以通过上一个位置的海拔以及海拔差值计算得到，那么可以从头开始一趟扫描，计算出每个位置的海拔并用这个海拔更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def largestAltitude(self, gain):
        """
        :type gain: List[int]
        :rtype: int
        """

        res = 0
        now = 0
        for g in gain:
            now += g
            res = max(res, now)
        
        return res
```
