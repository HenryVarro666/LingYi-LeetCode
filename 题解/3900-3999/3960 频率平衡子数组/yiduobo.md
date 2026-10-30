---
title: "3960. 频率平衡子数组"
aliases: ["yiduobo的每日leetcode 3960.频率平衡子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2049533537070719467"
zhihu_id: "2049533537070719467"
zhihu_title: "yiduobo的每日leetcode 3960.频率平衡子数组"
question_id: "3960"
question: "频率平衡子数组"
problem_url: "https://leetcode.cn/problems/frequency-balance-subarray/"
difficulty: "Medium"
created: "2026-06-14T17:01:01+08:00"
updated: "2026-06-14T17:01:15+08:00"
upvotes: 1
comments: 0
---

# 3960. 频率平衡子数组

> **[yiduobo的每日leetcode 3960.频率平衡子数组](https://zhuanlan.zhihu.com/p/2049533537070719467) · 知乎 · 2026-06-14 · 赞同 1**
> 力扣：[3960. 频率平衡子数组](https://leetcode.cn/problems/frequency-balance-subarray/) · Medium · 灵茶山艾府：[维护出现次数的出现次数 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3960.频率平衡子数组

<https://leetcode.cn/problems/frequency-balance-subarray/description/>

题目给出一个整数数组nums，其长度不超过1000。

对于一个数组，若其满足一下两个条件之一，则称其为频率平衡子数组：

- 子数组中只包含一种元素。
- 子数组中包含至少两种元素，且这些元素出现的频率不完全相同。同时对于其中每种出现频率最高的元素，其出现次数都必须是数组中，其他非出现频率最高的元素出现次数的两倍。

问数组中最长频率平衡子数组的长度。

根据题目的描述，有两种子数组满足条件：

1、所有元素都相同的子数组。

2、恰好包含两种不同频率的子数组，且较大的频率是较小频率的两倍。需要注意这里的两种不同频率，对应的不一定是只有两种元素，例如[1, 1, 2, 2, 3]，1和2的频率都是2，而3的频率为1，因此这个子数组也是恰好包含两种不同频率，且较大频率是较小频率的两倍的子数组。

由于本题的数据规模较小，因此可以直接枚举子数组的起点start，然后从start开始向后枚举终点，逐个将元素加入子数组，同时使用一个哈希表freq统计其中元素的频率，并使用另一个哈希表freq_freq统计freq中不同频率出现的次数。

那么对于当前遍历到的下标index，不妨设对应的nums\[index\]为v，那么在这里就需要先使用v更新freq\[v\]，然后使用freq\[v\]更新freq_freq\[freq\[v\]\]。接下来：

- 若freq的长度为1，说明当前子数组是所有元素都相同的子数组
- 若freq_freq的长度为2，且freq.values()的最大值恰好是freq.values()的最小值的两倍，说明当前子数组恰好包含两种不同的频率，且较大的那一种是较小的两倍

若满足以上两个条件之一，说明当前子数组符合条件，此时使用index - start + 1更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def getLength(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        for start in range(len(nums)):
            freq = {}
            freq_freq = {}
            for index in range(start, len(nums)):
                v = nums[index]
                freq[v] = freq.get(v, 0) + 1
                if freq[v] == 1:
                    freq_freq[1] = freq_freq.get(1, 0) + 1
                else:
                    freq_freq[freq[v] - 1] -= 1
                    if freq_freq[freq[v] - 1] == 0:
                        freq_freq.pop(freq[v] - 1)
                    freq_freq[freq[v]] = freq_freq.get(freq[v], 0) + 1

                if len(freq) == 1 or (len(freq_freq) == 2 and max(freq.values()) == 2 * min(freq.values())):
                    res = max(res, index - start + 1)

        return res
```
