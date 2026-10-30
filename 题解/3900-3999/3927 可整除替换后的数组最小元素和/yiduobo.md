---
title: "3927. 可整除替换后的数组最小元素和"
aliases: ["yiduobo的每日leetcode 3927.可整除替换后的数组最小元素和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2038382864618737793"
zhihu_id: "2038382864618737793"
zhihu_title: "yiduobo的每日leetcode 3927.可整除替换后的数组最小元素和"
question_id: "3927"
question: "可整除替换后的数组最小元素和"
problem_url: "https://leetcode.cn/problems/minimize-array-sum-using-divisible-replacements/"
difficulty: "Medium"
rating: 1652
created: "2026-05-14T22:31:05+08:00"
updated: "2026-05-14T22:31:05+08:00"
upvotes: 2
comments: 0
---

# 3927. 可整除替换后的数组最小元素和

> **[yiduobo的每日leetcode 3927.可整除替换后的数组最小元素和](https://zhuanlan.zhihu.com/p/2038382864618737793) · 知乎 · 2026-05-14 · 赞同 2**
> 力扣：[3927. 可整除替换后的数组最小元素和](https://leetcode.cn/problems/minimize-array-sum-using-divisible-replacements/) · Medium · 灵茶山艾府：[替换成最小的因子（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3927.可整除替换后的数组最小元素和

<https://leetcode.cn/problems/minimize-array-sum-using-divisible-replacements/description/>

题目给出一个整数数组nums，其长度以及其中元素的大小都不超过10^5。

现在可以执行以下操作任意次：选择任意两个下标a和b，满足nums[a]可以被nums[b]整除，然后将nums[a]替换为nums[b]。

问执行任意次操作后，数组可能得到的最小元素和。

题目要求使得数组的元素和最小，那么最佳的处理方式就是将每个元素都变成可以整除它的最小元素。由于题目中数组的长度不小，因此直接暴力显然是不行的。不过相对的，其中元素的大小不算太大，因此可以使用类似筛法的方法来进行处理。

具体来说，先使用一个哈希表cnt记录每种元素出现的次数，接下来从1开始向上枚举。对于当前枚举到的v，若cnt[v]大于0，那么说明数组中存在v，那么就沿着2v、3v向上枚举，将数组中的这些元素都变为v，更新cnt同时更新答案。这样一来，既可以保证所有v的倍数都变成了其最小的约数v，又可以保证cnt中留下的必然都是无法进一步变小的元素。

最后附上python代码：

```python
class Solution(object):
    def minArraySum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        cnt = {}
        ma = 0
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            ma = max(ma, v)
            
        res = 0
        for v in range(1, ma + 1):
            if cnt.get(v, 0) > 0:
                for x in range(v, ma + 1, v):
                    if x in cnt:
                        res += cnt[x] * v
                        cnt.pop(x)

        return res
```
