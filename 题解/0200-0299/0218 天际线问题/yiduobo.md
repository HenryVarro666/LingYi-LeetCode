---
title: "218. 天际线问题"
aliases: ["yiduobo的每日leetcode 218.天际线问题"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/148267776"
zhihu_id: "148267776"
zhihu_title: "yiduobo的每日leetcode 218.天际线问题"
question_id: "218"
question: "天际线问题"
problem_url: "https://leetcode.cn/problems/the-skyline-problem/"
created: "2020-06-14T19:48:51+08:00"
updated: "2020-06-14T19:48:51+08:00"
upvotes: 0
comments: 0
---

# 218. 天际线问题

> **[yiduobo的每日leetcode 218.天际线问题](https://zhuanlan.zhihu.com/p/148267776) · 知乎 · 2020-06-14 · 赞同 0**
> 力扣：[218. 天际线问题](https://leetcode.cn/problems/the-skyline-problem/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

218.天际线问题<https://leetcode-cn.com/problems/the-skyline-problem/>

一个很直观的想法是对于所有的x，找出当前的最大高度，然后如果这个最大高度出现了变化，那么说明有转折点。注意到转折点只可能出现在建筑的左边界或者右边界，那么实际上x只需要在所有建筑的左右边界中遍历即可。另外，涉及到最大值的问题，经典的做法就是运用堆来进行维护，于是现在就有了一种做法：

从左往右扫描，若当前点是某个建筑的左边界，则将其高度加入堆中，若是某个建筑的右边界，则将其高度从堆中删去。完成堆的操作后，堆顶值为现在建筑的最高高度，将其记录下来。若该高度与上一个扫描点的最高高度不同，那么说明出现了转折点，将其加入到答案即可。

对于样例来说，边界点分别为：

左边界为[2, 10], [3, 15], [5, 12], [15, 10], [19, 8]

右边界为[9, 10], [7, 15], [12, 12], [20, 10], [24, 8]

按边界点从左往右扫描，那么扫描顺序为：

左边界[2, 10] -> 左边界[3, 15] -> 左边界[5, 12] - > 右边界[7, 15] -> 右边界[9, 10] ->

右边界[12, 12] -> 左边界[15, 10] -> 左边界[19, 8] -> 右边界[20, 10] -> 右边界[24, 8]

此时堆中的情况为：

1、左边界[2, 10]，将一个10加入堆中，此时堆中元素为10，堆顶元素为10，产生了转折点(2, 10)

2、左边界[3, 15]，将一个15加入堆中，此时堆中元素为10、15，堆顶元素为15，产生了转折点(3, 15)

3、左边界[5, 12]，将一个12加入堆中，此时堆中元素为10、15、12，堆顶元素为15，不是转折点

4、右边界[7, 15]，需要从堆中移除一个15，堆中剩余10、12，堆顶元素为12，产生了转折点(7, 12)

5、右边界[9, 10]，需要从堆中移除一个10，堆中剩余12，堆顶元素为12，不是转折点

6、右边界[12, 12]，需要从堆中移除一个12，堆为空，默认高度为0，产生了转折点(12, 0)

7、左边界[15, 10]，将一个10加入堆中，此时堆中元素为10，堆顶元素为10，产生了转折点(15, 10)

8、左边界[19, 8]，将一个8加入堆中，此时堆中元素为10、8，堆顶元素为10，不是转折点

9、右边界[20, 10]，需要从堆中移除一个10，堆中剩余8，堆顶元素为8，产生了转折点(20, 8)

10、右边界[24, 8]，需要从堆中移除一个8，堆为空，默认高度为0，产生了转折点(24, 0)

于是最后的答案就是\[\[2, 10\], \[3, 15\], \[7, 12\], \[12, 0\], \[15, 10\], \[20, 8\], \[24, 0\]\]

需要注意的是，当某个点是多个建筑的左边界或者右边界时，需要优先完成堆的操作，再取堆顶判断是否是转折点。

由于对python的堆操作不熟悉，于是在这里自己手写了一个堆。堆中节点除了高度值height之外，还加入了频率值，表示现在堆中有几个高度为height的值，这样一来遇到插入或者删除操作的时候需要对应地修正这个频率值，当频率值为0时才从堆中删去对应节点。

另外，将右边界的高度记录为负数，用来区分左右边界。

每个左边界与右边界最多入堆一次，复杂度O(logn)，而每次查询的复杂度则是常数，因此最终的时间复杂度为O(nlogn)。

最后附上python代码，其中height_dict为按横坐标记录的高度：

```python
import Queue

class Solution(object):    

    def getSkyline(self, buildings):
        """
        :type buildings: List[List[int]]
        :rtype: List[List[int]]
        """

        height_dict = {}
        for left, right, height in buildings:
            if left not in height_dict:
                height_dict[left] = []
            if right not in height_dict:
                height_dict[right] = []

            height_dict[left].append(-height)
            height_dict[right].append(height)

        max_height = [[]]
        pos_dict = {}
        last_height = 0
        res = []

        for x in sorted(height_dict.keys()):
            for height in height_dict[x]:
                if height < 0:
                    height = -height
                    if height in pos_dict:
                        max_height[pos_dict[height]][1] += 1
                    else:
                        max_height.append([height, 1])
                        now = len(max_height) - 1
                        while now > 1 and height > max_height[now / 2][0]:
                            max_height[now] = max_height[now / 2]
                            pos_dict[max_height[now / 2][0]] = now
                            now /= 2
                        max_height[now] = [height, 1]
                        pos_dict[height] = now
                
                else:
                    pos = pos_dict[height]
                    max_height[pos][1] -= 1
                    if max_height[pos][1] == 0:
                        max_height[pos] = max_height[-1]
                        max_height.pop()
                        while True:
                            left = pos + pos
                            right = left + 1
                            left_flag = right_flag = False
                            if left < len(max_height) and max_height[pos][0] < max_height[left][0]:
                                left_flag = True
                            if right < len(max_height) and max_height[pos][0] < max_height[right][0]:
                                right_flag = True

                            if not left_flag:
                                if not right_flag:
                                    break
                                else:
                                    pos_dict[max_height[right][0]] = pos
                                    max_height[right], max_height[pos] = max_height[pos], max_height[right]
                                    pos = right
                            else:
                                if not right_flag or max_height[left][0] > max_height[right][0]:
                                    pos_dict[max_height[left][0]] = pos
                                    max_height[left], max_height[pos] = max_height[pos], max_height[left]
                                    pos = left
                                else:
                                    pos_dict[max_height[right][0]] = pos
                                    max_height[right], max_height[pos] = max_height[pos], max_height[right]
                                    pos = right

                        if pos < len(max_height):
                            pos_dict[max_height[pos][0]] = pos
                        pos_dict.pop(height)

            if len(max_height) == 1:
                now_height = 0
            else:
                now_height = max_height[1][0]

            if not res or res[-1][1] != now_height:
                res.append([x, now_height])

        return res
```
