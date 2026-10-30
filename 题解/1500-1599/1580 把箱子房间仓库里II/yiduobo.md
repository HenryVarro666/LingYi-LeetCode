---
title: "1580. 把箱子房间仓库里II"
aliases: ["yiduobo的每日leetcode 1580.把箱子房间仓库里II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618371158"
zhihu_id: "618371158"
zhihu_title: "yiduobo的每日leetcode 1580.把箱子房间仓库里II"
question_id: "1580"
question: "把箱子房间仓库里II"
problem_url: "https://leetcode.cn/problems/put-boxes-into-the-warehouse-ii/"
created: "2023-03-31T02:01:31+08:00"
updated: "2023-03-31T02:01:31+08:00"
upvotes: 0
comments: 0
---

# 1580. 把箱子房间仓库里II

> **[yiduobo的每日leetcode 1580.把箱子房间仓库里II](https://zhuanlan.zhihu.com/p/618371158) · 知乎 · 2023-03-31 · 赞同 0**
> 力扣：[1580. 把箱子房间仓库里II](https://leetcode.cn/problems/put-boxes-into-the-warehouse-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1580.把箱子放进仓库里II

[力扣](https://leetcode.cn/problems/put-boxes-into-the-warehouse-ii/)

之前1564题的强化版，不同的是本题可以从两侧将箱子放进仓库，不过处理方法还是类似。

[yiduobo：yiduobo的每日leetcode 1564.把箱子放进仓库里I](https://zhuanlan.zhihu.com/p/618087637)

对于本题，如果箱子从左侧进去，那么每一列可以放置的最高的箱子就可以按照之前相同的方式进行计算，那么将这种计算方式推广到从右侧进去，就可以通过正反两趟遍历得到每一列可能放置的最高的箱子是多高。

接下来只需对每一列取左右方向放置最高高度中较大的那一个，就得到了每一列可放置的高度。此时就可以照搬之前这一题的做法，对可放置高度和箱子高度分别从小到大进行排序，然后利用单调性一趟遍历计算出最终答案。

最后附上python代码：

```python
class Solution(object):
    def maxBoxesInWarehouse(self, boxes, warehouse):
        """
        :type boxes: List[int]
        :type warehouse: List[int]
        :rtype: int
        """

        now = warehouse[0]
        left = [now]
        for w in warehouse[1:]:
            now = min(now, w)
            left.append(now)
        
        n = len(warehouse)
        now = warehouse[n - 1]
        right = [now]
        for index in range(n - 2, -1, -1):
            w = warehouse[index]
            now = min(now, w)
            right.append(now)
        
        right.reverse()

        h_list = sorted([max(left[index], right[index]) for index in range(n)])
        p = 0
        boxes.sort()

        res = 0
        for h in h_list:
            if boxes[p] <= h:
                res += 1
                p += 1
                if p == len(boxes):
                    break
        
        return res
```
