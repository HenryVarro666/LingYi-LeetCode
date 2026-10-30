---
title: "LCP 32. 批量处理任务"
aliases: ["yiduobo的每日leetcode LCP32.批量处理任务"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/greedy", "leetcode/sorting", "leetcode/monotonic-stack", "题单/贪心算法", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/574151544"
zhihu_id: "574151544"
zhihu_title: "yiduobo的每日leetcode LCP32.批量处理任务"
question_id: "LCP 32"
question: "批量处理任务"
problem_url: "https://leetcode.cn/problems/t3fKg1/"
difficulty: "Hard"
created: "2022-10-16T20:08:21+08:00"
updated: "2022-10-16T20:08:21+08:00"
upvotes: 1
comments: 0
---

# LCP 32. 批量处理任务

> **[yiduobo的每日leetcode LCP32.批量处理任务](https://zhuanlan.zhihu.com/p/574151544) · 知乎 · 2022-10-16 · 赞同 1**
> 力扣：[LCP 32. 批量处理任务](https://leetcode.cn/problems/t3fKg1/) · Hard · 灵茶山艾府：[贪心+栈优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP32.批量处理任务

[力扣](https://leetcode.cn/problems/t3fKg1/)

题目的数据规模非常大，而且没有什么好的动态规划的状态表示方法，那么只能想办法用贪心来处理。

对于这类区间类的问题，如果想要贪心，常规的做法是先将区间按照起点或者终点进行排序。对于本题，选择对区间的终点排序是比较自然的想法，因为排序之后，如果尽量将靠前区间的后半部分时间开机的话，就更有可能惠及到后续的区间。反过来，如果按起点排序的话，则可能出现区间靠前的区间完全包裹住了靠后的区间，此时选择将靠前区间的后半部分开机可能无法照顾到靠后的区间。

那么现在的算法就是：

1、将原始区间按终点从小到大进行排序

2、使用一个数组open_list记录当前已经开机的时间段，接下来遍历所有的原始区间。对于当前区间，首先计算已有的开机时间，若当前区间还需要更多的开机时间，则从当前区间的末尾向前开始安排，并将这个新增的开机时间段记录到open_list当中

遍历完成后，计算open_list中所有开机时间段的长度，累加和就是最终答案。

对于上面的算法，有两个问题：

1、如果确定当前区间中有哪些时间已经开机了

2、对于当前区间剩余的需要开机的时间，如果从后往前安排的话，如何与已有开机时间进行区间合并

---

对于第一个问题，由于原始的区间已经按照终点排好序了，而每次新开机的时间段都是从当前的原始区间从后往前安排的，那么就意味着开机时间段数组中记录的时间段是单调递增的。这样一来，就可以在数组中二分当前区间的起点，从而找到当前区间中包含了哪些开机时间段。而对于开机时间的计算，则可以使用数组s维护open_list中所有时间段的前缀和，从而在O(1)的时间内计算出当前区间中已经开机的时间。

举个例子说明：

当前的open_list为

\[\[L0, R0\], \[L1, R1\], ..., \[Lm, Rm\]\]

那么s数组就是

[(R0 - L0 + 1), (R0 - L0 + 1) + (R1 - L1 + 1), ..., (R0 - L0 + 1) + ... + (Rm - Lm + 1)]

接下来对于当前区间[x, y]，若x小于等于Rm，说明[x, y]中已经有部分时间开机了，此时则需要在open_list中二分x，找到下标最小的大于等于x的R，记为Rk。

对于open_list中的\[L\[k + 1\], R\[k + 1\]\]到\[Lm, Rm\]，必然都处于\[x, y\]中，这部分时间段的时长之和就是s\[-1\] - s\[k\]。

另外，对于[Lk, Rk]自身，若x \<\= Lk，那么[Lk, Rk]也处于[x, y]中，反过来，若x > Lk，那么只有[x, Rk]处于[x, y]中。将这部分时长之和与之前的s[-1] - s[k]加起来，就是当前已经开机的时间。

---

接下来考虑第二个问题。计算得到当前区间中已开机的时间后，则可以计算出还需要开机的时间。按照上面所说的算法，此时应该从当前区间的尾部开始向前开始安排开机。不过这里的问题是可能出现区间合并的情况。

同样是举例说明。

例如当前已有的开机时间为[5, 6]，当前的区间为[1, 7]，需要的开机时间为6。在减去已有的开机时间2之后，还需要4的开机时间。理想情况下，应该是安排时间段[2, 7]开机，但是现在[5, 6]已经开机了，那么本轮的开机时间点应该是两个区间[2, 4]和[7, 7]。

如果老老实实做区间拆分再合并的话，整体的复杂性就太高了。在这里不妨转换一下思路，即出现区间合并重叠时，先将原有的时间段删除，并将这个时间累加到新区间需要的开机时间中。例如上面这种情况，就先将原有的[5, 6]删去，并将这个2的开机时间重新加回到需要的开机时间中。此时的情况就变成了open_list为空，且当前区间需要6的开机时间，那么就可以直接安排[1, 7]开机了。

需要注意的是，这个处理方法需要同步处理掉s数组。由于每个开机时间段只会进出一次open_list，那么均摊下来还是O(1)的时间复杂度。

最后附上python代码：

```python
class Solution(object):
    def processTasks(self, tasks):
        """
        :type tasks: List[List[int]]
        :rtype: int
        """

        tasks.sort(key=lambda d:d[1])
        open_list = []
        s = []
        for x, y, p in tasks:
            if open_list and x <= open_list[-1][1]:
                l = 0
                r = len(open_list) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if open_list[mid][1] >= x:
                        r = mid
                    else:
                        l = mid + 1
                
                #二分找到[x, y]包含的开机时间，并计算还需要的开机时间p
                p -= s[-1] - s[l]
                if x <= open_list[l][0]:
                    p -= open_list[l][1] - open_list[l][0] + 1
                else:
                    p-= open_list[l][1] - x + 1
                
            if p > 0:
                #需要新增的开机时间区间为[y - p + 1, y]，如果出现了重合，那么就将其弹出并更新s和p
                while open_list and open_list[-1][1] >= y - p + 1:
                    s.pop()
                    p += open_list[-1][1] - open_list[-1][0] + 1
                    open_list.pop()                    
                #将新的开机区间加入到open_list并更新s
                open_list.append([y - p + 1, y])
                if not s:
                    s.append(p)
                else:
                    s.append(s[-1] + p)

        return s[-1]
```
