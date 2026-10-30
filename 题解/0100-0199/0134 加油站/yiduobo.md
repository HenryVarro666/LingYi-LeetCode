---
title: "134. 加油站"
aliases: ["yiduobo的每日leetcode 134.加油站"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/graph", "题单/贪心算法", "题单/面试经典-150-题", "题单/贪心算法/八-其他", "题单/面试经典-150-题/数组-/-字符串"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/141472126"
zhihu_id: "141472126"
zhihu_title: "yiduobo的每日leetcode 134.加油站"
question_id: "134"
question: "加油站"
problem_url: "https://leetcode.cn/problems/gas-station/"
difficulty: "Medium"
created: "2020-05-16T23:09:20+08:00"
updated: "2020-05-16T23:09:20+08:00"
upvotes: 1
comments: 1
---

# 134. 加油站

> **[yiduobo的每日leetcode 134.加油站](https://zhuanlan.zhihu.com/p/141472126) · 知乎 · 2020-05-16 · 赞同 1**
> 力扣：[134. 加油站](https://leetcode.cn/problems/gas-station/) · Medium · 灵茶山艾府：[用【折线图】直观理解（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

134.加油站<https://leetcode-cn.com/problems/gas-station/submissions/>

首先，我们可以将gas与cost减一减，表示经过这个加油站之后可能得到的剩余油量rest。对样例而言，rest为：

-2，-2，-2，3，3

接下来，对于处理环状问题，一个经典做法就是原样复制一遍接在后面，重新变成线性的问题。对于样例而言，复制后的rest为：

-2，-2，-2，3，3，-2，-2，-2，3，3

于是，我们接下来得目标是找到p，其满足从rest[p]开始，长度为1到len(gas)的子段和均不小于0。

先假设p从0开始，逐个往后验证。设现在验证到了index：

1、若rest[p] + rest[p+ 1] + ... + rest[index - 1] + rest[index] >\= 0，那么说明从p开始目前还是符合条件的，于是可以检测index - p + 1是否已经达到了len(gas)，如果是，说明p就是要找的答案。

2、若rest[p] + rest[p + 1] + ... + rest[index - 1] + rest[index] \< 0，那么：

rest[p] + ... + rest[index - 1] \< -rest[index]

注意到对于p到index - 1中的任意点k，有

rest[p] + ... + rest[k - 1] >\= 0

从节点k开始的子段和

rest[k] + ... + rest[index - 1] \< rest[p] + ... + rest[k - 1] + rest[k] + ... + rest[index - 1]

因此从k开始的子段和一定也跨不过index这个点，这说明从p开始到index在内的所有点都不能成为起始点，于是重新假设p \= index + 1，然后重新开始验证。

若一趟扫描后没有找到p，说明无解，此时返回-1即可。

最后附上python代码：

```python
class Solution(object):
    def canCompleteCircuit(self, gas, cost):
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """

        if not gas:
            return -1

        rest = [gas[index] - cost[index] for index in range(len(gas))]
        rest.extend(rest)

        p = 0
        sum = 0
        for index, r in enumerate(rest):
            sum += r
            if sum < 0:
                p = index + 1
                sum = 0
            elif index - p + 1 == len(gas):
                return p

        return -1
```
