---
title: "3041. 修改数组后最大化数组中的连续元素数目"
aliases: ["yiduobo的每日leetcode 3041.修改数组后最大化数组中的连续元素数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695943668"
zhihu_id: "695943668"
zhihu_title: "yiduobo的每日leetcode 3041.修改数组后最大化数组中的连续元素数目"
question_id: "3041"
question: "修改数组后最大化数组中的连续元素数目"
problem_url: "https://leetcode.cn/problems/maximize-consecutive-elements-in-an-array-after-modification/"
difficulty: "Hard"
rating: 2231
created: "2024-05-04T23:23:48+08:00"
updated: "2024-05-04T23:23:48+08:00"
upvotes: 1
comments: 0
---

# 3041. 修改数组后最大化数组中的连续元素数目

> **[yiduobo的每日leetcode 3041.修改数组后最大化数组中的连续元素数目](https://zhuanlan.zhihu.com/p/695943668) · 知乎 · 2024-05-04 · 赞同 1**
> 力扣：[3041. 修改数组后最大化数组中的连续元素数目](https://leetcode.cn/problems/maximize-consecutive-elements-in-an-array-after-modification/) · Hard · 灵茶山艾府：[本题最简单写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3041.修改数组后最大化数组中的连续元素数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-consecutive-elements-in-an-array-after-modification/description/)

题目的数据规模较大，但是注意到数值的取值范围在10^6之内，因此可以考虑使用f[x]表示以x结尾的最大连续数组长度。

接下来对于数组中的某个数v，若v仅出现了一次，那么就需要考虑是否修改v，即可以尝试将v放在f[v - 1]的末尾形成以v结尾的连续数组，也可以考虑将v修改成v + 1放在f[v]的末尾；反之，若v出现了大于等于两次，那么除了上面的两种操作，在这里还可以在f[v - 1]的末尾加入v和修改后的v + 1直接形成以v + 1结尾的连续数组。

于是只需统计数组中每个数出现的次数，然后从小到大一趟遍历。对于当前遍历到的v，若其出现次数cnt为1，那么就需要先用f[v] +1来更新f[v + 1]，然后用f[v - 1] + 1来更新f[v]；反之，则可以先用f[v - 1] + 1来更新f[v]，然后再用f[v]来更新f[v + 1]，即隐式地包含了使用f[v - 1] + 2来更新f[v + 1]。

最后附上python代码：

```python
class Solution(object):
    def maxSelectedElements(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        freq = Counter(nums)
        ma = max(freq.keys())
        f = [0] * (ma + 2)

        for v, cnt in sorted(freq.items()):
            if cnt == 1:
                f[v + 1] = f[v] + 1
                f[v] = f[v - 1] + 1
            else:
                f[v] = f[v - 1] + 1
                f[v + 1] = f[v] + 1

        return max(f)
```
