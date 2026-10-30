---
title: "1564. 把箱子放进仓库里I"
aliases: ["yiduobo的每日leetcode 1564.把箱子放进仓库里I"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/618087637"
zhihu_id: "618087637"
zhihu_title: "yiduobo的每日leetcode 1564.把箱子放进仓库里I"
question_id: "1564"
question: "把箱子放进仓库里I"
problem_url: "https://leetcode.cn/problems/put-boxes-into-the-warehouse-i/"
created: "2023-03-30T00:59:21+08:00"
updated: "2023-03-30T00:59:21+08:00"
upvotes: 0
comments: 0
---

# 1564. 把箱子放进仓库里I

> **[yiduobo的每日leetcode 1564.把箱子放进仓库里I](https://zhuanlan.zhihu.com/p/618087637) · 知乎 · 2023-03-30 · 赞同 0**
> 力扣：[1564. 把箱子放进仓库里I](https://leetcode.cn/problems/put-boxes-into-the-warehouse-i/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1564.把箱子放进仓库里I

[力扣](https://leetcode.cn/problems/put-boxes-into-the-warehouse-i/)

题目规定了只能从左向右进入到仓库中，也就意味着仓库中的每一列可以放置的最大高度取决于该列以及其左侧所有列中的最小高度。换言之，仓库的可放置高度是从右向左单调递增的，可以先从左向右一趟遍历计算出仓库每一列可以放置的高度。

另一方面，题目只要求放置的箱子最多，因此在这里就应该尽量先放较矮的箱子。对于每个箱子，最优的放置位置应该是当前剩下列中可以放置该箱子的最右侧的那一列，于是可以将这些箱子按高度从小到大进行排序。由于仓库的可放置高度是已经有序的，因此只需遍历排序后的箱子，然后利用单调性找出每个箱子应该放置的列即可。

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
        h_list = [now]
        for w in warehouse[1:]:
            now = min(now, w)
            h_list.append(now)
            
        boxes.sort()
        p = 0
        res = 0
        for h in h_list[::-1]:
            if boxes[p] <= h:
                res += 1
                p += 1
                if p == len(boxes):
                    break
        
        return res
```
