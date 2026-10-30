---
title: "3192. 使二进制数组全部等于1的最少操作次数II"
aliases: ["yiduobo的每日leetcode 3192.使二进制数组全部等于1的最少操作次数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/simulation", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706709763"
zhihu_id: "706709763"
zhihu_title: "yiduobo的每日leetcode 3192.使二进制数组全部等于1的最少操作次数II"
question_id: "3192"
question: "使二进制数组全部等于 1 的最少操作次数 II"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-ii/"
difficulty: "Medium"
rating: 1433
created: "2024-07-03T02:37:30+08:00"
updated: "2024-07-03T02:37:30+08:00"
upvotes: 1
comments: 0
---

# 3192. 使二进制数组全部等于1的最少操作次数II

> **[yiduobo的每日leetcode 3192.使二进制数组全部等于1的最少操作次数II](https://zhuanlan.zhihu.com/p/706709763) · 知乎 · 2024-07-03 · 赞同 1**
> 力扣：[3192. 使二进制数组全部等于 1 的最少操作次数 II](https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-ii/) · Medium · 灵茶山艾府：[两种方法：记录操作次数/比较相邻元素（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3192.使二进制数组全部等于1的最少操作次数II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-ii/)

题目给出一个二进制数组nums，每一轮操作可以从数组中任选一个下标i，将从i开始到数组末尾的所有元素都反转，问至少需要多少次操作才能让nums变为全1。

与上一题相同，对于某个下标i，以i为起点的操作至多只会执行一次，因为执行偶数次相当于什么都没有发生。另一方面，对于下标位置0，只有选择以0为起点的操作才能修改这个位置上的元素，在修改好下标0的元素后，由于以单个下标开始的操作至多只会执行一次，因此想要修改下标1的元素就只能以1为起点执行操作，同样的，对于后续的下标i，如果想修改下标i就只能以下标i为起点执行操作。

明确了修改的规则后，只需一趟遍历，若当前元素需要修改，那么就以当前下标为起点执行操作。当然，在这里不需要真的反转数组的后缀，而是只需要使用一个变量reverse记录当前后缀是否被翻转过。对于每个元素v，若v一开始为0且没有被反转过，即reverse也为0，或者v一开始为1，且被反转过，即reverse为1，那么此时就需要执行一次操作，具体实现上就是更新答案，同时将reverse取反。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        reverse = 0
        res = 0
        for v in nums:
            if v ^ reverse == 0:
                res += 1
                reverse ^= 1
        
        return res
```
