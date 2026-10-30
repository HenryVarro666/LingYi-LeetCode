---
title: "1620. 网络信号最好的坐标"
aliases: ["yiduobo的每日leetcode 1620.网络信号最好的坐标"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435947330"
zhihu_id: "435947330"
zhihu_title: "yiduobo的每日leetcode 1620.网络信号最好的坐标"
question_id: "1620"
question: "网络信号最好的坐标"
problem_url: "https://leetcode.cn/problems/coordinate-with-maximum-network-quality/"
created: "2021-11-21T18:51:36+08:00"
updated: "2021-11-21T18:51:36+08:00"
upvotes: 1
comments: 0
---

# 1620. 网络信号最好的坐标

> **[yiduobo的每日leetcode 1620.网络信号最好的坐标](https://zhuanlan.zhihu.com/p/435947330) · 知乎 · 2021-11-21 · 赞同 1**
> 力扣：[1620. 网络信号最好的坐标](https://leetcode.cn/problems/coordinate-with-maximum-network-quality/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1620.网络信号最好的坐标

[力扣](https://leetcode-cn.com/problems/coordinate-with-maximum-network-quality/)

乍一看以为又是一道最优化问题，但是这里有向下取整的操作，同时要求坐标为正数，看样子是不能这么做。不过注意到题目数据的规模比较小，那么可以直接枚举坐标系里面的每一个整数坐标，然后计算该位置的网络信号，取其中最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def bestCoordinate(self, towers, radius):
        """
        :type towers: List[List[int]]
        :type radius: int
        :rtype: List[int]
        """

        res = [0, 0]
        max_c = 0
        for x in range(0, 101):
            for y in range(0, 101):
                tot = 0
                for tx, ty, q in towers:
                    tmp = (x - tx) ** 2 + (y - ty) ** 2
                    if tmp > radius ** 2:
                        continue
                    
                    tot += int(q / (1 + sqrt(tmp)))

                if tot > max_c:
                    max_c = tot
                    res = [x, y]
        
        return res
```
