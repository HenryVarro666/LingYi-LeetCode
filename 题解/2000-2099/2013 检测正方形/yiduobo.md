---
title: "2013. 检测正方形"
aliases: ["yiduobo的每日leetcode 2013.检测正方形"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/505027600"
zhihu_id: "505027600"
zhihu_title: "yiduobo的每日leetcode 2013.检测正方形"
question_id: "2013"
question: "检测正方形"
problem_url: "https://leetcode.cn/problems/detect-squares/"
difficulty: "Medium"
created: "2022-04-25T23:53:09+08:00"
updated: "2022-04-25T23:53:09+08:00"
upvotes: 0
comments: 0
---

# 2013. 检测正方形

> **[yiduobo的每日leetcode 2013.检测正方形](https://zhuanlan.zhihu.com/p/505027600) · 知乎 · 2022-04-25 · 赞同 0**
> 力扣：[2013. 检测正方形](https://leetcode.cn/problems/detect-squares/) · Medium · 灵茶山艾府：[枚举底边或顶边](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2013.检测正方形

[力扣](https://leetcode-cn.com/problems/detect-squares/)

题目保证了正方形每条边都与坐标轴平行或者垂直，那么对于要求解的点(x, y)，可以枚举与该点的横坐标相同的点，其坐标可以写作(x, y2)。

这两个点纵坐标之差就是正方形的边长，即abs(y - y2)。

接下来，(x, y)以及(x, y2)可以与(x - abs(y - y2), y)以及(x - abs(y - y2), y2)形成合法的正方形。除此之外，也可以与(x + abs(y - y2), y)以及(x + abs(y - y2), y2)形成合法的正方形。此时只需要通过哈希表找出这些坐标上的点有多少个，就可以计算出可以形成的合法正方形数量。

那么在这里，只需要在add的过程中使用哈希表统计每个坐标上点的数量，然后根据上面的方法求解每个count的答案。

最后附上python代码：

```python
class DetectSquares(object):

    def __init__(self):
        self.point_dict = {}

    def add(self, point):
        """
        :type point: List[int]
        :rtype: None
        """
        x, y = point
        if x not in self.point_dict:
            self.point_dict[x] = {}
        self.point_dict[x][y] = self.point_dict[x].get(y, 0) + 1

    def count(self, point):
        """
        :type point: List[int]
        :rtype: int
        """
        x, y = point
        if x not in self.point_dict:
            return 0

        res = 0
        for y2 in self.point_dict[x]:
            if y2 == y:
                continue

            if x - abs(y - y2) in self.point_dict:
                res += self.point_dict[x][y2] * self.point_dict[x - abs(y - y2)].get(y, 0) * self.point_dict[x - abs(y - y2)].get(y2, 0)
            
            if x + abs(y - y2) in self.point_dict:
                res += self.point_dict[x][y2] * self.point_dict[x + abs(y - y2)].get(y, 0) * self.point_dict[x + abs(y - y2)].get(y2, 0)
        
        return res
            

# Your DetectSquares object will be instantiated and called as such:
# obj = DetectSquares()
# obj.add(point)
# param_2 = obj.count(point)
```
