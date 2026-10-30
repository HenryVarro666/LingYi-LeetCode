---
title: "3833. 统计主导元素下标数"
aliases: ["yiduobo的每日leetcode 3833.统计主导元素下标数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2003932626428383270"
zhihu_id: "2003932626428383270"
zhihu_title: "yiduobo的每日leetcode 3833.统计主导元素下标数"
question_id: "3833"
question: "统计主导元素下标数"
problem_url: "https://leetcode.cn/problems/count-dominant-indices/"
difficulty: "Easy"
created: "2026-02-08T20:51:17+08:00"
updated: "2026-02-08T20:51:18+08:00"
upvotes: 0
comments: 0
---

# 3833. 统计主导元素下标数

> **[yiduobo的每日leetcode 3833.统计主导元素下标数](https://zhuanlan.zhihu.com/p/2003932626428383270) · 知乎 · 2026-02-08 · 赞同 0**
> 力扣：[3833. 统计主导元素下标数](https://leetcode.cn/problems/count-dominant-indices/) · Easy · 灵茶山艾府：[O(n) 一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3833.统计主导元素下标数

<https://leetcode.cn/problems/count-dominant-indices/description/>

题目给出一个长度为n的整数数组nums。

若下标index满足nums[index] > avg(nums[index + 1], nums[index + 2], ..., nums[n - 1])，就称该元素位ie主导元素。其中avg(nums[index + 1], nums[index + 2], ..., nums[n - 1])指的是括号中元素的平均值。

问nums中有多少个主导元素。需要注意，数组最右侧的元素不算作主导元素。

题目实际上是需要对比下标0到n - 2之间每个元素与这个元素后续所有元素的平均值大小，也就是说需要计算每种后缀子数组的平均值，于是可以从倒数第二个元素开始，往前一趟遍历，使用一个变量s记录当前后缀子数组之和，另外使用一个变量cnt记录后缀子数组中元素的数目。对于当前遍历到的元素v，先对比v与后缀子数组的平均值的大小并更新答案，然后将v累加到s中并将cnt加上1即可。

最后附上python代码：

```python
class Solution(object):
    def dominantIndices(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        s = nums[-1]
        cnt = 1
        res = 0
        for v in nums[-2::-1]:
            if v * cnt > s:
                res += 1
            cnt += 1
            s += v
        
        return res
```
