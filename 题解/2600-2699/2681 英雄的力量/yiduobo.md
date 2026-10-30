---
title: "2681. 英雄的力量"
aliases: ["yiduobo的每日leetcode 2681.英雄的力量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649679421"
zhihu_id: "649679421"
zhihu_title: "yiduobo的每日leetcode 2681.英雄的力量"
question_id: "2681"
question: "英雄的力量"
problem_url: "https://leetcode.cn/problems/power-of-heroes/"
difficulty: "Hard"
rating: 2060
created: "2023-08-13T00:03:38+08:00"
updated: "2023-08-13T00:03:38+08:00"
upvotes: 0
comments: 0
---

# 2681. 英雄的力量

> **[yiduobo的每日leetcode 2681.英雄的力量](https://zhuanlan.zhihu.com/p/649679421) · 知乎 · 2023-08-13 · 赞同 0**
> 力扣：[2681. 英雄的力量](https://leetcode.cn/problems/power-of-heroes/) · Hard · 灵茶山艾府：[贡献法（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2681.英雄的力量

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/power-of-heroes/description/)

题目要求对数组的所有子集计算子集最大值的平方乘以子集最小值，然后求和。为了方便处理这里的最值，和自然想到先将数组进行排序。

排序完毕后，对于数组中的某个数nums[index]，其左侧的所有数都是小于等于nums[index]，也就是说其左侧的任意子集再加上nums[index]，得到的集合都是以nums[index]为子集最大值；另一方面，对于这些子集的最小值则不是那么容易计算出来，不过可以换一种思路，通过整体求解计算出来。

不妨设nums[index]左侧的数可构成集合中的最小值之和为mi_s，那么所有以nums[index]为最大值的子集的得分之和就是v \* v \* mi_s + v \* v \*v。前面这一项很好理解，就是将nums[index]额外加入到其左侧形成的所有集合后形成的集合得分之和，而最后一项则是单独选择nums[index]作为集合的得分。

接下里的问题是mi_s应该如何计算。可以发现，对于nums[index + 1]使用的mi_s"，其可以分为两个部分，也就是包含nums[index]的集合以及不包含nums[index]的集合。对于前者，这些集合的最小值之和依然还是mi_s，而对于后者，除去nums[index]单独形成的集合之外，其他集合在加入了nums[index]后的最小值不会发生变化，因此这些集合的最小值之和依然是mi_s，而对于nums[index]单独形成的集合，其最小值为nums[index]，因此就有mi_s" \= mi_s + mi_s + v，式子中的三项分别对应上面的三个部分。

这样一来，就得到了一种递推计算mi_s的方式，而mi_s的初始值显然为0，因为对于nums[0]而言其左侧是不存在任何集合的，因此mi_s也就是0。

最后附上python代码：

```python
class Solution(object):
    def sumOfPower(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0
        mod = 10 ** 9 + 7
        mi_s = 0

        for v in sorted(nums):
            res += v * v * (mi_s + v)
            res %= mod
            mi_s = (mi_s + mi_s + v) % mod
        
        return res
```
