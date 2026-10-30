---
title: "2895. 最小处理时间"
aliases: ["yiduobo的每日leetcode 2895.最小处理时间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/662966063"
zhihu_id: "662966063"
zhihu_title: "yiduobo的每日leetcode 2895.最小处理时间"
question_id: "2895"
question: "最小处理时间"
problem_url: "https://leetcode.cn/problems/minimum-processing-time/"
difficulty: "Medium"
rating: 1352
created: "2023-10-23T23:22:12+08:00"
updated: "2023-10-23T23:22:12+08:00"
upvotes: 0
comments: 0
---

# 2895. 最小处理时间

> **[yiduobo的每日leetcode 2895.最小处理时间](https://zhuanlan.zhihu.com/p/662966063) · 知乎 · 2023-10-23 · 赞同 0**
> 力扣：[2895. 最小处理时间](https://leetcode.cn/problems/minimum-processing-time/) · Medium · 灵茶山艾府：[贪心及其证明：交换论证法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2895.最小处理时间

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-processing-time/)

题目中处理器的处理能力相同，为了使得总的处理时间最小，那么就应该让最早空闲的处理器来处理最耗时的任务，而确定了最耗时的任务用哪个处理器来处理后，此时剩余任务中耗时最大的前三个任务就应该也交给这个处理器进行处理，这样一来并不会影响当前的处理时间，又可以使得留给其他处理器的任务更容易处理。

根据这个结论，只需将处理器按空闲时间从小到大进行排序，然后将任务按耗时从大到小进行排序，接下来一趟遍历，将任务按4个一组分给对应下标的处理器就行了，最终耗时则是所有processorTime[index] + tasks[index \* 4]中的最大值。

最后附上python代码：

```python
class Solution(object):
    def minProcessingTime(self, processorTime, tasks):
        """
        :type processorTime: List[int]
        :type tasks: List[int]
        :rtype: int
        """

        processorTime.sort()
        tasks.sort(reverse=True)
        return max([processorTime[index] + tasks[index * 4] for index in range(len(processorTime))])
```
