---
title: "LCP 12. 小张刷题计划"
aliases: ["yiduobo的每日leetcode LCP12.小张刷题计划"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/571113112"
zhihu_id: "571113112"
zhihu_title: "yiduobo的每日leetcode LCP12.小张刷题计划"
question_id: "LCP 12"
question: "小张刷题计划"
problem_url: "https://leetcode.cn/problems/xiao-zhang-shua-ti-ji-hua/"
created: "2022-10-07T03:06:33+08:00"
updated: "2022-10-07T03:06:33+08:00"
upvotes: 0
comments: 0
---

# LCP 12. 小张刷题计划

> **[yiduobo的每日leetcode LCP12.小张刷题计划](https://zhuanlan.zhihu.com/p/571113112) · 知乎 · 2022-10-07 · 赞同 0**
> 力扣：[LCP 12. 小张刷题计划](https://leetcode.cn/problems/xiao-zhang-shua-ti-ji-hua/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP12.小张刷题计划

[力扣](https://leetcode.cn/problems/xiao-zhang-shua-ti-ji-hua/)

经典二分问题的某个变种，但是依然可以继续使用二分法来处理。，T越大，每天能刷的题只会多不会少，总的有时必然是更少的。

接下来的问题就是应该在何时使用场外求助。最直观的想法就是将求助机会留给当天做的题中最难的那个，这样节省的时间就会更多。

于是只需二分每天的做题时间mid，其中二分的左右边界分别为0和一次性做完所有题需要的总时间。

对于当前的mid，则需要模拟计算单天做题时间不超过mid的情况下需要多少天做完全部的题目。使用一个变量p记录做到了哪一题，然后从p开始向后遍历，使用当前题目的time[p]更新当天做题的总耗时s以及单题的最大耗时ma，直到某一时刻s - ma > mid或者做完了全部的题目。若s - ma > mid，说明即使通过场外求助解决了最难的题，剩下的题的总耗时依然超过了限制，那么说明当天做的最后一题必须留给下一天来做，此时就应该更新所需天数cnt，并将s和ma置为0，再从当前的p开始向后遍历。重复此过程直到做完了全部的题目或者cnt等于m。

若最终做完了全部的题目，说明当前的mid是可行的，且还可能有向下调整的空间，因此需要将二分的右边界r更新为mid，否则需要将左边界l更新为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minTime(self, time, m):
        """
        :type time: List[int]
        :type m: int
        :rtype: int
        """

        l = 0
        r = sum(time)

        while l < r:
            mid = (l + r) / 2
            p = 0
            ma = 0
            s = 0
            cnt = 0
            while p < len(time):
                ma = max(ma, time[p])
                s += time[p]
                if s - ma > mid:
                    cnt += 1
                    if cnt == m:
                        break
                    ma = 0
                    s = 0
                    continue
                p += 1
            
            if p == len(time):
                r = mid
            else:
                l = mid + 1
        
        return l
```
