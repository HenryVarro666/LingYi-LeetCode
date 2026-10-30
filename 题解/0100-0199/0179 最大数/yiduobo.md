---
title: "179. 最大数"
aliases: ["yiduobo的每日leetcode 179.最大数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/145173853"
zhihu_id: "145173853"
zhihu_title: "yiduobo的每日leetcode 179.最大数"
question_id: "179"
question: "最大数"
problem_url: "https://leetcode.cn/problems/largest-number/"
difficulty: "Medium"
created: "2020-06-01T22:11:56+08:00"
updated: "2020-06-01T22:11:56+08:00"
upvotes: 2
comments: 0
---

# 179. 最大数

> **[yiduobo的每日leetcode 179.最大数](https://zhuanlan.zhihu.com/p/145173853) · 知乎 · 2020-06-01 · 赞同 2**
> 力扣：[179. 最大数](https://leetcode.cn/problems/largest-number/) · Medium · 灵茶山艾府：[证明题：传递性和最优性（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

中间出现了一些sql和bash的题目，这里先跳过。

179.最大数<https://leetcode-cn.com/problems/largest-number/>

数学证明的题目。需要证明顺序的可传递性：

设nums[0]，nums[1]，nums[2]的长度分别为l0，l1，l2，且

(1)、nums[0] \* (10^l1) + nums[1] > nums[1] \* (10^l0) + nums[0]

(2)、nums[1] \* (10^l2) + nums[2] > nums[2] \* (10^l1) + nums[1]

需要证明

(3)、nums[0] \* (10^l2) + nums[2] > nums[2] \* (10^l0) + nums[0]

首先，nums[0]与nums[1]必然大于0，因为若nums[0]等于0，那么式(1)不成立。同理，若nums[1]等于0，那么式(2)不成立。

接下来，将式(1)与式(2)变形，得到

(4)、nums[0] \* (10^l1 - 1) > nums[1] \* (10^l0 - 1)

(5)、nums[1] \* (10^l2 - 1) > nums[2] \* (10^l1 - 1)

由于不等号两边均为非负数，因此不等号两边分别相乘，就有

(6)、nums[0] \* (10^l1 - 1) \* nums[1] \* (10^l2 - 1) > nums[1] \* (10^l0 - 1) \* nums[2] \* (10^l1 - 1)

由于nums[1]与(10^l1 - 1)都大于0，于是同时约掉这两项，最后得到

(7)、nums[0] \* (10^l2 - 1) > nums[2] \* (10^l0 - 1)

展开后是式(3)了

这说明如果nums[0]排在nums[1]之前较优，同时nums[1]排在nums[2]之前较优，那么一定有nums[0]排在nums[2]之前较优。

于是我们可以将nums排好序，然后依次拼接起来就好了。这里的依据是若最终答案中出现了逆序对，那么将逆序对调换之后答案一定更大，因为其他的nums提供的贡献不变，而上面证明了逆序提供的值小于顺序提供的值。

最后附上python代码：

```python
class Solution(object):
    def largestNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: str
        """

        nums = sorted(nums, self.cmp)

        if max(nums) == 0:
            return '0'
        else:
            return ''.join([str(x) for x in nums])

    def cmp(self, x, y):
        if str(x) + str(y) > str(y) + str(x):
            return -1
        return 1
```
