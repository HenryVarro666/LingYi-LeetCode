---
title: "1985. 找出数组中的第K大整数"
aliases: ["yiduobo的每日leetcode 1985.找出数组中的第K大整数"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/498738086"
zhihu_id: "498738086"
zhihu_title: "yiduobo的每日leetcode 1985.找出数组中的第K大整数"
question_id: "1985"
question: "找出数组中的第 K 大整数"
problem_url: "https://leetcode.cn/problems/find-the-kth-largest-integer-in-the-array/"
difficulty: "Medium"
created: "2022-04-14T22:06:13+08:00"
updated: "2022-04-14T22:06:13+08:00"
upvotes: 0
comments: 0
---

# 1985. 找出数组中的第K大整数

> **[yiduobo的每日leetcode 1985.找出数组中的第K大整数](https://zhuanlan.zhihu.com/p/498738086) · 知乎 · 2022-04-14 · 赞同 0**
> 力扣：[1985. 找出数组中的第 K 大整数](https://leetcode.cn/problems/find-the-kth-largest-integer-in-the-array/) · Medium · 灵茶山艾府：[Go 自定义排序](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1985.找出数组中的第K大整数

[力扣](https://leetcode-cn.com/problems/find-the-kth-largest-integer-in-the-array/)

找第K大数的字符串大整数版本，同样适用快速选择算法，只需要在判断大小时改为字符串数字的判断方式就行了。具体算法思路则可以参考前面的215题的做法。

[yiduobo：yiduobo的每日leetcode 215.数组中的第K个最大元素](https://zhuanlan.zhihu.com/p/148151993)

最后附上python代码：

```python
class Solution(object):
    def kthLargestNumber(self, nums, k):
        """
        :type nums: List[str]
        :type k: int
        :rtype: str
        """

        return self.search(nums, 0, len(nums) - 1, len(nums) - k + 1)

    def search(self, nums, left, right, k):
        if left == right:
            return nums[left]

        mid = nums[(left + right) / 2][:]
        i = left
        j = right
        while i <= j:
            while i <= right and len(nums[i]) < len(mid) or (len(nums[i]) == len(mid) and (nums[i] < mid)):
                i += 1
            while j >= left and len(nums[j]) > len(mid) or (len(nums[j]) == len(mid) and (nums[j] > mid)):
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j][:], nums[i][:]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
```
