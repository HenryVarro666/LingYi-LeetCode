---
title: "3434. 子数组操作后的最大频率"
aliases: ["yiduobo的每日leetcode 3434.子数组操作后的最大频率"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1890927742930907222"
zhihu_id: "1890927742930907222"
zhihu_title: "yiduobo的每日leetcode 3434.子数组操作后的最大频率"
question_id: "3434"
question: "子数组操作后的最大频率"
problem_url: "https://leetcode.cn/problems/maximum-frequency-after-subarray-operation/"
difficulty: "Medium"
rating: 2094
created: "2025-04-03T01:11:18+08:00"
updated: "2025-04-03T01:11:18+08:00"
upvotes: 0
comments: 0
---

# 3434. 子数组操作后的最大频率

> **[yiduobo的每日leetcode 3434.子数组操作后的最大频率](https://zhuanlan.zhihu.com/p/1890927742930907222) · 知乎 · 2025-04-03 · 赞同 0**
> 力扣：[3434. 子数组操作后的最大频率](https://leetcode.cn/problems/maximum-frequency-after-subarray-operation/) · Medium · 灵茶山艾府：[枚举 + 状态机 DP + O(n) 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3434.子数组操作后的最大频率

[3434. 子数组操作后的最大频率 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-frequency-after-subarray-operation/description/)

题目给出一个长度为n的数组nums，同时给出一个整数k。接下来可以选择nums中的某个子数组，然后将其中所有元素都增加x。

问操作后数组中k最多能出现多少次。

首先可以明确的是，对nums中的k做出修改是不优的，因此题目实际上是要找出一个子数组，其中出现次数最多的非k元素v的出现次数，减去子数组中k的出现次数最大，这个最大的差值加上原始nums中k出现的次数即为最终答案。

对于寻找找个子数组，则可以使用类似最大子段和的贪心法。使用数组cnt_k记录当前前缀中k的出现次数，另外使用哈希表cnt以及start分别记录每种非k的元素v在当前可用子段中出现的次数，以及当前可用子段的起点。

可用子段的起点这个说法比较含糊，可以换一种说法来进行描述：

对于指定的非k元素v，如果仅考虑将v修改成k，那么问题就可以转化为将nums中所有的v变为1，所有的k变为-1，其他的元素变为0，求数组中的最大子段和。

对于这个问题，可以一趟遍历，使用变量s记录当前子段之和。若某一时刻s小于等于0，就说明当前子段不应该出现在最终答案对应的子段中，无需再考虑了。此时则应该将s重新置为0，然后继续向后遍历。这样做也就相当于将子段的起点进行了重置。

而对于本题，由于需要在一趟遍历中对所有的非k元素v进行类似的操作，所以需要记录对每种v都记录当前考虑的子段的起点，也就是所谓的可用子段的起点，以及可用子段中v出现的次数cnt[v]。

那么对于当前遍历到的下标为index的元素v，若其不为k，则可以先将cnt\[v\]加上1。若cnt\[v\]等于1，或者cnt\[v\]小于等于当前可用子段中k出现的次数，也就是cnt\[v\]小于等于cnt_k\[-1\] - cnt_k\[start\[v\]\]，那么就说明当前可用子段中v的数量小于等于k，是不优的，因此需要对可用子段进行重置，将cnt\[v\]设置为1，并将start\[v\]设置为当前的index；反之，则可以用子段中v和k的数量之差，即cnt\[v\] - (cnt_k\[-1\] - cnt_k\[start\[v\]\])来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxFrequency(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        cnt = {}
        cnt_k = [0]
        start = {}
        res = 0

        for index, v in enumerate(nums):
            cnt_k.append(cnt_k[-1])
            if v == k:
                cnt_k[-1] += 1
            else:
                cnt[v] = cnt.get(v, 0) + 1
                if cnt[v] == 1 or cnt_k[-1] - cnt_k[start[v]] >= cnt[v]:
                    cnt[v] = 1
                    start[v] = index
                
                res = max(res, cnt[v] - (cnt_k[-1] - cnt_k[start[v]]))

        return res + cnt_k[-1]
```
