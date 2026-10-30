---
title: "2527. 查询数组Xor美丽值"
aliases: ["yiduobo的每日leetcode 2527.查询数组Xor美丽值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/636628423"
zhihu_id: "636628423"
zhihu_title: "yiduobo的每日leetcode 2527.查询数组Xor美丽值"
question_id: "2527"
question: "查询数组异或美丽值"
problem_url: "https://leetcode.cn/problems/find-xor-beauty-of-array/"
difficulty: "Medium"
rating: 1550
created: "2023-06-13T01:43:37+08:00"
updated: "2023-06-13T01:43:37+08:00"
upvotes: 0
comments: 0
---

# 2527. 查询数组Xor美丽值

> **[yiduobo的每日leetcode 2527.查询数组Xor美丽值](https://zhuanlan.zhihu.com/p/636628423) · 知乎 · 2023-06-13 · 赞同 0**
> 力扣：[2527. 查询数组异或美丽值](https://leetcode.cn/problems/find-xor-beauty-of-array/) · Medium · 灵茶山艾府：[两种思路：对称性 / 拆位法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2527.查询数组Xor美丽值

[力扣](https://leetcode.cn/problems/find-xor-beauty-of-array/)

乍一看感觉是与数位操作有关的问题，不过注意到本题最终是计算异或值，且参与最终异或运算的中间结果所需的三元组(i, j, k)中的i、j、k是完全等价的，那么就可能可以通过对称性以及相同值异或结果为0来进行化简。

具体来说：

1、i、j、k三者两两不同的情况：

对于每一组(nums[i] | nums[j]) & nums[k]，都存在一组(nums[j] | nums[i]) & nums[k]。

由于括号内的或运算结果相同，因此这两组三元组的最终结果也相同，在最终异或运算时二者异或就变成了0。换言之，两两不同的i、j、k三元组不会对最终结果产生任何影响

2、i与j相同，但与k不同的情况：

对于每一组(nums[i] | nums[i]) & nums[k]，都存在一组(nums[k] | nums[k]) & nums[i]。

同样的，这种情况下的三元组也不会影响到最终结果

3、i与j不同，且i与k相同的情况：

对于每一组(nums[i] | nums[j]) & nums[i]，都存在一组(nums[j] | nums[i]) & nums[i]。

可以发现，这种情况本质上与情况1相同

4、i与j不同，且j与k相同的情况：

这种情况与情况3对称，不需要额外讨论

5、三元组中的i、j、k都相同的情况：

这种情况下，每一组(nums[i] | nums[i]) & nums[i]的计算结果就是nums[i]，同时这种情况是找不到对称情况的。因此这种情况下将会有nums[i]参与到最终结果的计算中

综合以上几种情况，可以发现只有情况5中的结果会影响到最终结果，而最终结果就是将原数组全部异或起来。

最后附上python代码：

```python
class Solution(object):
    def xorBeauty(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        for num in nums:
            res ^= num
        
        return res
```
