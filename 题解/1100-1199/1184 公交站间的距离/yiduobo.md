---
title: "1184. 公交站间的距离"
aliases: ["yiduobo的每日leetcode 1184.公交站间的距离"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380209350"
zhihu_id: "380209350"
zhihu_title: "yiduobo的每日leetcode 1184.公交站间的距离"
question_id: "1184"
question: "公交站间的距离"
problem_url: "https://leetcode.cn/problems/distance-between-bus-stops/"
difficulty: "Easy"
created: "2021-06-12T18:23:34+08:00"
updated: "2021-06-12T18:23:34+08:00"
upvotes: 0
comments: 0
---

# 1184. 公交站间的距离

> **[yiduobo的每日leetcode 1184.公交站间的距离](https://zhuanlan.zhihu.com/p/380209350) · 知乎 · 2021-06-12 · 赞同 0**
> 力扣：[1184. 公交站间的距离](https://leetcode.cn/problems/distance-between-bus-stops/) · Easy · 灵茶山艾府：[遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1184.公交站间的距离

[力扣](https://leetcode-cn.com/problems/distance-between-bus-stops/)

静态区间和的问题，依然是利用前缀数组来解决。

题目中存在顺时针和逆时针两种情况，不妨设start小于destination，那么顺时针的情况就对应了pre[destination] - pre[start]，而逆时针的情况则是走过了剩余的所有边，因此是pre[-1] - (pre[destination - pre[start])，取二者的较小值即可。

最后附上python代码：

```python
class Solution(object):
    def distanceBetweenBusStops(self, distance, start, destination):
        """
        :type distance: List[int]
        :type start: int
        :type destination: int
        :rtype: int
        """

        s = [0]
        for index in range(len(distance) - 1):
            s.append(s[-1] + distance[index])
        s.append(s[-1] + distance[-1])

        if start > destination:
            start, destination = destination, start

        res = s[destination] - s[start]
        return min(res, s[-1] - res)
```
