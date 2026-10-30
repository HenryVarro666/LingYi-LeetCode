---
title: "2856. 删除数对后的最小数组长度"
aliases: ["yiduobo的每日leetcode 2856.删除数对后的最小数组长度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/binary-search", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661023928"
zhihu_id: "661023928"
zhihu_title: "yiduobo的每日leetcode 2856.删除数对后的最小数组长度"
question_id: "2856"
question: "删除数对后的最小数组长度"
problem_url: "https://leetcode.cn/problems/minimum-array-length-after-pair-removals/"
difficulty: "Medium"
rating: 1750
created: "2023-10-13T00:29:47+08:00"
updated: "2023-10-13T00:29:47+08:00"
upvotes: 0
comments: 0
---

# 2856. 删除数对后的最小数组长度

> **[yiduobo的每日leetcode 2856.删除数对后的最小数组长度](https://zhuanlan.zhihu.com/p/661023928) · 知乎 · 2023-10-13 · 赞同 0**
> 力扣：[2856. 删除数对后的最小数组长度](https://leetcode.cn/problems/minimum-array-length-after-pair-removals/) · Medium · 灵茶山艾府：[O(log n) 贪心+二分查找（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2856.删除数对后的最小数组长度

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-array-length-after-pair-removals/)

对于数组中的任意数x，其可以与另外任意一个与x不同的数y形成数对进行删除，也就是说只要数组中各元素出现次数的最大值max_freq不超过数组长度的一半，那么必然有办法将数组删完或者删到只剩下一个元素，这里的0还是1取决于数组长度是偶数还是奇数。反之，对于max_freq对应的元素，即使其与另外的所有元素都形成配对，也最多只能形成n - max_freq组数对，此时将遗留下max_freq \* 2 - n个元素无法配对。

最后附上python代码：

```python
class Solution(object):
    def minLengthAfterRemovals(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        max_freq = max(freq.values())
        if len(nums) - max_freq >= max_freq:
            return len(nums) % 2
        else:
            return max_freq * 2 - len(nums)
```
