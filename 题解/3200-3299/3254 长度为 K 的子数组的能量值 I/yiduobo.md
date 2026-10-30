---
title: "3254. 长度为K的子数组的能量值I & 3255. 长度为K的子数组的能量值II"
aliases: ["yiduobo的每日leetcode 3254.长度为K的子数组的能量值I && 3255.长度为K的子数组的能量值II", "3254. 长度为K的子数组的能量值I", "3255. 长度为K的子数组的能量值II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/721941575"
zhihu_id: "721941575"
zhihu_title: "yiduobo的每日leetcode 3254.长度为K的子数组的能量值I && 3255.长度为K的子数组的能量值II"
question_id: ["3254", "3255"]
question: ["长度为 K 的子数组的能量值 I", "长度为 K 的子数组的能量值 II"]
problem_url: ["https://leetcode.cn/problems/find-the-power-of-k-size-subarrays-i/", "https://leetcode.cn/problems/find-the-power-of-k-size-subarrays-ii/"]
difficulty: "Medium"
rating: 1595
created: "2024-09-25T03:26:01+08:00"
updated: "2024-09-25T03:28:49+08:00"
upvotes: 1
comments: 0
---

# 3254. 长度为K的子数组的能量值I & 3255. 长度为K的子数组的能量值II

> **[yiduobo的每日leetcode 3254.长度为K的子数组的能量值I && 3255.长度为K的子数组的能量值II](https://zhuanlan.zhihu.com/p/721941575) · 知乎 · 2024-09-25 · 赞同 1**
> 力扣：[3254. 长度为 K 的子数组的能量值 I](https://leetcode.cn/problems/find-the-power-of-k-size-subarrays-i/) · Medium · 灵茶山艾府：[O(n) 简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)
> 力扣：[3255. 长度为 K 的子数组的能量值 II](https://leetcode.cn/problems/find-the-power-of-k-size-subarrays-ii/) · Medium · 灵茶山艾府：[O(n) 简洁写法（Python/Java/C++/C/Go/JS/Rust）](../3255%20长度为%20K%20的子数组的能量值%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3254.长度为K的子数组的能量值I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-power-of-k-size-subarrays-i/description/)

3255.长度为K的子数组的能量值II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-power-of-k-size-subarrays-ii/description/)

题目给出一个长度为n的整数数组nums以及一个正整数k，若nums中的某个子数组满足其中所有元素都是依次连续且上升的，那么这个子数组的能量值就是其中最大的元素，否则其能量值为-1。现在要求找出数组中所有长度为k的子数组的能量值。

两题的题设相同，第二题的数据规模较大。

首先可以明确的是，一个大小为k的子数组如果是依次连续且上升的，那么其中最大的元素一定是这个子数组的最后一个元素，那么就只需想办法判断nums中，以每个元素nums[index]为结尾的连续且上升的子数组的最大长度length[index]是否大于等于k。若大于等于，那么nums[index]就是以该元素结尾的大小为k的子数组的能量值，否则这个子数组的能量值就是-1。

对于length的计算则可以使用动态规划，若当前元素nums[index]是首个元素，或者nums[index] !\= nums[index - 1]，那么length[index]就是1，这里的1表示nums[index]自身，否则的话就相当于在以nums[index - 1]为结尾的子数组的基础上再添加nums[index]，即length[index] \= length[index - 1] + 1。

根据上面的结论，就只需要一趟遍历，根据当前的nums[index]与nums[index - 1]的关系计算对应的length，并通过length与k的大关系来更新答案。需要注意由于题目要计算的是长度为k的子数组，而只有当index + 1 >\= k时才能形成长度为k的子数组，因此在这之前都不应该更新答案。

另外注意到length是即算即用，且只与上一轮的状态有关，因此在这里可以使用变量迭代而不需要使用数组。

最后附上python代码：

```python
class Solution(object):
    def resultsArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        res = []
        length = 0

        for index in range(len(nums)):
            if index == 0 or nums[index] != nums[index - 1] + 1:
                length = 1
            else:
                length += 1
            
            if index + 1 >= k:
                if length >= k:
                    res.append(nums[index])
                else:
                    res.append(-1)
        
        return res
```
