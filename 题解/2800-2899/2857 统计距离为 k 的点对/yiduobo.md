---
title: "2857. 统计距离为k的点对"
aliases: ["yiduobo的每日leetcode 2857.统计距离为k的点对"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/bian-li", "leetcode/bao-li", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661233836"
zhihu_id: "661233836"
zhihu_title: "yiduobo的每日leetcode 2857.统计距离为k的点对"
question_id: "2857"
question: "统计距离为 k 的点对"
problem_url: "https://leetcode.cn/problems/count-pairs-of-points-with-distance-k/"
difficulty: "Medium"
rating: 2082
created: "2023-10-14T03:47:30+08:00"
updated: "2023-10-14T03:47:30+08:00"
upvotes: 0
comments: 0
---

# 2857. 统计距离为k的点对

> **[yiduobo的每日leetcode 2857.统计距离为k的点对](https://zhuanlan.zhihu.com/p/661233836) · 知乎 · 2023-10-14 · 赞同 0**
> 力扣：[2857. 统计距离为 k 的点对](https://leetcode.cn/problems/count-pairs-of-points-with-distance-k/) · Medium · 灵茶山艾府：[暴力：注意 k 的范围（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2857.统计距离为k的点对

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-pairs-of-points-with-distance-k/)

题目中点的数量很多，因此暴力法肯定是不行的。

注意到本题中k的规模比较小，而异或的结果必然是非负的，因此在这里就可以从0到k枚举x坐标的异或结果p，通过k - p得到y坐标的异或结果q，然后计算有多少点对两个坐标的异或结果分别为p和q。

具体检测的方法则可以利用哈希表，一趟遍历，使用哈希表记录已经遍历过的节点出现过的次数。接下来对于当前遍历到的(x, y)，其与(p^x, q^y)将形成距离为k的点对，因此只需检测(p^x, q^y)在哈希表中出现的次数，然后再将(x, y)加入到哈希表中并继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, coordinates, k):
        """
        :type coordinates: List[List[int]]
        :type k: int
        :rtype: int
        """

        res = 0
        for p in range(k + 1):
            q = k - p
            cnt = {}
            for x, y in coordinates:
                res += cnt.get((p ^ x, q ^ y), 0)
                cnt[(x, y)] = cnt.get((x, y), 0) + 1
        
        return res
```
