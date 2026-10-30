---
title: "475. 供暖器"
aliases: ["yiduobo的每日leetcode 475.供暖器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/238212374"
zhihu_id: "238212374"
zhihu_title: "yiduobo的每日leetcode 475.供暖器"
question_id: "475"
question: "供暖器"
problem_url: "https://leetcode.cn/problems/heaters/"
created: "2020-09-12T23:20:36+08:00"
updated: "2020-09-12T23:20:36+08:00"
upvotes: 0
comments: 0
---

# 475. 供暖器

> **[yiduobo的每日leetcode 475.供暖器](https://zhuanlan.zhihu.com/p/238212374) · 知乎 · 2020-09-12 · 赞同 0**
> 力扣：[475. 供暖器](https://leetcode.cn/problems/heaters/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

475.供暖器<https://leetcode-cn.com/problems/heaters/>

比较基础的题目。对于每个房子，我们只需要找到与该房子距离最近的供暖器并计算二者之间的距离，那么这些距离的最大值即为最后答案。

具体实现上，我才用的是先对供暖器进行排序。若房子的位置在第一个供暖器之前，那么就由第一个供暖器为其供暖；若房子的位置在最后一个供暖器之后，那么就由最后一个供暖器为其供暖；否则房子必然位于两个供暖器之间，那么可以通过二分查找找到这两个供暖器，然后由较近的那个供暖器为房子供暖。

最后附上python代码：

```python
class Solution(object):
    def findRadius(self, houses, heaters):
        """
        :type houses: List[int]
        :type heaters: List[int]
        :rtype: int
        """

        heaters = sorted(heaters)
        res = 0
        for house in houses:
            if house >= heaters[-1]:
                res = max(res, house - heaters[-1])
            else:
                l = 0
                r = len(heaters) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if heaters[mid] >= house:
                        r = mid
                    else:
                        l = mid + 1

                if l == 0:
                    res = max(res, heaters[0] - house)
                else:
                    res = max(res, min(heaters[l] - house, house - heaters[l - 1]))
        
        return res
```
