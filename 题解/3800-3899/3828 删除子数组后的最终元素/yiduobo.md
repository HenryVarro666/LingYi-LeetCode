---
title: "3828. 删除子数组后的最终元素"
aliases: ["yiduobo的每日leetcode 3828.删除子数组后的最终元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/brainteaser", "leetcode/game-theory", "题单/数学算法", "题单/贪心算法", "题单/数学算法/四-博弈论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2002176542231515871"
zhihu_id: "2002176542231515871"
zhihu_title: "yiduobo的每日leetcode 3828.删除子数组后的最终元素"
question_id: "3828"
question: "删除子数组后的最终元素"
problem_url: "https://leetcode.cn/problems/final-element-after-subarray-deletions/"
difficulty: "Medium"
rating: 1591
created: "2026-02-05T02:58:12+08:00"
updated: "2026-02-05T02:58:12+08:00"
upvotes: 2
comments: 0
---

# 3828. 删除子数组后的最终元素

> **[yiduobo的每日leetcode 3828.删除子数组后的最终元素](https://zhuanlan.zhihu.com/p/2002176542231515871) · 知乎 · 2026-02-05 · 赞同 2**
> 力扣：[3828. 删除子数组后的最终元素](https://leetcode.cn/problems/final-element-after-subarray-deletions/) · Medium · 灵茶山艾府：[脑筋急转弯，严格证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3828.删除子数组后的最终元素

<https://leetcode.cn/problems/final-element-after-subarray-deletions/>

题目给出一个整数数组nums。

有两名玩家alice和bob轮流进行游戏，alice是先手。

- 每一轮中，当前玩家都可以从选择任意一个子数组，这个子数组的长度必须小于当前数组的长度。换言之，就是不能全选。
- 被选择的子数组将被移除，剩余的元素将连接起来形成新的数组
- 当只剩下唯一一个元素时，游戏终止

alice想让剩下的元素最大，而bob则想让剩下的元素最小。在双方都采取最优策略的情况下，最终剩下的元素是多少。

乍一看感觉没什么特别好的思路，不妨考虑先从极端情况入手。

根据题目的描述，alice是有能力直接结束游戏的，此时剩下的要么是nums[0]，要么是nums[-1]，也就是说，最终答案的下界就是max(nums[0], nums[-1])。

另一方面，如果alice没有选择在第一轮结束游戏的话，bob则可以在第二轮结束游戏。

在这里可以明确的是，alice操作后剩下的数组，其中一端必然是max(nums[0], nums[-1])，而另一端必然大于等于这个数，否则的话bob可以选择留下较小的那一端并结束游戏，这个结果对alice而言显然不如alice在第一轮就结束游戏并留下max(nums[0], nums[-1])更优。

而对于bob来说，由于有alice首轮操作是最优策略的这一前提，说明接下来无论怎么操作，最终结果都必然大于等于alice在首轮结束游戏得到的结果下界max(nums[0], nums[-1])，因此bob的最优选择就只能是在本轮结束游戏，留在较小的那一端，即max(nums[0], nums[-1])。

综合来说，就是alice在有能力在首轮直接结束游戏的情况下，选择不结束游戏而是继续操作，就说明后续局面无论bob怎样操作，最终得到的结果都必然大于等于alice在首轮就结束游戏得到的结果。因此对bob而言，最明智的选择就是直接结束游戏，取alice在首轮就结束游戏可以得到的最优解max(nums[0], nums[-1])。

最后附上python代码：

```python
class Solution(object):
    def finalElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        return max(nums[0], nums[-1])
```
