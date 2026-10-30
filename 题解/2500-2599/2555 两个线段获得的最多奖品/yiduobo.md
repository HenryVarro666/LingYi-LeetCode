---
title: "2555. 两个线段获得的最多奖品"
aliases: ["yiduobo的每日leetcode 2555.两个线段获得的最多奖品"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/638958466"
zhihu_id: "638958466"
zhihu_title: "yiduobo的每日leetcode 2555.两个线段获得的最多奖品"
question_id: "2555"
question: "两个线段获得的最多奖品"
problem_url: "https://leetcode.cn/problems/maximize-win-from-two-segments/"
difficulty: "Medium"
rating: 2081
created: "2023-06-26T18:47:39+08:00"
updated: "2023-06-26T18:47:39+08:00"
upvotes: 0
comments: 0
---

# 2555. 两个线段获得的最多奖品

> **[yiduobo的每日leetcode 2555.两个线段获得的最多奖品](https://zhuanlan.zhihu.com/p/638958466) · 知乎 · 2023-06-26 · 赞同 0**
> 力扣：[2555. 两个线段获得的最多奖品](https://leetcode.cn/problems/maximize-win-from-two-segments/) · Medium · 灵茶山艾府：[两种不同的思考角度（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2555.两个线段获得的最多奖品

[力扣](https://leetcode.cn/problems/maximize-win-from-two-segments/)

为了使得获得的奖品最多，本题中的两条线段是不应该相交的，而对于单条线段可包含的奖品数，则可以利用变长滑动窗口来进行求解。

对于一个以prizePositions[right]为右边界的窗口，设其包含的最左侧的奖品的下标为left，那么在这里只需要知道所有右边界在prizePositions[0]到prizePositions[left - 1]的窗口中，最多包含了多少奖品，就可以使用当前窗口中奖品的个数right - left + 1加上这个最多的奖品数来更新答案了。

对于这个最多的奖品数，则可以使用动态规划来求解。令f[i]表示所有右边界在prizePositions[0]到prizePositions[i]之间窗口中，包含最多的奖品个数，那么对于每个遍历到的right，就有f[right] \= max(f[right - 1]，right - left + 1)。

最后附上python代码：

```python
class Solution(object):
    def maximizeWin(self, prizePositions, k):
        """
        :type prizePositions: List[int]
        :type k: int
        :rtype: int
        """

        n = len(prizePositions)
        f = [0] * n

        left = right = 0
        res = 0
        while right < n:
            while prizePositions[right] - prizePositions[left] > k:
                left += 1
            
            now = right - left + 1
            if left > 0:
                now += f[left - 1]
            
            res = max(res, now)
            f[right] = right - left + 1
            if right > 0 and f[right] < f[right - 1]:
                f[right] = f[right - 1]
            right += 1
        
        return res
```
