---
title: "3824. 减小数组使其满足条件的最小k值"
aliases: ["yiduobo的每日leetcode 3824.减小数组使其满足条件的最小k值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2001437320335890013"
zhihu_id: "2001437320335890013"
zhihu_title: "yiduobo的每日leetcode 3824.减小数组使其满足条件的最小k值"
question_id: "3824"
question: "减小数组使其满足条件的最小 K 值"
problem_url: "https://leetcode.cn/problems/minimum-k-to-reduce-array-within-limit/"
difficulty: "Medium"
rating: 1531
created: "2026-02-03T00:23:16+08:00"
updated: "2026-02-03T00:23:19+08:00"
upvotes: 2
comments: 0
---

# 3824. 减小数组使其满足条件的最小k值

> **[yiduobo的每日leetcode 3824.减小数组使其满足条件的最小k值](https://zhuanlan.zhihu.com/p/2001437320335890013) · 知乎 · 2026-02-03 · 赞同 2**
> 力扣：[3824. 减小数组使其满足条件的最小 K 值](https://leetcode.cn/problems/minimum-k-to-reduce-array-within-limit/) · Medium · 灵茶山艾府：[二分答案 + 上下界优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3824.减小数组使其满足条件的最小k值

<https://leetcode.cn/problems/minimum-k-to-reduce-array-within-limit/description/>

题目给出一个正整数数组nums。

对于一个正整数k，定义nonPositive(nums, k)为使得nums的每个元素都变为非正数所需的最小操作次数。在意给操作中，可以选择一个下标index，并将nums[index]减少k。

要求找出最小的k，满足nonPositive(nums, k) \<\= k^2。

首先，对于某个nums[index]，将其变为非正的操作次数为nums[index]除以k，向上取整。

随着k的增大，所需的操作次数是越来越少的，也就是说nonPositive(nums, k)会随着k的增大越来越小。另一方面，k^2显然是随着k的增大越来越大的，也就是说k越大，满足最后这个不等式的可能性就越大，因此在这里可以通过二分答案来寻找这个最小的k。

二分的下界为1，而对于二分的上界，一个自然的想法max(nums)，因为当k取max(nums)时，nums中所有元素变为非正所需的操作次数都是1次。但是需要注意的是，在这种情况下，nonPositive(nums, k)恰好就等于nums的长度n，但是此时的k^2并不一定大于等于n。更进一步的，由于nonPositive(nums, k)至少为n，因此k的取值至少是sqrt(n)向上取整，于是这里二分的上界就应该取max(max(nums), sqrt(n)向上取整)。

确定了二分的上下界之后，就可以开始进行二分了。对于当前二分到的mid，只需一趟遍历，计算对应的nonPositive(nums, mid)，若其小于等于mid^2，就修正二分上界为mid，否则修正二分下界为mid + 1。

最后附上python代码：

```python
class Solution(object):
    def minimumK(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        ma = max(nums)

        left = 1
        right = max(ma, int(n ** 0.5) + 1)
        while left < right:
            mid = (left + right) // 2
            cnt = 0
            for v in nums:
                cnt += v // mid
                if v % mid != 0:
                    cnt += 1
            
            if cnt <= mid * mid:
                right = mid
            else:
                left = mid + 1
    
        return left
```
