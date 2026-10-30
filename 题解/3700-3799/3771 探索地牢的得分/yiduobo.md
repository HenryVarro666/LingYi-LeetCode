---
title: "3771. 探索地牢的得分"
aliases: ["yiduobo的每日leetcode 3771.探索地牢的得分"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/prefix-sum", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1981138090744649269"
zhihu_id: "1981138090744649269"
zhihu_title: "yiduobo的每日leetcode 3771.探索地牢的得分"
question_id: "3771"
question: "探索地牢的得分"
problem_url: "https://leetcode.cn/problems/total-score-of-dungeon-runs/"
difficulty: "Medium"
rating: 1981
created: "2025-12-10T21:06:56+08:00"
updated: "2025-12-10T21:06:59+08:00"
upvotes: 1
comments: 0
---

# 3771. 探索地牢的得分

> **[yiduobo的每日leetcode 3771.探索地牢的得分](https://zhuanlan.zhihu.com/p/1981138090744649269) · 知乎 · 2025-12-10 · 赞同 1**
> 力扣：[3771. 探索地牢的得分](https://leetcode.cn/problems/total-score-of-dungeon-runs/) · Medium · 灵茶山艾府：[贡献法：前缀和 + 二分查找（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3771.探索地牢的得分

<https://leetcode.cn/problems/total-score-of-dungeon-runs/description/>

题目给出一个正整数hp以及两个正整数数组damge和requirement。

有一个地牢，里面有n个陷阱房间，进入房间index会使得生命值减少damage[index]。减少后，若剩余生命值至少为requirement[index]，那么就可以得到1分。

另外定义score[index]为从房间index开始，依次进入index、index + 1、...、n这些房间时可以获得的总分。在这个过程中，不能跳过房间，但是即使生命值降到非正数，依然可以继续进入房间。

要求计算所有score之和。

对于score[index]，由于damage是正整数数组，因此随着向后移动，hp必然是逐渐减少的。但是这里的requirement并不是单调的，因此直接计算每个score[index]是比较麻烦的，不妨换一个思路，改成计算对于index，有多少个起点可以在index这个房间得到分数。

这样做的好处是可以直接消除掉requirement的影响，就相当于对于每个index，需要找出一个最小的p，满足damage[p + 1] + ... + damage[index] \<\= hp - requirement[index]，那么以房间p + 1到房间index为起点对应的score都可以在index这个房间拿到分数，一共可以得到index - p分。当然，若requirement[index]一开始就大于hp，那么就不可能在index这里拿到分数。

对于damage[p + 1] + ... + damage[index] \<\= hp - requirement[index]这个式子，前半部分是个典型的区间和形式，可以写成前缀和，即s[index] - s[p]。另一方面，由于damage是正整数数组，因此随着p的增大或减小，s[p]也会跟着增大或减小，因此在这里可以通过二分来确定这个p。

基于上面的结论，就可以先对damage进行一趟遍历，计算出前缀和数组s。

接下来再对requirement进行一趟遍历，若当前的requirement[index]大于hp，那么不可能得到分数，可以跳过这个房间。

否则可以先计算出h \= hp - requirement[index]，若h大于等于s[index]，那么就说明index之前所有的起点都可以在index这里拿到分数，一共是index + 1个房间，因此需要将index + 1累加到答案之中。反之，则需要在0到index之间二分，找到最小的p，然后将index - p累加到答案之中。

最后附上python代码：

```python
class Solution(object):
    def totalScore(self, hp, damage, requirement):
        """
        :type hp: int
        :type damage: List[int]
        :type requirement: List[int]
        :rtype: int
        """
        
        s = [damage[0]]
        for d in damage[1:]:
            s.append(s[-1] + d)
        
        res = 0
        for index, r in enumerate(requirement):
            if r > hp:
                continue
            
            h = hp - r
            if s[index] <= h:
                res += index + 1
            else:
                left = 0
                right = index
                while left < right:
                    mid = (left + right) // 2
                    if s[index] - s[mid] > h:
                        left = mid + 1
                    else:
                        right = mid

                res += index - left
        
        return res
```
