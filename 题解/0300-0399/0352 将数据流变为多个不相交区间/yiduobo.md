---
title: "352. 将数据流变为多个不相交区间"
aliases: ["yiduobo的每日leetcode 352.将数据流变为多个不相交区间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/163661021"
zhihu_id: "163661021"
zhihu_title: "yiduobo的每日leetcode 352.将数据流变为多个不相交区间"
question_id: "352"
question: "将数据流变为多个不相交区间"
problem_url: "https://leetcode.cn/problems/data-stream-as-disjoint-intervals/"
created: "2020-07-25T17:18:39+08:00"
updated: "2020-07-25T17:18:39+08:00"
upvotes: 0
comments: 0
---

# 352. 将数据流变为多个不相交区间

> **[yiduobo的每日leetcode 352.将数据流变为多个不相交区间](https://zhuanlan.zhihu.com/p/163661021) · 知乎 · 2020-07-25 · 赞同 0**
> 力扣：[352. 将数据流变为多个不相交区间](https://leetcode.cn/problems/data-stream-as-disjoint-intervals/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

352.将数据流变为多个不相交区间<https://leetcode-cn.com/problems/data-stream-as-disjoint-intervals/>

这个题目需要使用某种数据结构维护当前区间的情况，然后对于新来的一个数，首先通过比较区间左端点找到这个数应该位于哪两个区间之间，然后判断这个数：

1、形成新的独立区间。此时需要将这个新区间插入到数据结构中。

2、融入左侧或者右侧的区间。此时只需要修改对应区间的左端点或右端点。

3、连接两个区间。此时需要将右侧区间从数据结构中删去，并更新左侧区间的右端点。

可以发现，在这里需要高效地在数据结构中进行按序查找以及插入删除，于是首选自然是平衡树。不过平衡树实现起来相对复杂，所以我在这里偷懒使用的是list，查找则通过二分来进行。理论上来说最坏能达到n^2的复杂度，不过这里的测试数据还算比较友好。

于是现在的做法就是一趟扫描，对于每个数x：

1、若当前list为空，那么将区间[x, x]加入list。

2、若x小于list[0]的左端点list[0][0]，那么需要判断x是否刚好邻接list[0]的左侧。如果是，那么只需要扩展list[0]的左端点，否则需要将[x, x]作为新区间加入到list头部。插入头部的操作时间复杂度为O(n)。

3、若x大于list[-1]的左端点list[-1][0]，那么需要判断x是否位于list[-1]中。如果是，那么无事发生，否则需要判断x是否刚好邻接list[-1]的右侧。如果是，那么只需要扩展list[-1]的右端点，否则需要将[x, x]作为新区间加入到list尾部。

4、此时可以确定，一定存在pos，满足list[pos][0] \<\= x \< list[pos][1]，于是可以通过二分法找到这个pos，然后分别判断x是否位于list[pos]中，是否邻接list[pos]的右端点，以及是否临接list[pos + 1]的左端点。

1）若x位于list[pos]中，那么此时无事发生。

2）若x邻接list[pos]的右端点，且同时邻接list[pos + 1]的左端点，那么此时需要将list[pos]和list[pos + 1]进行合并。这一步的时间复杂度为O(n)。

3）若x仅邻接list[pos]的右端点但不邻接list[pos + 1]的左端点，那么此时只需要扩展list[pos]的右端点。

4）若x仅邻接list[pos + 1]的左端点但不邻接list[pos]的右端点，那么此时只需要扩展 list[pos + 1]的左端点。

5）若不满足上面的条件，那么此时需要将[x, x]作为新区间插入到list[pos]和list[pos + 1]之间。这一步的时间复杂度为O(n)。

因此，上述算法的理论时间复杂度应该为O(n^2)。当使用平衡树替代list时，这些O(n)的操作都能优化为O(logn)。

最后附上python代码：

```python
class SummaryRanges(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.interval_list = []

    def addNum(self, val):
        """
        :type val: int
        :rtype: None
        """
        if not self.interval_list:
            self.interval_list = [[val, val]]
        
        elif val < self.interval_list[0][0]:
            if val == self.interval_list[0][0] - 1:
                self.interval_list[0][0] -= 1
            else:
                self.interval_list = [[val, val]] + self.interval_list
        
        elif val > self.interval_list[-1][0]:
            if val <= self.interval_list[-1][1]:
                pass
            elif val == self.interval_list[-1][1] + 1:
                self.interval_list[-1][1] += 1
            else:
                self.interval_list.append([val, val])

        else:
            l = 0
            r = len(self.interval_list) - 1
            pos = None
            while l <= r:
                mid = (l + r) / 2
                if self.interval_list[mid][0] == val:
                    return
                elif self.interval_list[mid][0] < val:
                    pos = mid
                    l = mid + 1
                else:
                    r = mid - 1

            if val <= self.interval_list[pos][1]:
                return
            
            if val == self.interval_list[pos][1] + 1:
                if self.interval_list[pos + 1][0] - 1 == val:
                    self.interval_list = self.interval_list[:pos] + [[self.interval_list[pos][0], self.interval_list[pos + 1][1]]] + self.interval_list[pos + 2:]
                else:
                    self.interval_list[pos][1] += 1
            elif self.interval_list[pos + 1][0] - 1 == val:
                self.interval_list[pos + 1][0] -= 1
            else:
                self.interval_list = self.interval_list[:pos + 1] + [[val, val]] + self.interval_list[pos + 1:]

    def getIntervals(self):
        """
        :rtype: List[List[int]]
        """
        return self.interval_list

# Your SummaryRanges object will be instantiated and called as such:
# obj = SummaryRanges()
# obj.addNum(val)
# param_2 = obj.getIntervals()
```
