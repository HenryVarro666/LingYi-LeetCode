---
title: "3728. 边界与内部和相等的稳定子数组"
aliases: ["yiduobo的每日leetcode 3728.边界与内部和相等的稳定子数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1965859824517494173"
zhihu_id: "1965859824517494173"
zhihu_title: "yiduobo的每日leetcode 3728.边界与内部和相等的稳定子数组"
question_id: "3728"
question: "边界与内部和相等的稳定子数组"
problem_url: "https://leetcode.cn/problems/stable-subarrays-with-equal-boundary-and-interior-sum/"
difficulty: "Medium"
rating: 1909
created: "2025-10-28T19:46:54+08:00"
updated: "2025-10-28T19:46:54+08:00"
upvotes: 3
comments: 0
---

# 3728. 边界与内部和相等的稳定子数组

> **[yiduobo的每日leetcode 3728.边界与内部和相等的稳定子数组](https://zhuanlan.zhihu.com/p/1965859824517494173) · 知乎 · 2025-10-28 · 赞同 3**
> 力扣：[3728. 边界与内部和相等的稳定子数组](https://leetcode.cn/problems/stable-subarrays-with-equal-boundary-and-interior-sum/) · Medium · 灵茶山艾府：[前缀和与哈希表 + 式子变形（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3728.边界与内部和相等的稳定子数组

[3728. 边界与内部和相等的稳定子数组 - 力扣（LeetCode）](https://leetcode.cn/problems/stable-subarrays-with-equal-boundary-and-interior-sum/description/)

题目给出一个整数数组capacity。

若子数组中left到right这一段满足：

1、长度至少为3

2、首元素与尾元素都等于它们之间的所有元素的和，即capacity[left] \= capacity[right] \= capacity[left + 1] + capacity[left + 2] + ... + capacity[right - 1]

那么就称其为稳定子数组。

问capacity中稳定子数组的数目。

考察题目中关于稳定子数组的定义，发现有一段区间和的式子，那么自然是将其转化为前缀和之差。令s表示capacity的前缀和，那么上面的式子就可以写作capacity[left] \= capacity[right] \= s[right - 1] - s[left]。另一方面，s[right - 1]又可以认为是s[right] - capacity[right]，整理一下就有

capacity[left] \= capacity[right]

s[left] \= s[right] - capacity[right] - capacity[right]

也就是说，对于每个right，满足以上两个条件的left的个数就是以right为结尾的稳定子数组的数目。于是只需一趟遍历，使用哈希表cnt记录每种s和c的组合，对于当前遍历到的c，先更新对应的s，然后使用cnt[(s - c - c, c)]来更新答案，然后更新cnt[(s, c)]即可。

需要特别注意的是，上面的做法并没有考虑到长度至少为3这一条件，因此在遇到两个连续的0时会出现问题。此时通过前缀和之差计算s[left + 1]到s[right - 1]这一段的结果也同样是0，因此会将这两个0构成的子数组也算作稳定子数组。为了处理这种情况，可以使用一个变量pre记录每个元素的前一个元素，若遇到了两个连续的0，则将答案减去1。

最后附上python代码：

```python
class Solution(object):
    def countStableSubarrays(self, capacity):
        """
        :type capacity: List[int]
        :rtype: int
        """

        s = 0
        cnt = {}
        res = 0
        pre = None
        for c in capacity:
            s += c
            key = (s - c - c, c)
            res += cnt.get(key, 0)
            if c == 0 and pre == 0:
                res -= 1
            pre = c
            cnt[(s, c)] = cnt.get((s, c), 0) + 1
        
        return res
```
