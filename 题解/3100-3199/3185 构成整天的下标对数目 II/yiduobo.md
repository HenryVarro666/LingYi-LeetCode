---
title: "3184. 构成整天的下标对数目I & 3185. 构成整天的下标对数目II"
aliases: ["yiduobo的每日leetcode 3184.构成整天的下标对数目I && 3185.构成整天的下标对数目II", "3184. 构成整天的下标对数目I", "3185. 构成整天的下标对数目II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/array", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/零-常用枚举技巧"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/706188670"
zhihu_id: "706188670"
zhihu_title: "yiduobo的每日leetcode 3184.构成整天的下标对数目I && 3185.构成整天的下标对数目II"
question_id: ["3184", "3185"]
question: ["构成整天的下标对数目 I", "构成整天的下标对数目 II"]
problem_url: ["https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-i/", "https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-ii/"]
difficulty: ["Easy", "Medium"]
rating: 1010
created: "2024-06-30T00:33:47+08:00"
updated: "2024-06-30T00:33:47+08:00"
upvotes: 0
comments: 0
---

# 3184. 构成整天的下标对数目I & 3185. 构成整天的下标对数目II

> **[yiduobo的每日leetcode 3184.构成整天的下标对数目I && 3185.构成整天的下标对数目II](https://zhuanlan.zhihu.com/p/706188670) · 知乎 · 2024-06-30 · 赞同 0**
> 力扣：[3184. 构成整天的下标对数目 I](https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-i/) · Easy · 灵茶山艾府：[枚举右，维护左，O(n) 一次遍历（Python/Java/C++/C/Go/JS/Rust）](../3184%20构成整天的下标对数目%20I/灵茶山艾府.md)
> 力扣：[3185. 构成整天的下标对数目 II](https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-ii/) · Medium · 灵茶山艾府：[枚举右，维护左，O(n) 一次遍历（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3184.构成整天的下标对数目I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-i/description/)

3185.构成整天的下标对数目II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-ii/description/)

题目给出一个整数数组hours，要求找出其中满足i \< j且hours[i] + hours[j]之和构成整天的下标对(i, j)的总数，这里的整体指的是24的倍数。

两题的题设一致，第二题的数据规模较大。

由于题目要求找出和为24的倍数的下标对，那么在这里就可以先将hours中的所有元素对24取模。接下来对于其中的某个元素v，若v等于0，那么就需要找到另一个0与之配对，否则需要找到24 - v与之配对。

于是可以使用一个哈希表freq记录已经出现过的时间的频率，然后一趟遍历，对于当前遍历到的v，若v等于0，那么就将freq[v]累加到答案中，否则将freq[24 - v]累加到答案中。无论是哪种情况，接下来都需要将freq[v]加上1，然后继续向后遍历。

最后附上python代码：

```python
class Solution(object):
    def countCompleteDayPairs(self, hours):
        """
        :type hours: List[int]
        :rtype: int
        """

        freq = Counter()
        res = 0
        for h in hours:
            v = h % 24
            if v == 0:
                res += freq[v]
            else:
                res += freq[24 - v]

            freq[v] += 1

        return res
```
