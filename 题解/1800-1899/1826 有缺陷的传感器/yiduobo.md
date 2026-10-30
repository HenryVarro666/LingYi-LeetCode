---
title: "1826. 有缺陷的传感器"
aliases: ["yiduobo的每日leetcode 1826.有缺陷的传感器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/622077307"
zhihu_id: "622077307"
zhihu_title: "yiduobo的每日leetcode 1826.有缺陷的传感器"
question_id: "1826"
question: "有缺陷的传感器"
problem_url: "https://leetcode.cn/problems/faulty-sensor/"
created: "2023-04-15T02:25:31+08:00"
updated: "2023-04-15T02:25:31+08:00"
upvotes: 0
comments: 0
---

# 1826. 有缺陷的传感器

> **[yiduobo的每日leetcode 1826.有缺陷的传感器](https://zhuanlan.zhihu.com/p/622077307) · 知乎 · 2023-04-15 · 赞同 0**
> 力扣：[1826. 有缺陷的传感器](https://leetcode.cn/problems/faulty-sensor/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1826.有缺陷的传感器

[力扣](https://leetcode.cn/problems/faulty-sensor/)

首先一趟遍历，找出两个数组中第一次数值不相等的下标p。若找不到p，说明两个数组相同，此时直接返回-1。

对于p存在的情况，暂时还无法确定是哪个传感器出问题，因此需要分别进行校验。

若第一个传感器出了问题，那么其数组的最后一个数字必然不能与第二个数组在下标p的数字相同，同时其从p开始直到倒数第二个数字的子数组也必须与第二个数组从下标p开始直到末尾的子数组完全相同。若符合这两个条件，说明第一个传感器有问题。

对于第二个传感器也需要按照上面方法对称来进行判断。

若仅有一个传感器有问题，那么就返回对应的数字，否则返回-1。

最后附上python代码：

```python
class Solution(object):
    def badSensor(self, sensor1, sensor2):
        """
        :type sensor1: List[int]
        :type sensor2: List[int]
        :rtype: int
        """

        n = len(sensor1)
        p = 0
        while p < n and sensor1[p] == sensor2[p]:
            p += 1
        
        if p == n:
            return -1
        
        flag1 = False
        if sensor2[p] != sensor1[-1] and sensor1[p : n - 1] == sensor2[p + 1:]:
            flag1 = True
        
        flag2 = False
        if sensor1[p] != sensor2[-1] and sensor2[p : n - 1] == sensor1[p + 1:]:
            flag2 = True
        
        if flag1:
            if flag2:
                return -1
            else:
                return 1
        elif flag2:
            return 2
        else:
            return -1
```
