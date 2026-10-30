---
title: "3355. 零数组变换I"
aliases: ["yiduobo的每日leetcode 3355.零数组变换I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/26921398165"
zhihu_id: "26921398165"
zhihu_title: "yiduobo的每日leetcode 3355.零数组变换I"
question_id: "3355"
question: "零数组变换 I"
problem_url: "https://leetcode.cn/problems/zero-array-transformation-i/"
difficulty: "Medium"
rating: 1591
created: "2025-02-28T00:54:17+08:00"
updated: "2025-02-28T00:54:17+08:00"
upvotes: 0
comments: 0
---

# 3355. 零数组变换I

> **[yiduobo的每日leetcode 3355.零数组变换I](https://zhuanlan.zhihu.com/p/26921398165) · 知乎 · 2025-02-28 · 赞同 0**
> 力扣：[3355. 零数组变换 I](https://leetcode.cn/problems/zero-array-transformation-i/) · Medium · 灵茶山艾府：[【模板】差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3355.零数组变换I

[3355. 零数组变换 I - 力扣（LeetCode）](https://leetcode.cn/problems/zero-array-transformation-i/description/)

题目给出一个长度为n的整数数组nums以及一个二维数组queries，其中queries\[i\] \= \[l\[i\], r\[i\]\]。对于每个查询queries\[i\]，可以在下标范围\[l\[i\], r\[i\]\]中选择一个下标子集，将这些下标对应的元素减去1。

问在按顺序处理完所有查询后，能否将nums变为全0。

为了使得nums变为全0，也就意味着对于其中每个位置index需要执行nums[index]次操作，也就是说index至少需要被queries中的nums[index]个区间覆盖住。

对于这类静态区间问题，一种场景的处理方法是差分数组。具体来说，对于区间\[l\[i\], r\[i\]\]，可以将其拆分为以l\[i\]为起点的后缀增加一次覆盖，然后以r\[i\] + 1为起点的后缀减少一次覆盖。

令f\[index\]表示以index为起点的后缀的覆盖次数，那么对于区间\[l\[i\], r\[i\]\]，只需将f\[l\[i\]\]加上1，然后将f\[r\[i\] + 1\]减去1即可。

遍历完queries更新得到f之后，再对f进行一次遍历，计算其每个下标对应的前缀和即为覆盖对应下标的次数。若对于某个位置index，其前缀和now小于nums[index]，说明操作的次数不够，此时应该返回false。若不存在这样的下标，则返回true。

最后附上python代码：

```python
class Solution(object):
    def isZeroArray(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: bool
        """
        
        n = len(nums)
        f = [0] * n
        for x, y in queries:
            f[x] += 1
            if y + 1 < n:
                f[y + 1] -= 1
        
        now = 0
        for index in range(n):
            now += f[index]
            if now < nums[index]:
                return False
        return True
```
