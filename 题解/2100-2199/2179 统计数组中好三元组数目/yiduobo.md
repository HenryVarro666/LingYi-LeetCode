---
title: "2179. 统计数组中好三元组数目"
aliases: ["yiduobo的每日leetcode 2179.统计数组中好三元组数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/binary-indexed-tree", "leetcode/math", "leetcode/ordered-set", "题单/常用数据结构", "题单/常用数据结构/八-树状数组和线段树"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/535139606"
zhihu_id: "535139606"
zhihu_title: "yiduobo的每日leetcode 2179.统计数组中好三元组数目"
question_id: "2179"
question: "统计数组中好三元组数目"
problem_url: "https://leetcode.cn/problems/count-good-triplets-in-an-array/"
difficulty: "Hard"
rating: 2272
created: "2022-06-29T00:46:13+08:00"
updated: "2023-08-09T17:32:01+08:00"
upvotes: 0
comments: 2
---

# 2179. 统计数组中好三元组数目

> **[yiduobo的每日leetcode 2179.统计数组中好三元组数目](https://zhuanlan.zhihu.com/p/535139606) · 知乎 · 2022-06-29 · 赞同 0**
> 力扣：[2179. 统计数组中好三元组数目](https://leetcode.cn/problems/count-good-triplets-in-an-array/) · Hard · 灵茶山艾府：[转化成严格递增子序列 + 枚举中间 + 树状数组（Java/Python/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2179.统计数组中好三元组数目

[力扣](https://leetcode.cn/problems/count-good-triplets-in-an-array/)

题目的数据规模比较大，只能考虑用O(n)或者O(nlogn)的方法求解。

对于这类有前后顺序的三元组问题，通常的处理方法是枚举中间元素的位置，然后想办法高效计算左右两侧两个元素的相关性质最后得出答案。

对于本题也是一样的处理方法。从左向右遍历nums1，对于当前遍历到的nums1[index]，设其在nums2中的位置为p，那么现在需要想办法计算出两个值：

1、nums[0]到nums[index - 1]这些数当中，在nums2对应位置小于p的数的数目，记为left

2、nums[index + 1]到nums[n - 1]这些数当中，在nums2对应位置大于p的数的数目，记为right

那么最终从左侧这left个数以及右侧right个数中，分别选取一个数与nums1[index]组成，都能得到一个合法的三元组，因此以nums1[index]作为中间元素可以得到的合法三元组数目就是left \* right。只需对于num1中的所有元素都计算出对应的left和right，就能得到最终答案了。

现在的问题就变成了left和right应该如何计算。

首先是计算left。对于问题实际上就是给出一个数组，问每个元素左侧有多少个元素小于当前元素。由于这些元素都在0到n - 1之间，那么可以使用树状数组来解决。

需要注意的是，为了方便树状数组的计算，也就是下标从1开始，在这里需要将nums2中的所有位置都加上1，也就是从0到n - 1变成1到n。

---

补充说明一下，在这里使用树状数组的目的是高效求解前缀和，而判断某个元素左侧有多少个元素小于当前元素，则需要通过下标对应的01数组的前缀和来完成。

设置一个下标从1开始，仅由0和1组成的数组arr。arr的初始值都为0，接下来遍历数组，当遍历到元素k时，就将arr[k]置为1。那么在遍历过程中，对于遍历到的元素p，只需检测当前的arr[1]到arr[p - 1]之间1的数目，就表示在p左侧有多少个数大小在1到p - 1之间，也就是小于p。

而这里1的数目实际上就是arr[1]到arr[p - 1]的前缀和，对于这个动态的前缀和，就可以利用树状数组来求解了。

---

在得到left之后，则可以利用left和index直接计算出right。由于nums1[0]到nums1[index - 1]这index个数中只有left个数满足在nums2中的位置小于p，也就是说在nums2中，1到p - 1这p - 1个小于p的位置中还剩下p - left - 1个位置对应的数来自于nums1[index + 1]到nums1[n - 1]，这也就意味着nums1[index + 1]到nums1[n - 1]这n - index - 1个数中，只有剩下的n - index - 1 - (p - left - 1)个数的映射值大于p，也就是上面描述的right。

这样一来，就可以在O(logn)的时间内求出每一个nums1[index]对应的left和right了，总的时间复杂度就是O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def goodTriplets(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        mapping = {}
        for index, num in enumerate(nums2):
            mapping[num] = index + 1
        
        res = 0
        n = len(nums1)
        suffix_array = [0] * (n + 1)
        for index, num in enumerate(nums1):
            p = mapping[num]
            
            left = 0
            now = p - 1
            while now > 0:
                left += suffix_array[now]
                now -= (now & -now)
            
            right = (n - index - 1) - (p - left - 1)
            res += left * right

            now = p
            while now <= n:
                suffix_array[now] += 1
                now += (now & -now)
        
        return res
```
