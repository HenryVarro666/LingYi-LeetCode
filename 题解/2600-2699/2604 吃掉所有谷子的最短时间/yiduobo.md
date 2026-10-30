---
title: "2604. 吃掉所有谷子的最短时间"
aliases: ["yiduobo的每日leetcode 2604.吃掉所有谷子的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/644917956"
zhihu_id: "644917956"
zhihu_title: "yiduobo的每日leetcode 2604.吃掉所有谷子的最短时间"
question_id: "2604"
question: "吃掉所有谷子的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-eat-all-grains/"
created: "2023-07-21T02:43:55+08:00"
updated: "2023-07-21T02:43:55+08:00"
upvotes: 0
comments: 0
---

# 2604. 吃掉所有谷子的最短时间

> **[yiduobo的每日leetcode 2604.吃掉所有谷子的最短时间](https://zhuanlan.zhihu.com/p/644917956) · 知乎 · 2023-07-21 · 赞同 0**
> 力扣：[2604. 吃掉所有谷子的最短时间](https://leetcode.cn/problems/minimum-time-to-eat-all-grains/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2604.吃掉所有谷子的最短时间

[力扣](https://leetcode.cn/problems/minimum-time-to-eat-all-grains/)

首先，每只鸡吃谷子的路线是不会出现重叠的，因为对于重叠的部分，只需要其中一只鸡经过就行了，而另一只鸡则可以通过节省掉走这一段重叠部分的时间来吃更多其他的谷子。如果将所有的鸡和谷子都按坐标从小到大进行排序的话，那么就可以将谷子拆分成若干个区间，依次交给每只鸡来负责。

接下来的问题就是如何确定拆分谷子。注意到时间越长，吃掉所有谷子的可能性就越大，因此在这里可以使用二分法，二分吃掉所有谷子的最短时间mid，那么在拆分谷子时，就可以在耗时不超过mid的前提下尽量多进行拆分。

对于某只位于下标h的鸡而言，其负责的区间与h的大小关系可能有三种情况：

1、区间中所有谷子都位于h前方

2、区间中所有谷子都位于h后方

3、区间中部分谷子位于h前方，其他谷子位于h后方

对于上面这三种情况，其中前两种的耗时是很好计算的，即从h出发走到区间中距离最远谷子所在下标的距离。

而对于情况3，则存在“先往前走，再折回到h，再往后”以及“先往后走，再折回到h，再往前”这两种走法。前者的耗时为从h出发走到前方最远谷子的距离的两倍，再加上从h出发走到后方最远处谷子的距离；后者的耗时则反过来，也就是从h出发走到后方最远谷子的距离的两倍，再加上从h出发走到前方最远谷子的距离。换言之，在这里只需要知道前方最远处谷子的位置以及后方最远处谷子的位置就可以计算出耗时了。

更进一步的，如果认为情况1中后方最远处谷子就位于h，情况2中前方最远处谷子也位于h，那么情况1和情况2就可以认为是情况3的特例，可以直接套用情况3相同的计算方法来计算耗时。

到了这里，就得到了一种分配谷子的方式。

对于当前遍历到的母鸡，不妨设其位于h，那么先初始化其前方和后方最远处的谷子位置为h。接下来，遍历当前还未分配的谷子。若当前未分配谷子中最靠前谷子的下标小于h，那么就使用这个谷子的下标来更新母鸡前方最远处谷子的下标，否则就更新母鸡后方最远处谷子的下标。接下来，按照上面描述计算耗时，并取较小的那一种作为母鸡吃掉当前分配谷子所需的耗时。若这个耗时不超过mid，那么说明可以将当前剩余谷子中最靠前的谷子分配给当前母鸡，此时可以继续向后考虑其他谷子；反之，该谷子就不能分配给当前母鸡，需要继续考虑后续的母鸡。若某一时刻所有谷子都分配出去了，那么说明当前的耗时mid足够，此时更新二分的上界为mid，否则更新二分的下界为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minimumTime(self, hens, grains):
        """
        :type hens: List[int]
        :type grains: List[int]
        :rtype: int
        """

        hens.sort()
        grains.sort()

        left = 0
        right = abs(hens[0] - grains[0]) + grains[-1] - grains[0]

        while left < right:
            mid = (left + right) >> 1
            p = 0
            for h in hens:
                backward = forward = 0
                while p < len(grains):
                    if grains[p] < h:
                        forward = max(forward, h - grains[p])
                    elif grains[p] > h:
                        backward = max(backward, grains[p] - h)
                    
                    if forward + forward + backward <= mid or backward + backward + forward <= mid:
                        p += 1
                    else:
                        break
                
                if p == len(grains):
                    break
            
            if p == len(grains):
                right = mid
            else:
                left = mid + 1

        return left
```
