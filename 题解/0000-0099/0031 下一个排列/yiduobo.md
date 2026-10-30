---
title: "31. 下一个排列"
aliases: ["yiduobo的每日leetcode 31.下一个排列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/bian-li", "题单/数学算法", "题单/LeetCode-热题-100", "题单/数学算法/七-杂项", "题单/LeetCode-热题-100/技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/119442273"
zhihu_id: "119442273"
zhihu_title: "yiduobo的每日leetcode 31.下一个排列"
question_id: "31"
question: "下一个排列"
problem_url: "https://leetcode.cn/problems/next-permutation/"
difficulty: "Medium"
created: "2020-03-28T22:13:06+08:00"
updated: "2020-03-28T22:13:06+08:00"
upvotes: 0
comments: 0
---

# 31. 下一个排列

> **[yiduobo的每日leetcode 31.下一个排列](https://zhuanlan.zhihu.com/p/119442273) · 知乎 · 2020-03-28 · 赞同 0**
> 力扣：[31. 下一个排列](https://leetcode.cn/problems/next-permutation/) · Medium · 灵茶山艾府：[带你发明下一个排列算法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

31.下一个排列<https://leetcode-cn.com/problems/next-permutation/>

找规律的题目，首先可以找到下面两个规律。

(1)设a和b都是通过nums生成的排列，那么如果他们前k位都相同，且a[k + 1] \< b[k + 1]，a就一定是排在b前面的排列。

(2)如果有a[i] \< a[j]，且i \< j，那么交换a[i]与a[j]之后一定能形成更加靠后的排列。

通过(1)可以知道，对于一个排列a，如果能通过交换最后p位中的数字形成靠后的排列，那么就不应该把倒数第p + 1加入到交换的序列中。于是我们可以从后往前，看看最后的若干位能否找到更靠后的排列。此时可以通过(2)来进行判断，即可以从后往前扫描：

如果不存在a[pos] > a[pos - 1]，说明现在是逆序排列的，因此此时把a整个翻转过来就是答案了。

如果存在a[pos] > a[pos - 1]，那么pos - 1位就是我们应该交换的数。通过(1)可以得知，新的a[pos - 1]应该是pos以及后面的数中，大于a[pos - 1]的数中最小的那一个。通过一次扫描找个这个数，设为a[swap_pos]，那么交换a[pos - 1]与a[swap_pos]之后，a[pos : len(a)]依然是逆序的，此时只需要把这个部分翻转过来即可。

一次扫描找到pos，一次扫描找到swap_pos，再一次扫描翻转，因此时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def nextPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """

        pos = 0
        for index in range(len(nums) - 1, 0, -1):
            if nums[index] > nums[index - 1]:
                pos = index
                break
        if pos == 0:
            for index in range(len(nums) / 2):
                tmp = nums[index]
                nums[index] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp
        else:
            pos -= 1
            sawp_pos = None
            sawp_num = None
            for index in range(len(nums) - 1, pos, -1):
                if nums[index] > nums[pos]:
                    if sawp_num is None or sawp_num > nums[index]:
                        sawp_num = nums[index]
                        sawp_pos = index

            tmp = nums[pos]
            nums[pos] = nums[sawp_pos]
            nums[sawp_pos] = tmp

            for index in range((len(nums) - pos - 1) / 2):
                tmp = nums[pos + index + 1]
                nums[pos + index + 1] = nums[len(nums) - index - 1]
                nums[len(nums) - index - 1] = tmp
```
