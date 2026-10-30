---
title: "1199. 建造街区的最短时间"
aliases: ["yiduobo的每日leetcode 1199.建造街区的最短时间"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/613021717"
zhihu_id: "613021717"
zhihu_title: "yiduobo的每日leetcode 1199.建造街区的最短时间"
question_id: "1199"
question: "建造街区的最短时间"
problem_url: "https://leetcode.cn/problems/minimum-time-to-build-blocks/"
created: "2023-03-10T21:51:05+08:00"
updated: "2023-03-10T21:51:05+08:00"
upvotes: 0
comments: 0
---

# 1199. 建造街区的最短时间

> **[yiduobo的每日leetcode 1199.建造街区的最短时间](https://zhuanlan.zhihu.com/p/613021717) · 知乎 · 2023-03-10 · 赞同 0**
> 力扣：[1199. 建造街区的最短时间](https://leetcode.cn/problems/minimum-time-to-build-blocks/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1199.建造街区的最短时间

[力扣](https://leetcode.cn/problems/minimum-time-to-build-blocks/)

建造时间越长，可以完成建造的可能性就越大，这也就意味着本题可以通过二分这个最短的建造时间，将问题转化为判定问题。

对于建造的流程，应该是

分裂若干轮 -> 选择一个工人开始执行建造 -> 继续分裂 -> 继续选择一个工人开始建造 -> ...

这样重复一共n次，这里的n是街区的数量，同时每一层的分裂轮次都是非负数。

为了使得最终花费的时间最少，就应该将耗时最久的建造尽量放在前面。同时由于二分了最短的建造时间mid，那么就可以通过mid减去下一个计划建造的街区得到分裂的时间，也就是rest_time \= mid - block[i]。更进一步的，使用rest_time / split就得到了分裂的轮次。到了这里，就可以在一趟遍历的时间内计算出每一次分裂出来的工人数量。若在这个过程中工人始终是够用的，或者某一轮分裂后的工人已经大于后续剩余街区的数量，那么说明当前二分的mid是足够的，此时应该更新二分上界，否则应该更新二分下界。

需要特别注意的是，在计算过程中分裂的轮次可能非常大，如果直接计算分裂后的人数是不太好的选择。注意到街区数量不超过1000，那么若某次分裂的轮次超过了10，那么在分裂后工人的数量必然大于1000，这种情况下就可以直接调整二分上界了。

另外，如果在最后这个街区的建造之后工人数量变成了0，这种情况下也同样应该调整二分上界，因此对于剩余工人的判断应该放在每次分裂-建造操作的前面。

最后附上python代码：

```python
class Solution(object):
    def minBuildTime(self, blocks, split):
        """
        :type blocks: List[int]
        :type split: int
        :rtype: int
        """

        blocks.sort(reverse=True)

        n = len(blocks)
        left = blocks[0]
        right = blocks[0] + (n - 1) * split

        while left < right:
            mid = (left + right) / 2

            idle = 1
            flag = True
            last_rnd = 0

            for index, t in enumerate(blocks):
                if idle == 0:
                    flag = False
                    break
                rest_time = mid - t
                rnd = rest_time / split

                if rnd - last_rnd >= 10:
                    break
                
                idle <<= (rnd - last_rnd)
                if idle >= n - index:
                    break
                
                last_rnd = rnd
                idle -= 1

            if flag:
                right = mid
            else:
                left = mid + 1
        
        return left
```
