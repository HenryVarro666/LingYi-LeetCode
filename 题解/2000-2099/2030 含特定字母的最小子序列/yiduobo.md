---
title: "2030. 含特定字母的最小子序列"
aliases: ["yiduobo的每日leetcode 2030.含特定字母的最小子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/monotonic-queue", "题单/单调栈", "题单/单调栈/四-最小字典序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/508257590"
zhihu_id: "508257590"
zhihu_title: "yiduobo的每日leetcode 2030.含特定字母的最小子序列"
question_id: "2030"
question: "含特定字母的最小子序列"
problem_url: "https://leetcode.cn/problems/smallest-k-length-subsequence-with-occurrences-of-a-letter/"
difficulty: "Hard"
rating: 2562
created: "2022-05-02T00:04:52+08:00"
updated: "2022-05-02T00:04:52+08:00"
upvotes: 0
comments: 0
---

# 2030. 含特定字母的最小子序列

> **[yiduobo的每日leetcode 2030.含特定字母的最小子序列](https://zhuanlan.zhihu.com/p/508257590) · 知乎 · 2022-05-02 · 赞同 0**
> 力扣：[2030. 含特定字母的最小子序列](https://leetcode.cn/problems/smallest-k-length-subsequence-with-occurrences-of-a-letter/) · Hard · 灵茶山艾府：[Go 单调队列](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2030.含特定字母的最小子序列

[力扣](https://leetcode-cn.com/problems/smallest-k-length-subsequence-with-occurrences-of-a-letter/)

为了使得最终答案的字典序最小，那么就应该尽可能将小的字符放在答案的前面。不妨先来考虑首字符的选择。

对于答案的首字母，其选择的范围将受到几个限制：

1、选择了首字母外后续还需要选择k - 1个字母，因此只能从0到n - k这个范围内选择首字母

2、选择了首字母后，由于不一定选择了letter，因此还需要保证后续至少存在repetition个letter。一趟遍历，使用一个数组pos_list记录每个letter出现的位置。在选择了首字母后要保证后续还有repetition个letter，那么首字母选择的范围不能超过pos_list[p]，其中pos_list[p]后续还有repetition - 1个letter，因此可以计算得到p \= len(pos_list) - repetition

综合上面两点，就是首字母的选择范围在0到bound \= min(n - k, pos_list[p])之间。

除此之外，还有一个限制是由于最终答案的长度限定为k，其中又需要存在repetition个letter，因此留给其他字符的位置至多只有other \= k - repetition。那么在选择时，如果other已经为0就不能再选择letter之外的字符了。

那么对于首字母的选择，就可以使用一个堆维护0到bound直接的字符，相同字符再按下标小的在前面。不断弹出堆顶的字符，直到其满足other这个条件。

在选好了首字符之后，第二个字符的选择范围产生了一些变化：

1、首字母左侧的所有字符都不再可用。当然在这里没必要立即将这些字符从堆中移除，只需要等该字符作为最小值弹出时再判断其下标是否已经失效即可

2、剩下需要预留的位置少了1，因此bound中的n - k这一项需要向后移动1位。若此时的答案长度为len(res)，剩下需要预留的位置就是k - len(res)个，因此此时可以选择0到n - k + len(res)中的字符

3、若当前选择的是letter，那么后续需要预留给letter的次数也减少了1，因此pos_list[p]这一项会向后移动到pos_list[p + 1]

综合2和3，可以发现新的边界new_bound \= (n - k + len(res), pos_list[p + 1])，那么此时应该将bound + 1到new_bound之间的所有字符也加入到堆中备选。

对于后续的所有字符，只需重复上面的过程，直到选出完整的答案为止。

最后附上python代码：

```python
class Solution(object):
    def smallestSubsequence(self, s, k, letter, repetition):
        """
        :type s: str
        :type k: int
        :type letter: str
        :type repetition: int
        :rtype: str
        """

        pos_list = []
        n = len(s)
        for index, char in enumerate(s):
            if char == letter:
                pos_list.append(index)

        p = len(pos_list) - repetition
        heap = []
        n = len(s)
        bound = min(pos_list[p], n - k)
        for index in range(bound + 1):
            heapq.heappush(heap, (s[index], index))

        res = []
        other = k - repetition
        while len(res) < k:
            char, index = heapq.heappop(heap)
            if len(res) > 0 and index < res[-1]:
                continue
            if char != letter:
                if other == 0:
                    continue
                other -= 1
                res.append(index)
            else:
                res.append(index)
                if p < len(pos_list):
                    p += 1

            if len(res) == k:
                break

            next_bound = n - (k - len(res))
            if p < len(pos_list):
                next_bound = min(next_bound, pos_list[p])

            for index in range(bound + 1, next_bound + 1):
                heapq.heappush(heap, (s[index], index))
            bound = next_bound
        
        return ''.join([s[index] for index in res])
```
