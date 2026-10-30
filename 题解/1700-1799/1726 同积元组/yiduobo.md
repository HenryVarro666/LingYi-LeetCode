---
title: "1726. 同积元组"
aliases: ["yiduobo的每日leetcode 1726.同积元组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452017865"
zhihu_id: "452017865"
zhihu_title: "yiduobo的每日leetcode 1726.同积元组"
question_id: "1726"
question: "同积元组"
problem_url: "https://leetcode.cn/problems/tuple-with-same-product/"
created: "2021-12-31T12:41:23+08:00"
updated: "2021-12-31T12:41:23+08:00"
upvotes: 1
comments: 0
---

# 1726. 同积元组

> **[yiduobo的每日leetcode 1726.同积元组](https://zhuanlan.zhihu.com/p/452017865) · 知乎 · 2021-12-31 · 赞同 1**
> 力扣：[1726. 同积元组](https://leetcode.cn/problems/tuple-with-same-product/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1726.同积元组

[力扣](https://leetcode-cn.com/problems/tuple-with-same-product/)

首先需要考虑去重。由于nums中不存在相同的元素，因此只需要保持一组乘积中靠前的元素在数组中的下标小于靠后的元素，就不会出现重复的情况了。

对于出现次数，题目也非常贴心地给出了一组合法的a、b、c、d可以带来8中合法的答案，若某个乘积一共出现了k次，那么从中任选两组数，就是C(k, 2)中选法，每种选法提供8种答案，那么这里就有k \* (k - 1) \* 4种答案。

于是现在的做法就是两两遍历数组中的元素，保证前一个元素的下标小于后一个元素的下标，将二者之积以及出现的次数统计起来。然后对于所有的乘积，使用上面的式子更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def tupleSameProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt_dict = {}
        n = len(nums)
        for i in range(n - 1):
            for j in range(i + 1, n):
                m = nums[i] * nums[j]
                cnt_dict[m] = cnt_dict.get(m, 0) + 1
        
        res = 0
        for cnt in cnt_dict.values():
            res += cnt * (cnt - 1) * 4
        
        return res
```
