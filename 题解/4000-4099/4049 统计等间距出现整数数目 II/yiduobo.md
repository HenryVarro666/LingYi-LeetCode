---
title: "4048. 统计等间距出现整数数目I & 4049. 统计等间距出现整数数目II"
aliases: ["yiduobo的每日leetcode 4048.统计等间距出现整数数目I && 4049.统计等间距出现整数数目II", "4048. 统计等间距出现整数数目I", "4049. 统计等间距出现整数数目II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2083024505606348834"
zhihu_id: "2083024505606348834"
zhihu_title: "yiduobo的每日leetcode 4048.统计等间距出现整数数目I && 4049.统计等间距出现整数数目II"
question_id: ["4048", "4049"]
question: ["统计等间距出现整数数目 I", "统计等间距出现整数数目 II"]
problem_url: ["https://leetcode.cn/problems/count-values-with-equally-spaced-occurrences-i/", "https://leetcode.cn/problems/count-values-with-equally-spaced-occurrences-ii/"]
difficulty: ["Easy", "Medium"]
created: "2026-09-15T03:06:17+08:00"
updated: "2026-09-15T03:06:22+08:00"
upvotes: 1
comments: 0
---

# 4048. 统计等间距出现整数数目I & 4049. 统计等间距出现整数数目II

> **[yiduobo的每日leetcode 4048.统计等间距出现整数数目I && 4049.统计等间距出现整数数目II](https://zhuanlan.zhihu.com/p/2083024505606348834) · 知乎 · 2026-09-15 · 赞同 1**
> 力扣：[4048. 统计等间距出现整数数目 I](https://leetcode.cn/problems/count-values-with-equally-spaced-occurrences-i/) · Easy · 灵茶山艾府：[记录每个元素的所有出现位置（Python/Java/C++/Go）](../4048%20统计等间距出现整数数目%20I/灵茶山艾府.md)
> 力扣：[4049. 统计等间距出现整数数目 II](https://leetcode.cn/problems/count-values-with-equally-spaced-occurrences-ii/) · Medium · 灵茶山艾府：[记录每个元素的所有出现位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4048.统计等间距出现整数数组I

<https://leetcode.cn/problems/count-values-with-equally-spaced-occurrences-i/description/>

4049.统计等间距出现整数数组II

<https://leetcode.cn/problems/count-values-with-equally-spaced-occurrences-ii/description/>

题目给出一个整数数组nums。

若一个整数x在nums中的所有出现都是等间隔的，且其出现次数满足一定的条件，那么就称x是特别的。

在4048题中，这个条件是x恰好出现三次。

在4049题中，这个条件是x至少出现三次。

问nums中不同的特别整数的数量。

对于一个元素x，其出现次数是很好统计的。而对于等间隔出现这个条件，则需要记录每个元素上一次出现的位置，以及已经约定好的下标差才方便判断。除此之外，还需要标记每种元素的下标差是否合法。

综合起来，就需要四个哈希表来记录上面这些东西，具体来说：

- pre[x]表示x上次出现的下标
- diff[x]表示约定好的x出现位置的下标差
- cnt[x]表示x出现的次数
- flag[x]表示x的下标差是否合法

接下来就只需要一趟遍历，对于当前遍历到的x，若其是首次出现，那么就：

- 将pre[x]置为当前下标index
- 将diff[x]置为None，因为目前仅有一个x，还不存在下标差
- 将cnt[x]置为1
- 将flag[x]置为True

否则：

- 若diff[x]非None，且index - pre[x]不等于diff[x]，说明下标差不一致，此时应该将flag[x]置为False
- 将diff[x]置为index - pre[x]
- 将pre[x]置为index
- 将cnt[x]加上1

对于4048题，x合法的条件是flag[x]为true且cnt[x]等于3，而对于4049题，x合法的条件则是flag[x]为true且cnt[x]大于等于3。因此在遍历完成后，只需要再次遍历所有出现过的x，然后检测其是否合法并更新答案即可。

最后附上python代码，两题仅有最后cnt[v]处的判断略有区别：

4048:

```python
class Solution(object):
    def countSpecialIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        pre = {}
        diff = {}
        cnt = {}
        flag = {}

        for index, v in enumerate(nums):
            if v not in pre:
                pre[v] = index
                diff[v] = None
                cnt[v] = 1
                flag[v] = True
            
            else:
                if diff[v] is not None and diff[v] != index - pre[v]:
                    flag[v] = False
                diff[v] = index - pre[v]
                pre[v] = index
                cnt[v] += 1
        
        res = 0
        for v in flag:
            if cnt[v] == 3 and flag[v]:
                res += 1
        
        return res
```

4049:

```python
class Solution(object):
    def countSpecialIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        pre = {}
        diff = {}
        cnt = {}
        flag = {}

        for index, v in enumerate(nums):
            if v not in pre:
                pre[v] = index
                diff[v] = None
                cnt[v] = 1
                flag[v] = True
            
            else:
                if diff[v] is not None and diff[v] != index - pre[v]:
                    flag[v] = False
                diff[v] = index - pre[v]
                pre[v] = index
                cnt[v] += 1
        
        res = 0
        for v in flag:
            if cnt[v] >= 3 and flag[v]:
                res += 1
        
        return res
```
