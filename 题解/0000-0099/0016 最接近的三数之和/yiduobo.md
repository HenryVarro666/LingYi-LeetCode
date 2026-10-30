---
title: "16. 最接近的三数之和"
aliases: ["yiduobo的每日leetcode 16.最接近的三数之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sorting", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/三-单序列双指针"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/114863639"
zhihu_id: "114863639"
zhihu_title: "yiduobo的每日leetcode 16.最接近的三数之和"
question_id: "16"
question: "最接近的三数之和"
problem_url: "https://leetcode.cn/problems/3sum-closest/"
difficulty: "Medium"
created: "2020-03-20T22:39:56+08:00"
updated: "2020-03-20T22:39:56+08:00"
upvotes: 0
comments: 0
---

# 16. 最接近的三数之和

> **[yiduobo的每日leetcode 16.最接近的三数之和](https://zhuanlan.zhihu.com/p/114863639) · 知乎 · 2020-03-20 · 赞同 0**
> 力扣：[16. 最接近的三数之和](https://leetcode.cn/problems/3sum-closest/) · Medium · 灵茶山艾府：[极致优化！基于三数之和的做法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

16.最接近的三数之和<https://leetcode-cn.com/problems/3sum-closest/>

与15题相同，也是固定住first_num之后寻找另外两数，如果能直接匹配那么就返回结果，否则记录下当前结果与目标的差值并更新最优解，并移动left或right直到无法继续移动。时间复杂度依然是O(n^2)。另外，重复的数只做一次first_num这个优化依然适用。

最后附上python代码：

```python
class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """

        nums = sorted(nums)

        min_delta = None

        for index, first_num in enumerate(nums):
            if index > 0 and first_num == nums[index - 1]:
                continue
            left = index + 1
            right = len(nums) - 1
            new_target = target - first_num
            while left < right:
                now = nums[left] + nums[right]
                if now == new_target:
                    return target
                delta = new_target - now
                if min_delta is None or abs(delta) < abs(min_delta):
                    min_delta = delta
                if delta > 0:
                    left += 1
                else:
                    right -= 1

        return target - min_delta
```
