---
title: "2406. 将区间分为最少组数"
aliases: ["yiduobo的每日leetcode 2406.将区间分为最少组数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "leetcode/heap-priority-queue", "leetcode/ping-heng-shu", "leetcode/chai-fen", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/二-差分", "题单/常用数据结构/五-堆-优先队列", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/567888918"
zhihu_id: "567888918"
zhihu_title: "yiduobo的每日leetcode 2406.将区间分为最少组数"
question_id: "2406"
question: "将区间分为最少组数"
problem_url: "https://leetcode.cn/problems/divide-intervals-into-minimum-number-of-groups/"
difficulty: "Medium"
rating: 1713
created: "2022-09-25T03:31:57+08:00"
updated: "2022-09-25T03:31:57+08:00"
upvotes: 0
comments: 0
---

# 2406. 将区间分为最少组数

> **[yiduobo的每日leetcode 2406.将区间分为最少组数](https://zhuanlan.zhihu.com/p/567888918) · 知乎 · 2022-09-25 · 赞同 0**
> 力扣：[2406. 将区间分为最少组数](https://leetcode.cn/problems/divide-intervals-into-minimum-number-of-groups/) · Medium · 灵茶山艾府：[一题双解：贪心+堆 / 差分](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2406.将区间分为最少组数

[力扣](https://leetcode.cn/problems/divide-intervals-into-minimum-number-of-groups/)

贪心法的题目。对于区间合并类的问题，常规的做法是将所有区间按照起点或者按照终点进行排序，然后在合并时就可以通过这个序得到一些优良的性质从而起到优化的作用。

对于本题，我采用的是将区间按起点进行排序，那么对于排序后的某个区间\[left\[index\], right\[index\]\]而言，若其可以放在某个区间的后面，那么从index + 1往后的所有区间都可以放在那个区间的后面。换言之，在这里选择任意可用的区间，让\[left\[index\], right\[index\]\]接在其后面总是最优的。方便起见，就只需要判断当前已有区间中最小的终点是否小于left\[index\]，若是，那么就可以将\[left\[index\], right\[index\]\]放在这个区间的后面，否则就必须新增一个区间。

这样做还需要考虑一个问题是，有没有可能需要放弃某些区间，即对于某些区间不选择之前的区间进行拼接，而是单独新增一个区间，将拼接的机会留给后续的区间。由于题目要求每个区间都用上，因此在这里并不需要考虑这种情况。简单的证明如下：

对于某个区间\[left\[p\], right\[p\]\]而言：

1、如果选择该区间后\[left\[q\], right\[q\]\]也可以得到安置，那么并不需要新增区间

2、如果选择该区间会导致后续的某个区间\[left\[q\], right\[q\]\]无法放置的话，那么总计需要新增一个区间，同时会会得到一个以right\[p\]为结尾的区间和一个以right\[q\]为结尾的区间

3、如果放弃了\[left\[p\], right\[p\]\]，那么新增的区间就是以right\[p\]为结尾的区间，同时right\[q\]由于得到了放置，因此最终也是新增一个区间，同时依然是一个以right\[p\]为结尾的区间和一个以right\[q\]为结尾的区间

可以发现，选择安置区间\[left\[p\], right\[p\]\]，最坏情况下也只是与放弃区间\[left\[p\], right\[p\]\]相同，因此在遍历区间时，对于每个区间都应该尽可能地安置。

根据上面的结论就有了一种做法：首先将所有区间按起点从小到大进行排序，然后一趟遍历，使用一个堆维护当前划分出来的区间的右边界。对于当前遍历到的区间\[left\[index\], right\[index\]\]，若堆不为空，且left\[index\]大于堆顶表示的划分的右边界，那么说明当前的\[left\[index\], right\[index\]\]可以被放在堆顶这个划分的末尾，因此此时应该将堆顶弹出，并将right\[index\]加入到堆中。若不满足，那么就必须另起一个划分用来安置\[left\[index\], right\[index\]\]，因此在这种情况下不需要弹出堆顶，但还是要将right\[index\]加入到堆中。

遍历完成后，堆的大小就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def minGroups(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: int
        """

        end_pos = []
        for x, y in sorted(intervals, key=lambda d:d[0]):
            if end_pos and end_pos[0] < x:
                heapq.heappop(end_pos)
            heapq.heappush(end_pos, y)
        
        return len(end_pos)
```
