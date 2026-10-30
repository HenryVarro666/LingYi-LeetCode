---
title: "1603. 设计停车系统"
aliases: ["yiduobo的每日leetcode 1603.设计停车系统"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/432312472"
zhihu_id: "432312472"
zhihu_title: "yiduobo的每日leetcode 1603.设计停车系统"
question_id: "1603"
question: "设计停车系统"
problem_url: "https://leetcode.cn/problems/design-parking-system/"
created: "2021-11-14T17:44:06+08:00"
updated: "2021-11-14T17:44:06+08:00"
upvotes: 0
comments: 0
---

# 1603. 设计停车系统

> **[yiduobo的每日leetcode 1603.设计停车系统](https://zhuanlan.zhihu.com/p/432312472) · 知乎 · 2021-11-14 · 赞同 0**
> 力扣：[1603. 设计停车系统](https://leetcode.cn/problems/design-parking-system/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1603.设计停车系统

[力扣](https://leetcode-cn.com/problems/design-parking-system/)

比较基础的题目，只需要统计各类车位的剩余数目，并根据当前需求的车位类型判断是否还有空余车位，并根据是否停车来修正各类车位的剩余数目即可。

最后附上python代码：

```python
class ParkingSystem(object):

    def __init__(self, big, medium, small):
        """
        :type big: int
        :type medium: int
        :type small: int
        """
        self.cnt_list = [big, medium, small]

    def addCar(self, carType):
        """
        :type carType: int
        :rtype: bool
        """
        if self.cnt_list[carType - 1] > 0:
            self.cnt_list[carType - 1] -= 1
            return True

        return False

# Your ParkingSystem object will be instantiated and called as such:
# obj = ParkingSystem(big, medium, small)
# param_1 = obj.addCar(carType)
```
