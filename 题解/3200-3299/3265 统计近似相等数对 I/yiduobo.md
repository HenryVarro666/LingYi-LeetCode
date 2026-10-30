---
title: "3265. 统计近似相等数对I"
aliases: ["yiduobo的每日leetcode 3265.统计近似相等数对I"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration", "leetcode/sorting", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/747778517"
zhihu_id: "747778517"
zhihu_title: "yiduobo的每日leetcode 3265.统计近似相等数对I"
question_id: "3265"
question: "统计近似相等数对 I"
problem_url: "https://leetcode.cn/problems/count-almost-equal-pairs-i/"
difficulty: "Medium"
created: "2024-09-29T02:22:19+08:00"
updated: "2024-09-29T02:22:19+08:00"
upvotes: 1
comments: 0
---

# 3265. 统计近似相等数对I

> **[yiduobo的每日leetcode 3265.统计近似相等数对I](https://zhuanlan.zhihu.com/p/747778517) · 知乎 · 2024-09-29 · 赞同 1**
> 力扣：[3265. 统计近似相等数对 I](https://leetcode.cn/problems/count-almost-equal-pairs-i/) · Medium · 灵茶山艾府：[排序+枚举右维护左+暴力交换（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3265.统计近似相等数对I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-almost-equal-pairs-i/description/)

题目给出一个正整数数组nums，对于其中的两个元素x和y，可以执行一次操作，交换x中任意两个数位上的数，或者交换y中任意两个数位上的数。若执行完操作后x和y相等，那么在这里就称x和y近似相等。需要注意的是，这里的操作允许出现前导0，例如300和3，对300执行操作后可以得到003，此时与3相等。

现在问数组nums中存在多少个下标对i、j满足i \< j且nums[i]与nums[j]近似相等。

对于这类找数对的问题，一种经典的处理方法就是一趟遍历，遍历的过程中一边使用哈希表记录已经遍历过的元素可以形成的所有状态，一边利用哈希表计算当前遍历到的元素在哈希表中能形成多少配对，然后将当前元素处理后也加入到哈希表中。

对于本题，则可以使用哈希表freq记录已经遍历过的元素经过一次操作后可以得到的每种新元素出现的次数，那么对于当前遍历到的元素x，freq[x]就是其左侧元素中经过操作后可以变为x的元素数目，使用freq[x]更新答案，然后计算x操作后可以得到的新元素并更新freq即可。

在这里需要注意的是，上面的处理方法只计算了x左侧元素进行操作后与x配对的情况，没有计算x进行操作后与x左侧元素进行配对的情况。

在这里不妨先对交换后相等的情况进行讨论。注意到题目强调了操作后可以出现前导0，那么可以根据是否出现了前导0进行讨论：

1、若没有前导0：

说明x和y的数位一定相同。此时交换x中的两个下标x[i]与x[j]后得到y，等价于交换y中的两个下标y[i]与y[j]得到x。也就是说这种情况下如果对x进行操作后可以匹配到y，那么对y进行操作后也一定可以匹配到x。

2、若存在前导0：

此时只有对数位较长的那个元素进行操作，去匹配数位较短的那个元素

也就是说，只要按照元素从大到小的顺序遍历nums执行上面的算法，就一定不会出现x左侧元素操作后无法匹配x，但是x操作后可以匹配左侧元素的情况。

另外对于操作的具体执行，注意到数组中元素的大小优先，也就是说位数比较少，那么只需暴力枚举交换的下标i、j，计算交换后的结果就行了。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort(reverse=True)

        res = 0
        freq = {}

        for v in nums:
            res += freq.get(v, 0)
            digits = list(str(v))
            new_v_set = set([v])
            for i in range(len(digits) - 1):
                for j in range(i + 1, len(digits)):
                    digits[i], digits[j] = digits[j], digits[i]
                    new_v_set.add(int(''.join(digits)))
                    digits[i], digits[j] = digits[j], digits[i]
            
            for new_v in new_v_set:
                freq[new_v] = freq.get(new_v, 0) + 1
        
        return res
```
