---
title: "18. 四数之和"
aliases: ["yiduobo的每日leetcode 18.四数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/115110040"
zhihu_id: "115110040"
zhihu_title: "yiduobo的每日leetcode 18.四数之和"
question_id: "18"
question: "四数之和"
problem_url: "https://leetcode.cn/problems/4sum/"
difficulty: "Medium"
created: "2020-03-21T23:49:33+08:00"
updated: "2020-03-22T01:15:24+08:00"
upvotes: 0
comments: 0
---

# 18. 四数之和

> **[yiduobo的每日leetcode 18.四数之和](https://zhuanlan.zhihu.com/p/115110040) · 知乎 · 2020-03-21 · 赞同 0**
> 力扣：[18. 四数之和](https://leetcode.cn/problems/4sum/) · Medium · 灵茶山艾府：[极致优化！基于三数之和的做法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

18.四数之和<https://leetcode-cn.com/problems/4sum/>

果然人类的本质就是套娃。

与15题三数之和类似，这次排序后枚举first_num和second_num，然后再找剩下两数即可。最后的时间复杂度是O(n^3)。

当然，对于重复的数字也是可以预先判断的，不过相比三数之和的判断方式要复杂很多，这里采取另一种思路。

---

对于排好序的数组nums，我们设数组left_pos和right_pos，其中：

left_pos[i] \= min(j，j > i && nums[j] !\= nums[i])，表示在nums[i]右边的第一个不等于nums[i]的数的位置。

相对应的right_pos[i] \= max(j，j \< i && nums[j] !\= nums[i])，表示在nums[i]左侧的第一个不等nums[i]的数的位置。

例如样例中的[1, 0, -1, 0, -2, 2]，排好序之和是[-2, -1, 0, 0, 1, 2]，那么有：

left_pos \= [1, 2, 4, 4, 5, 6]，其中，nums[2] \= nums[3] \= 0，所以nums[2] \= 4。

可以发现，当nums[l] \= nums[l + 1] \= ... \= nums[r]时，有left_pos[l] \= left_pos[l + 1] \= ... \= left_pos[r] \= r + 1。

right_pos \= [-1, 0, 1, 1, 3, 4]，其中，nums[3] \= nums[2] \= 0，所以nums[3] \= 1。

同样的，当nums[r] \= nums[r - 1] \= ... \= nums[l]时，有right_pos[r] \= right_pos[r - 1] \= ... \= right_pos[l] \= l - 1。

这样一来，通过从头到尾一次扫描，就可以得到right_pos。反过来从尾到头一次扫描，就能得到left_pos。

有了left_pos和right_pos，在后续的计算中，遇到需要移动first_num，second_num或是左右指针的时候，无需再一位一位移动，而是直接使用left_pos和right_pos进行移动即可。

最后附上python代码：

```python
class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """

        nums = sorted(nums)

        if len(nums) < 4:
            return []

        res = []
        left_pos = [i + 1 for i in range(len(nums))]
        right_pos = [i - 1 for i in range(len(nums))]

        for i in range(len(nums) - 2, -1, -1):
            if nums[i] == nums[i + 1]:
                left_pos[i] = left_pos[i + 1]
        for i in range(1, len(nums)):
            if nums[i] == nums[i - 1]:
                right_pos[i] = right_pos[i - 1]

        i = 0
        while i < len(nums) - 3:
            if nums[i] + nums[i + 1] + nums[i + 2] + nums[i + 3] > target:
                break
            if nums[i] + nums[-1] + nums[-2] + nums[-3] < target:
                i = left_pos[i]
                continue

            j = i + 1
            while j < len(nums) - 2:
                if nums[i] + nums[j] + nums[j + 1] + nums[j + 2] > target:
                    break
                if nums[i] + nums[j] + nums[-1] + nums[-2] < target:
                    j = left_pos[j]
                    continue

                left = j + 1
                right = len(nums) - 1

                new_target = target - nums[i] - nums[j]
                while left < right:
                    if nums[left] + nums[left + 1] > new_target:
                        break
                    if nums[right] + nums[right - 1] < new_target:
                        break
                    if nums[left] + nums[right] == new_target:
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        left = left_pos[left]

                    elif nums[left] + nums[right] < new_target:
                        left = left_pos[left]
                    else:
                        right = right_pos[right]

                j = left_pos[j]
            i = left_pos[i]

        return res
```
