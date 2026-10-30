---
title: "1710. 卡车上的最大单元数"
aliases: ["yiduobo的每日leetcode 1710.卡车上的最大单元数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/449613823"
zhihu_id: "449613823"
zhihu_title: "yiduobo的每日leetcode 1710.卡车上的最大单元数"
question_id: "1710"
question: "卡车上的最大单元数"
problem_url: "https://leetcode.cn/problems/maximum-units-on-a-truck/"
created: "2021-12-25T00:01:38+08:00"
updated: "2021-12-25T00:01:38+08:00"
upvotes: 0
comments: 0
---

# 1710. 卡车上的最大单元数

> **[yiduobo的每日leetcode 1710.卡车上的最大单元数](https://zhuanlan.zhihu.com/p/449613823) · 知乎 · 2021-12-25 · 赞同 0**
> 力扣：[1710. 卡车上的最大单元数](https://leetcode.cn/problems/maximum-units-on-a-truck/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1710.卡车上的最大单元数

[力扣](https://leetcode-cn.com/problems/maximum-units-on-a-truck/)

由于选择每种箱子的代价都一样，那么显然应该优先选择units多的箱子。于是可以将箱子按照units从大到小进行排序，一趟扫描。对于当前的number[index]和units[index]：

1、若卡车剩余的位置truckSize >\= number[index]，那么就将这种箱子全部弄上车，此时可以新装number[index] \* units[index]的单元数，使用这个值更新答案，并将truckSize减去number[index]

2、若卡车剩余的位置truckSize \< number[index]，说明只能取一部分这种箱子，这个量自然就是truckSize，于是应该使用truckSize \* units[index]来更新答案。由于此时卡车已经没有空余的空间了，那么可以直接退出循环并返回结果

最后附上python代码：

```python
class Solution(object):
    def maximumUnits(self, boxTypes, truckSize):
        """
        :type boxTypes: List[List[int]]
        :type truckSize: int
        :rtype: int
        """

        res = 0
        for number, unit in sorted(boxTypes, key=lambda d:d[1], reverse=True):
            if truckSize >= number:
                res += number * unit
                truckSize -= number
            else:
                res += truckSize * unit
                break
        
        return res
```
