---
title: "2528. 最大化城市的最小供电站数量"
aliases: ["yiduobo的每日leetcode 2528.最大化城市的最小供电站数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "leetcode/prefix-sum", "leetcode/sliding-window", "题单/二分算法", "题单/常用数据结构", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/常用数据结构/二-差分", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636629022"
zhihu_id: "636629022"
zhihu_title: "yiduobo的每日leetcode 2528.最大化城市的最小供电站数量"
question_id: "2528"
question: "最大化城市的最小电量"
problem_url: "https://leetcode.cn/problems/maximize-the-minimum-powered-city/"
difficulty: "Hard"
rating: 2236
created: "2023-06-13T02:20:31+08:00"
updated: "2023-06-13T02:20:31+08:00"
upvotes: 0
comments: 0
---

# 2528. 最大化城市的最小供电站数量

> **[yiduobo的每日leetcode 2528.最大化城市的最小供电站数量](https://zhuanlan.zhihu.com/p/636629022) · 知乎 · 2023-06-13 · 赞同 0**
> 力扣：[2528. 最大化城市的最小电量](https://leetcode.cn/problems/maximize-the-minimum-powered-city/) · Hard · 灵茶山艾府：[二分答案+前缀和+差分数组+贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2528.最大化城市的最小供电站数量

[力扣](https://leetcode.cn/problems/maximize-the-minimum-powered-city/)

超级缝合怪的一题，综合了leetcode中最经常出现的滑动窗口、二分、贪心以及差分数组。如果再加上组合数学将会绝杀，可惜加不得。

首先可以明确的一点是如果想要最小供电站数量越大，那么所需的额外电站就越多，符合二分的性质，因此在这里可以二分最后的答案mid，将问题转化成能否得到一种分配电站的方案，使得每个城市供电站的数目都大于等于mid，且需要新增的电站不超过k。

注意到每个电站都可以为一个区间供电，因此在枚举每个城市时需要使用滑动窗口来计算原始状况下有多少个电站可以为当前城市供电。

一趟遍历，枚举每座城市i，同时使用一个变量j记录能为i供电的最右侧城市下标。随着i的向后移动，j也应该跟着向后移动，同时更新可以为城市i供电的电站数目now。

得到now之后，若其小于mid，就需要额外增加电站为当前城市供电。

对于新增的电站，其放置的位置应该尽量靠后，理由是前方的城市已经有足够电站供电了，将新增的电站往后放可以减轻后续的电站数量需求。由于电站供电的范围为r，那么对于当前位置i而言，就应该将新增的电站放置在i + r这个位置上，这些电站将可以为i到i + r + r范围内的城市供电。

可以发现，这些新增的电站会影响到后续城市电站数量的计算，那么为了方便计算这些新增电站的数目，则可以使用类似差分数组的技巧。使用一个变量used统计当前新增的电站，同时使用一个数组f记录在当前城市失效的电站数目。对于城市i所需的delta个电站，将会在城市i + r新增delta个电站，这些电站将在城市i + r + r + 1失效，因此对于这种情况，应该将used加上delta，然后将f[i + r + r + 1]也加上delta。当来到城市i + r + r + 1时，通过减去f[i + r + r + 1]来去除掉这delta个电站的影响。

在具体实现上，由于used还兼具着检测当前所需电站delta与已新增的电站used之和是否不超过k的这一任务，因此可以将f作用到now而不是used上。

最后，在当前电站从i移动到i + 1时，还需要将可以为i供电但是不能为i + 1供电的原始电站，也就是位于城市i - r的原始电站从now中移除。

综合上面描述的算法，就得到一个大致的算法流程：

1、二分最后答案mid，对于当前的mid，初始化原始有效电站数目now、原始有效电站右边界j、新增电站数目used以及差分数组f为0

2、遍历所有城市。对于当前城市i：

2-1）先将j向右移动到i + r，将过程中所有的stations[j]累加到now中

2-2）将now减去f[i]，表示之前添加在i - r - 1这个位置的电站失效了

2-3）若当前的now加上used依然不足mid，那么就需要新增delta \= mid - now - used个电站。若delta与used之和大于k，说明电站数目不足，此时应该退出循环；反之若delta与used之和小于等于k，那么就在i + r这座城市新增delta座电站，这些电站可以为区间[i, i + r + r]的城市供电，此时应该将used加上delta，然后将f[i + r + r +1]也加上delta，表示这些电站将在i + r + r + 1失效。

2-4）最后，考察的城市将会从i来到i + 1，而位于i - r这座城市的原始电站不能为i + 1供电，此时应该将now减去stations[i - r]

3、如果最终是正常退出2中的循环，说明电站的数目足够，此时应该调整二分下界为mid；如果是从2-3中途退出了循环，说明电站数目不足，此时应该调整二分上界为mid - 1。无论是哪种情况，都应该回到步骤1继续二分，直到二分上下界相遇为止

最后附上python代码：

```python
class Solution(object):
    def maxPower(self, stations, r, k):
        """
        :type stations: List[int]
        :type r: int
        :type k: int
        :rtype: int
        """

        left = min(stations)
        right = sum(stations) + k
        n = len(stations)
        while left < right:
            mid = (left + right + 1) >> 1
            f = [0] * n
            used = 0
            now = 0
            j = 0
            flag = True

            for i in range(n):
                if j < i:
                    j = i
                while j < n and j - i <= r:
                    now += stations[j]
                    j += 1
                
                now -= f[i]

                if now + used < mid:
                    delta = mid - now - used
                    if delta + used <= k:
                        used += delta
                        if i + r + r + 1 < n:
                            f[i + r + r + 1] += delta
                    else:
                        flag = False
                        break
            
                if i - r >= 0:
                    now -= stations[i - r]

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left
```
