---
title: "3516. 找到最近的人"
aliases: ["yiduobo的每日leetcode 3516.找到最近的人"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902541771625444167"
zhihu_id: "1902541771625444167"
zhihu_title: "yiduobo的每日leetcode 3516.找到最近的人"
question_id: "3516"
question: "找到最近的人"
problem_url: "https://leetcode.cn/problems/find-closest-person/"
difficulty: "Easy"
created: "2025-05-08T00:09:01+08:00"
updated: "2025-05-08T00:09:01+08:00"
upvotes: 0
comments: 0
---

# 3516. 找到最近的人

> **[yiduobo的每日leetcode 3516.找到最近的人](https://zhuanlan.zhihu.com/p/1902541771625444167) · 知乎 · 2025-05-08 · 赞同 0**
> 力扣：[3516. 找到最近的人](https://leetcode.cn/problems/find-closest-person/) · Easy · 灵茶山艾府：[计算绝对值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3516.找到最近的人

[3516. 找到最近的人 - 力扣（LeetCode）](https://leetcode.cn/problems/find-closest-person/description/)

题目给出三个整数x、y、z，表示数轴上的三个人的位置。其中x和y分别是第一个人和第二个人的位置，z是第三个人的位置，且第三个人是不会移动的。

第一个人和第二个人会以相同的速度向第三个人移动。问谁先到达第三个人的位置。

题目实际上就是需要判断x和y哪个与z的距离更近，因此只需分别计算x和y与z的差的绝对值就行了。

最后附上python代码：

```python
class Solution(object):
    def findClosest(self, x, y, z):
        """
        :type x: int
        :type y: int
        :type z: int
        :rtype: int
        """
        
        dis_x = abs(x - z)
        dis_y = abs(y - z)
        if dis_x < dis_y:
            return 1
        if dis_x > dis_y:
            return 2
        return 0
```
