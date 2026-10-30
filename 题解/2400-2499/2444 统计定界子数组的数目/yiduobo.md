---
title: "2444. 统计定界子数组的数目"
aliases: ["yiduobo的每日leetcode 2444.统计定界子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/two-pointers", "leetcode/bian-li", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/五-三指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/584787455"
zhihu_id: "584787455"
zhihu_title: "yiduobo的每日leetcode 2444.统计定界子数组的数目"
question_id: "2444"
question: "统计定界子数组的数目"
problem_url: "https://leetcode.cn/problems/count-subarrays-with-fixed-bounds/"
difficulty: "Hard"
rating: 2093
created: "2022-11-19T03:58:38+08:00"
updated: "2022-11-19T03:58:38+08:00"
upvotes: 0
comments: 0
---

# 2444. 统计定界子数组的数目

> **[yiduobo的每日leetcode 2444.统计定界子数组的数目](https://zhuanlan.zhihu.com/p/584787455) · 知乎 · 2022-11-19 · 赞同 0**
> 力扣：[2444. 统计定界子数组的数目](https://leetcode.cn/problems/count-subarrays-with-fixed-bounds/) · Hard · 灵茶山艾府：[一次遍历，简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2444.统计定界子数组的数目

[力扣](https://leetcode.cn/problems/count-subarrays-with-fixed-bounds/)

题目要求所有最大值为maxK，最小值为minK的子数组的数目。对于这个问题，可以拆分成两个部分，分别为：

1、找出所有数组值都在minK到maxK之间的子数组

2、对于上述子数组，找出所有minK和maxK都至少出现过一次的子数组的数目

首先是第一个问题。对于这个问题，可以先确定子数组的左边界left，然后从left开始向后找出当前left对应的最大的right。left的寻找相对简单，只需要满足nums[left]在minK到maxK之间就行了。而对于left对应的right，则可以从left开始向后遍历，直到遇到一个不在minK到maxK之间的数，或者到达数组的末尾。

找到一组left和right之后，就需要处理第二个问题，即对于nums[left]到nums[right]这一段中，所有既包含minK又包含maxK的子数组的数目。为了方便判断，在这里可以使用数组记录所有minK和maxK出现的位置，分别记为minK_list和maxK_list。这个操作可以在寻找right的过程中顺便完成。

得到所有minK和maxK的位置后，就可以从left开始向后枚举问题2中数组的左边界。不妨设当前枚举到的位置为l，那么只要l的右侧存在minK以及maxK，那么就有以l为左边界的定界子数组，而这些定界子数组中最小的右边界就是l右侧，minK以及maxK第一次出现位置中较大的那一个，最大的右边界则是right，那么就可以通过这两个右边界相减计算出以l为左边界的定界子数组的数量。

最后的问题就是对于l，如何找到其右侧第一次出现的minK以及maxK的位置。对于这个问题，同样是利用类似滑动窗口的处理方式。使用两个遍历minK_pos以及maxK_pos表示当前在minK_list和maxK_list中，第一次出现在l右侧的值在minK_list以及maxK_list中的下标，那么随着l的向右移动，minK_pos以及maxK_pos也会跟着向右移动，直到这两个变量移动到对应的数组尾部为止，此时left到right中所有的定界子数组就都找完了，此时只需重复上面的过程，寻找下一组left和right并计算其中的定界子数组数目，直到left来到原数组的末尾位置。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums, minK, maxK):
        """
        :type nums: List[int]
        :type minK: int
        :type maxK: int
        :rtype: int
        """

        n = len(nums)
        left = 0
        right = 0
        res = 0
        while left < n:
            while left < n and (nums[left] < minK or nums[left] > maxK):
                left += 1
            
            if left == n:
                break
            
            right = left
            minK_list = []
            maxK_list = []
            while right < n and minK <= nums[right] <= maxK:
                if nums[right] == minK:
                    minK_list.append(right)
                if nums[right] == maxK:
                    maxK_list.append(right)
                right += 1

            minK_pos = maxK_pos = 0
            while minK_pos != len(minK_list) and maxK_pos != len(maxK_list):
                res += right - max(minK_list[minK_pos], maxK_list[maxK_pos])
                if nums[left] == minK:
                    minK_pos += 1
                if nums[left] == maxK:
                    maxK_pos += 1
                
                left += 1
            
            left = right
            
        return res
```
