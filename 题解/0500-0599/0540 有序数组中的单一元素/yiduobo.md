---
title: "540. 有序数组的单一元素"
aliases: ["yiduobo的每日leetcode 540.有序数组的单一元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/四-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261209054"
zhihu_id: "261209054"
zhihu_title: "yiduobo的每日leetcode 540.有序数组的单一元素"
question_id: "540"
question: "有序数组中的单一元素"
problem_url: "https://leetcode.cn/problems/single-element-in-a-sorted-array/"
difficulty: "Medium"
created: "2020-10-07T22:23:59+08:00"
updated: "2020-10-07T22:23:59+08:00"
upvotes: 0
comments: 0
---

# 540. 有序数组的单一元素

> **[yiduobo的每日leetcode 540.有序数组的单一元素](https://zhuanlan.zhihu.com/p/261209054) · 知乎 · 2020-10-07 · 赞同 0**
> 力扣：[540. 有序数组中的单一元素](https://leetcode.cn/problems/single-element-in-a-sorted-array/) · Medium · 灵茶山艾府：[二分，性质分析+简洁写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

540.有序数组的单一元素<https://leetcode-cn.com/problems/single-element-in-a-sorted-array/>

很有意思的题目。题目描述每个元素出现两次，而其中有一个只出现了一次，那么就有一个隐藏条件，即数组长度的奇偶性。

对于有序数组查找问题，一般想到的就是二分。

那么对于区间l到r，找出nums[mid]：

1、若nums[mid]等于nums[mid - 1]，此时可以判断l到mid - 2这一段的长度是奇数还是偶数，因为如果答案在里面，其长度必然为奇数，否则为偶数。即mid - l - 1为奇数，那么答案位于区间l到mid - 2，那么r \= mid - 2，否则答案位于区间mid + 1到r，那么l \= mid + 1。

2、若nums[mid]等于nums[mid + 1]，此时可以判断mid + 2到r这一段的长度是奇数还是偶数，即r - mid + 1为奇数，那么答案位于区间mid + 2到r之间，于是有l \= mid + 2，否则就是r \= mid - 1。

3、若nums[mid]不满足情况1和情况2，那么说明nums[mid]就是要求的答案。

若最后没有出现情况3且退出了二分的循环，那么此时的nums[l]即为答案。

最后附上python代码：

```python
class Solution(object):
    def singleNonDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        l = 0
        r = len(nums) - 1
        while l < r:
            mid = (l + r) / 2
            if mid > l and nums[mid] == nums[mid - 1]:
                if (mid - l - 1) % 2 == 0:
                    l = mid + 1
                else:
                    r = mid - 2
            elif mid < r and nums[mid] == nums[mid + 1]:
                if (r - mid - 1) % 2 == 0:
                    r = mid - 1
                else:
                    l = mid + 2
            else:
                return nums[mid]
        
        return nums[l]
```
