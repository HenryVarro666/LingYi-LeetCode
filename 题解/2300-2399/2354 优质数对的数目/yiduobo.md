---
title: "2354. 优质数对的数目"
aliases: ["yiduobo的每日leetcode 2354.优质数对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/math", "leetcode/prefix-sum", "题单/位运算", "题单/位运算/六-恒等式"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561612480"
zhihu_id: "561612480"
zhihu_title: "yiduobo的每日leetcode 2354.优质数对的数目"
question_id: "2354"
question: "优质数对的数目"
problem_url: "https://leetcode.cn/problems/number-of-excellent-pairs/"
difficulty: "Hard"
rating: 2076
created: "2022-09-06T00:28:35+08:00"
updated: "2022-09-06T00:28:35+08:00"
upvotes: 1
comments: 0
---

# 2354. 优质数对的数目

> **[yiduobo的每日leetcode 2354.优质数对的数目](https://zhuanlan.zhihu.com/p/561612480) · 知乎 · 2022-09-06 · 赞同 1**
> 力扣：[2354. 优质数对的数目](https://leetcode.cn/problems/number-of-excellent-pairs/) · Hard · 灵茶山艾府：[等价转换 + 后缀和优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2354.优质数对的数目

[力扣](https://leetcode.cn/problems/number-of-excellent-pairs/)

首先，注意到题目中的数可以与自身形成数对，同时相同的数对只计算一次，因此可以先过滤掉重复出现的数。

接下来看看题目中关于优质数对的定义。对于数组中的两个数nums1和nums2，需要计算两个数按位与以及按位或，然后将这两个结果中1的数目相加,。若这里1的总数大于等于k，那么nums1和nums2是合法的数对。由于数据规模比较大，很明显不能两两枚举然后再计算按位与以及按位或，必须另想办法。

不妨设nums1和nums2的二进制表示中分别有cnt1和cnt2个1，那么两数取或之后，结果中1的数目就等于cnt1 + cnt2，再减去那些在nums1和nums2中都为1的数位的数目。可以发现，后面这一句描述的恰好就是nums1和nums2做与运算的结果中1的数目。换言之，题目要找的1的数目恰好就是cnt1 + cnt2。

于是可以先一趟遍历，计算出每个数二进制下1的数目，使用一个数组cnt记录下来。

接下来再一趟遍历，对于当前nums[index]，其二进制表示下就有cnt[index]个1，那么：

1、若cnt[index] >\= k，那么其与数组中的任意数都可以组成合法的数对，此时应该使用去重后的数组长度来更新答案。

2、若cnt[index] \< k，那么若这个缺口，也就是k - cnt[index]小于等于30，那么就可能被nums中的数填补上，此时就需要找出cnt中大于等于k - cnt[index]的数目。

不妨设f[index]表示cnt中大于等于index的数的数目，那么在这里可以利用类似后缀和的做法来求解f。可以先初始化f[index]为cnt中值等于index的数的数目，然后再使用f[index] \= f[index + 1]来递推计算得到最终想要的f。这里的f可以在得到cnt之后里面预处理出来。

那么对于当前情况，能与nums\[index\]形成合法数对的数的数目就是f\[k - cnt\[index\]\]。

最后附上python代码：

```python
class Solution(object):
    def countExcellentPairs(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums = list(set(nums))

        cnt_list = []
        f = [0] * 31
        for num in nums:
            cnt = 0
            while num:
                cnt += 1
                num -= num & -num
            
            cnt_list.append(cnt)
            f[cnt] += 1
        
        for index in range(29, -1, -1):
            f[index] += f[index + 1]

        res = 0
        for cnt in cnt_list:
            if cnt >= k:
                res += f[0]
            elif k - cnt <= 30:
                res += f[k - cnt]
        
        return res
```
