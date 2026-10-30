---
title: "2848. 与车相交的点"
aliases: ["yiduobo的每日leetcode 2848.与车相交的点"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/prefix-sum", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/二-差分", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660403644"
zhihu_id: "660403644"
zhihu_title: "yiduobo的每日leetcode 2848.与车相交的点"
question_id: "2848"
question: "与车相交的点"
problem_url: "https://leetcode.cn/problems/points-that-intersect-with-cars/"
difficulty: "Easy"
rating: 1230
created: "2023-10-10T03:23:19+08:00"
updated: "2023-10-10T03:23:19+08:00"
upvotes: 0
comments: 0
---

# 2848. 与车相交的点

> **[yiduobo的每日leetcode 2848.与车相交的点](https://zhuanlan.zhihu.com/p/660403644) · 知乎 · 2023-10-10 · 赞同 0**
> 力扣：[2848. 与车相交的点](https://leetcode.cn/problems/points-that-intersect-with-cars/) · Easy · 灵茶山艾府：[差分数组（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2848.与车相交的点

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/points-that-intersect-with-cars/)

经典的区间合并问题。将所有区间按起点从小到大排序，使用变量nowx, nowy记录之前遍历过的最后这个区间的起点和终点，初始值可以设定为最左侧区间的左右边界。接下来从下标1的区间开始向后遍历，对于当前遍历到的区间[x, y]：

1、若x \<\= nowy，说明这两个区间是重叠的，此时就需要将二者合并。由于nowx必然小于等于x，因此新区间的左边界依然是nowx不变，而右边界则为nowy和y这两者中的较大值

2、若x > nowy，说明这两个区间不重叠，同时由于区间是按照起点排序的，因此后续的区间左边界必然也大于nowy，也就是说[nowx, nowy]不会与后续任何区间相交，此时应该将[nowx, nowy]的长度，也就是nowy - nowx + 1累加到答案中，然后将nowx、nowy分别置为x和y，也就是新的最后这个区间

遍历完成后，不要忘了当前[nowx, nowy]的长度累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def numberOfPoints(self, nums):
        """
        :type nums: List[List[int]]
        :rtype: int
        """

        nums.sort()
        nowx, nowy = nums[0]
        res = 0
        for x, y in nums[1:]:
            if x <= nowy:
                nowy = max(nowy, y)
            else:
                res += nowy - nowx + 1
                nowx, nowy = x, y
        
        return res + nowy - nowx + 1
```
