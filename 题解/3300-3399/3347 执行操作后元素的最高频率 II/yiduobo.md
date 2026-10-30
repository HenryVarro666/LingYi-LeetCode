---
title: "3346. 执行操作后元素的最高频率I & 3347. 执行操作后元素的最高频率II"
aliases: ["yiduobo的每日leetcode 3346.执行操作后元素的最高频率I && 3347.执行操作后元素的最高频率II", "3346. 执行操作后元素的最高频率I", "3347. 执行操作后元素的最高频率II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/two-pointers", "leetcode/ordered-set", "leetcode/prefix-sum", "leetcode/sliding-window", "leetcode/hard", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/滑动窗口与双指针/五-三指针", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25845862356"
zhihu_id: "25845862356"
zhihu_title: "yiduobo的每日leetcode 3346.执行操作后元素的最高频率I && 3347.执行操作后元素的最高频率II"
question_id: ["3346", "3347"]
question: ["执行操作后元素的最高频率 I", "执行操作后元素的最高频率 II"]
problem_url: ["https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-i/", "https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2156
created: "2025-02-23T23:14:27+08:00"
updated: "2025-02-23T23:14:27+08:00"
upvotes: 3
comments: 0
---

# 3346. 执行操作后元素的最高频率I & 3347. 执行操作后元素的最高频率II

> **[yiduobo的每日leetcode 3346.执行操作后元素的最高频率I && 3347.执行操作后元素的最高频率II](https://zhuanlan.zhihu.com/p/25845862356) · 知乎 · 2025-02-23 · 赞同 3**
> 力扣：[3346. 执行操作后元素的最高频率 I](https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-i/) · Medium · 灵茶山艾府：[两种方法：差分/滑动窗口（Python/Java/C++/Go）](../3346%20执行操作后元素的最高频率%20I/灵茶山艾府.md)
> 力扣：[3347. 执行操作后元素的最高频率 II](https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-ii/) · Hard · 灵茶山艾府：[两种方法：差分/三指针+双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3346.执行操作后元素的最高频率I

[3346. 执行操作后元素的最高频率 I - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-i/description/)

3347.执行操作后元素的最高频率II

[3347. 执行操作后元素的最高频率 II - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-frequency-of-an-element-after-performing-operations-ii/description/)

题目给出一个整数数组nums和两个整数k和numOperations。现在要求对nums执行numOperations次操作，每次操作中可以选择一个之前没有选过的下标i，将nums[i]增加范围[-k, k]中的一个整数。问在执行完所有操作之后，nums中元素的最大可能出现次数可能是多少。

两题的题设一样，第二题的数据规模较大，数组长度可以来到10^5，而nums中的元素以及k的大小可以来到10^9。

题目中的操作可以将nums[i]变为nums[i] - k到nums[i] + k中的任意整数，那么如果将原始的nums[i]视为一个起点和终点都为nums[i]的区间，那么一次操作就是将这个区间扩展成起点为nums[i] - k，终点为nums[i] + k的区间，而题目要计算的最大可能出现次数，在区间重叠的视角上就可以认为是要如果分配这些操作，使得尽量多的区间能相交在同一个下标。

对于区间重叠类的问题，一个经典的结论就是最多区间相交的下标一定处于某个区间的起点或者终点。对于本题，如果对nums[i]不执行操作，那么nums[i]自身可能就是最多区间相交的位置；而如果对nums[i]执行操作，那么nums[i] - k或者nums[i] + k就可能是最多区间相交的位置，换言之，最多只有n \* 3种可能的下标位置，这里的n是数组的长度。

更进一步的，一个自然的想法就是依次遍历这n \* 3个位置，检测有多少个区间可以覆盖到当前位置。直观上来说向计算这个覆盖数是比较困难的，不过注意到本题中的操作扩展长度都是-k到k，因此对于两个下标位置p和q，若以p为中心扩展后的区间如果可以覆盖q，那么以q为中心扩展后的区间也一定可以覆盖p，于是在这里可以反过来思考，将检测有多少个区间可以覆盖到当前位置，改成以当前位置为中心，向两侧扩展k得到的区间可以覆盖多少个nums中的元素。将这些位置从小到大排序后，这就是一个标准的滑动窗口问题。

需要特别注意的是，对于以v为中心的窗口[v - k, v + k]，不妨设其覆盖住了nums中的m个元素，在这m个元素，本身就等于v的元素是不需要执行操作的。令cnt[v]表示nums中值等于v的元素的数量，那么这m个元素中有cnt[v]个元素是不需要执行操作的，而剩下的m - cnt[v]个元素都需要执行操作才能覆盖住v。因为操作数有上限numOperations，因此最终可以覆盖住v的区间数量实际上为min(numOperations, m - cnt[v]) + cnt[v]，对于每个中心点v，计算出对应的m，然后使用上面这个式子的结果更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maxFrequency(self, nums, k, numOperations):
        """
        :type nums: List[int]
        :type k: int
        :type numOperations: int
        :rtype: int
        """
        
        cnt = {}
        num_set = set()
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            num_set.add(v)
            num_set.add(v - k)
            num_set.add(v + k)
        
        nums.sort()
        left = 0
        right = 0
        res = 0
        for v in sorted(list(num_set)):
            while right < len(nums) and nums[right] - k <= v:
                right += 1
            while nums[left] + k < v:
                left += 1
            
            res = max(res, min(numOperations, right - left - cnt.get(v, 0)) + cnt.get(v, 0))
        return res
```
