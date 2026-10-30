---
title: "1658. 将x减到0的最小操作数"
aliases: ["yiduobo的每日leetcode 1658.将x减到0的最小操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/441509400"
zhihu_id: "441509400"
zhihu_title: "yiduobo的每日leetcode 1658.将x减到0的最小操作数"
question_id: "1658"
question: "将 x 减到 0 的最小操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-reduce-x-to-zero/"
difficulty: "Medium"
rating: 1817
created: "2021-12-05T18:30:24+08:00"
updated: "2021-12-05T18:30:24+08:00"
upvotes: 0
comments: 0
---

# 1658. 将x减到0的最小操作数

> **[yiduobo的每日leetcode 1658.将x减到0的最小操作数](https://zhuanlan.zhihu.com/p/441509400) · 知乎 · 2021-12-05 · 赞同 0**
> 力扣：[1658. 将 x 减到 0 的最小操作数](https://leetcode.cn/problems/minimum-operations-to-reduce-x-to-zero/) · Medium · 灵茶山艾府：[两种写法：逆向思维/直接双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1658.将x减到0的最小操作数

[力扣](https://leetcode-cn.com/problems/minimum-operations-to-reduce-x-to-zero/)

由于只能从两端删去元素，那么最终删去的一定是数组的一个前缀加上一个后缀，那么可以计算数组的前缀和并记录该前缀和第一次出现的位置，然后枚举每个后缀，若当前后缀和为suffix_s，那么只需要找到前缀和为x - suffix_s第一次出现的位置，然后根据这一组前缀和后缀的长度更新答案即可。

除此之外，还有一种思路是将前缀和与后缀和视为从整个数组中去掉中间的连续一段，即寻找数组中长度最小的连续区间，满足该区间中所有数的和等于sum(nums) - x。对于这类区间和问题经典做法也还是前缀和，不过注意到这里nums中的数都非负，所以也可以使用双指针来做。

往常都是用前缀和来实现的，这一次我选择了用双指针。

首先需要计算出nums的总和s，那么需要寻找的区间和就是target \= s - x。

接下来考察边界情况。若target \= 0，说明整个数组都要被删掉，直接返回n。若target \< 0，说明删掉整个数组都凑不够x，直接返回-1。

接下来再考察一般情况。

初始化左指针l为0，右指针r为1，那么此时的区间和now就是nums[0]。接下来若l \< n，那么：

1、若r小于n且now \< target，那么就需要向右继续扩展区间，将nums[r]加入到now当中并将r向右移动一位。重复此过程直到r到达n或者now大于等于target。

2、若此时的now \< target且r等于n，说明后续子区间的和不可能达到target了，此时可以推出循环了。

3、若此时的l \< r且now > target，说明需要从区间中移除掉左边界，于是将nums[l]从now当中减去，并将l向右移动一位。重复此过程直到l到达r或者now小于等于target。

4、若此时的now \= target，说明保留当前的l到r - 1，删去0到l - 1的部分以及r到n - 1的部分可以使得x变为0，此时删去元素的个数可以认为是除了l到r - 1这一段全部删去，因此一共是n - (r - l)个数。用这个值更新答案。另外，此时以l为左边界的区间没有继续向右扩展的意义了，因为区间和必然会大于target，那么也需要将nums[l]从now当中减去，并将l向右移动一位。

重复上面的过程直到l到达n。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """

        n = len(nums)
        target = sum(nums) - x
        if target == 0:
            return n
        elif target < 0:
            return -1

        res = -1
        l = 0
        r = 1
        now = nums[0]

        while l < n:
            while now < target and r < n:
                now += nums[r]
                r += 1
            
            if now < target and r == n:
                break

            while l < r and now > target:
                now -= nums[l]
                l += 1

            if now == target:
                if res == -1 or res > n - (r - l):
                    res = n - (r - l)
                now -= nums[l]
                l += 1
            
        return res
```
