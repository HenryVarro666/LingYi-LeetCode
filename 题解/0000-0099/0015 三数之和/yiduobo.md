---
title: "15. 三数之和"
aliases: ["yiduobo的每日leetcode 15.三数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/滑动窗口与双指针/三-单序列双指针", "题单/LeetCode-热题-100/双指针", "题单/面试经典-150-题/双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/114860209"
zhihu_id: "114860209"
zhihu_title: "yiduobo的每日leetcode 15.三数之和"
question_id: "15"
question: "三数之和"
problem_url: "https://leetcode.cn/problems/3sum/"
difficulty: "Medium"
created: "2020-03-20T22:34:47+08:00"
updated: "2020-03-20T22:34:47+08:00"
upvotes: 0
comments: 0
---

# 15. 三数之和

> **[yiduobo的每日leetcode 15.三数之和](https://zhuanlan.zhihu.com/p/114860209) · 知乎 · 2020-03-20 · 赞同 0**
> 力扣：[15. 三数之和](https://leetcode.cn/problems/3sum/) · Medium · 灵茶山艾府：[【视频】极致优化！一个视频讲透双指针！（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

15.三数之和<https://leetcode-cn.com/problems/3sum/>

第一题的升级版本，一个可行的思路是排序后固定住第一个数，设为first_num，然后从这个数后一位开始，使用第一题的方法找到两数之和为 -first_num的两个数即可。时间复杂度为O(n^2)。

有一个可以优化的点是，当出现两个相同的数字时，只需要选一个作为first_num即可。这样一来可以优先计算解是a + a + b \= 0形式的答案，然后在去除掉一个a之后再使用上面的方法计算，可以在一定程度上缩小n的规模。需要特别注意的是，有一个特例，即0 + 0 + 0 \= 0。

计算a + a + b \= target的具体方案是，对于排好序的数组nums，从头往后遍历，如果nums[index] \=\= nums[index - 1]，那么在set记录下nums[index] \* 2，否则将nums[index]加入到新的数组new_nums中。

接下来从头开始遍历新的数组，检查 -new_nums[index]是否存在于set中，如果存在，那么表示 -new_nums[index] / 2是一nums中的一个重复元素，且形成了一组解。

接下来就按最上面的做法寻找剩下的解即可。时间复杂度依然为O(n ^ 2)，但是由于n的规模缩小了一些，效率会稍微高一点。

最后附上python代码，其中double_set记录重复出现两次的数，zero_count则是为了处理三个0的情况，最后的二重循环则是确定first_num之后寻找其他两个数的部分：

```python
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        
        res = []

        if len(nums) < 3:
            return []

        double_set = set()
        nums = sorted(nums)

        zero_count = 0
        new_nums = []
        for index in range(len(nums)):
            if index > 0 and nums[index] == nums[index - 1]:
                double_set.add(nums[index] + nums[index])
            else:
                new_nums.append(nums[index])
            if nums[index] == 0:
                zero_count += 1

        for index in range(len(new_nums)):
            if -new_nums[index] in double_set:
                if new_nums[index] == 0 and zero_count < 3:
                    continue
                res.append([-new_nums[index] / 2, -new_nums[index] / 2, new_nums[index]])

        for index, first_num in enumerate(new_nums):
            left = index + 1
            right = len(new_nums) - 1
            while left < right:
                if new_nums[left] + new_nums[right] == -first_num:
                    res.append([first_num, new_nums[left], new_nums[right]])
                    left += 1
                elif new_nums[left] + new_nums[right] < -first_num:
                    left += 1
                else:
                    right -= 1
        return res
```
