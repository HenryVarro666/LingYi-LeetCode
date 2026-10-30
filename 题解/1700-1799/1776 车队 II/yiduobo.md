---
title: "1776. 车队II"
aliases: ["yiduobo的每日leetcode 1776.车队II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/单调栈", "题单/常用数据结构/三-栈", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/462241419"
zhihu_id: "462241419"
zhihu_title: "yiduobo的每日leetcode 1776.车队II"
question_id: "1776"
question: "车队 II"
problem_url: "https://leetcode.cn/problems/car-fleet-ii/"
difficulty: "Hard"
rating: 2531
created: "2022-01-27T00:16:52+08:00"
updated: "2022-01-27T00:16:52+08:00"
upvotes: 0
comments: 0
---

# 1776. 车队II

> **[yiduobo的每日leetcode 1776.车队II](https://zhuanlan.zhihu.com/p/462241419) · 知乎 · 2022-01-27 · 赞同 0**
> 力扣：[1776. 车队 II](https://leetcode.cn/problems/car-fleet-ii/) · Hard · 灵茶山艾府：[倒序遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1776.车队II

[力扣](https://leetcode-cn.com/problems/car-fleet-ii/)

根据题目的描述可知，对于一个车队而言，其能否追上前面的车队只取决于其自身和前面的车队，与其后面的车队没有关系，因为后面的车队一旦追上来当前车队，就会变成当前车队的一部分，且不会影响当前车队的速度。

有了这个结论，在这里显然就应该从最远的车队开始向前逆推，分别计算每个车队追上前队的时间。

一个车队能追上前队必须要这个车队的速度比前队的速度要快，又或者是前队融入了更前面的队伍导致速度被拉低到更前面队伍的水平，且这个速度比当前车队的速度要慢。简单来说，就是当前车队的前方必须存在速度比当前车队要慢的车队，才有可能发生追及事件。

在这里就可以先考虑一个特殊情况，即对于某个车队p而言，其前面的车队的最小速度大于p的速度。此时p是不可能追上前队的，因此p对应的答案就是-1。同时，p后方的车队也不可能再追上p前方的车队，因此可以认为这里的p变成了最靠前的那个车队。

而对于一般情况，设当前车队为p，根据最上面的结论可知，无论p是否追上p + 1，都不影响p + 1追上p + 2的时间。因此实际上这里需要判断的就是在p + 1追上p + 2之前p能否追上p + 1。幸运的是，由于是倒过来计算的，因此在计算p之前已经知道了p + 1追上p + 2所需的时间，那么此时就只需要通过计算p和p + 1之间的速度差，乘以时间后对于p和p + 1之间的距离，就可以知道在p + 1追上p + 2之前p能否追上p + 1了。

若可以，那么可以通过距离差和速度差直接计算出p对应的答案，若不可以，那么此时p + 1会率先一步加入到p + 2的车队当中，而问题就变成了计算在p+ 2追上p + 3之前p能否追上p + 2，以此类推。

可以发现，在这里直接计算复杂度是O(n)的，那么最终的时间复杂度就是O(n^2)，在这里是无法接受的。

依然是根据最上面的结论，可以发现当确定在p + 1并入p + 2之前p无法追上p + 1，那么p - 1以及后面的车队就更不可能追上p + 1了，换言之，在这里就没有保留p + 1的意义了。对于这种操作方式，可以使用熟悉的单调栈来进行适配。具体来说就是对于当前车队，计算其能否在栈顶车队追上更前面的车队之前，先追上当前栈顶的车队。若不能追上，那么说明栈顶车队已经没有保留的价值了，那么将其从栈顶弹出。重复此过程直到栈为空或者当前车队可以追上栈顶的车队。若栈为空，说明原来栈中所有车队的速度都大于等于当前车队的速度，那么当前车队对应的答案就是-1，否则这个追及的时间自然也是通过栈顶车队与当前车队的距离差和速度差来计算。最后还需要将当前车队加入到栈中，然后继续考察前一个车队。

由于每个车队最多进出栈一次，因此这里的时间复杂度就是均摊O(1)的，从而将整体时间复杂度优化到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def getCollisionTimes(self, cars):
        """
        :type cars: List[List[int]]
        :rtype: List[float]
        """

        n = len(cars)
        res = [-1] * n
        stack = [n - 1]
        for index in range(n - 1, -1, -1):
            if cars[index][1] <= cars[stack[0]][1]:
                res[index] = -1
                stack = [index]
            else:
                while len(stack) > 1 and (cars[index][1] - cars[stack[-1]][1]) * res[stack[-1]] < cars[stack[-1]][0] - cars[index][0]:
                    stack.pop()
                
                res[index] = (cars[stack[-1]][0] - cars[index][0]) * 1.0 / (cars[index][1] - cars[stack[-1]][1])
                stack.append(index)
        
        return res
```
