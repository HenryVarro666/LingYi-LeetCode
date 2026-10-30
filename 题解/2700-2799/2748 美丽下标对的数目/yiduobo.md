---
title: "2748. 美丽下标对的数目"
aliases: ["yiduobo的每日leetcode 2748.美丽下标对的数目"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/number-theory", "题单/常用数据结构", "题单/数学算法", "题单/常用数据结构/零-常用枚举技巧", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653981204"
zhihu_id: "653981204"
zhihu_title: "yiduobo的每日leetcode 2748.美丽下标对的数目"
question_id: "2748"
question: "美丽下标对的数目"
problem_url: "https://leetcode.cn/problems/number-of-beautiful-pairs/"
difficulty: "Easy"
rating: 1301
created: "2023-09-03T02:49:22+08:00"
updated: "2023-09-03T02:49:22+08:00"
upvotes: 0
comments: 0
---

# 2748. 美丽下标对的数目

> **[yiduobo的每日leetcode 2748.美丽下标对的数目](https://zhuanlan.zhihu.com/p/653981204) · 知乎 · 2023-09-03 · 赞同 0**
> 力扣：[2748. 美丽下标对的数目](https://leetcode.cn/problems/number-of-beautiful-pairs/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2748.美丽下标对的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/number-of-beautiful-pairs/)

题目考虑的是单个数位上的互质关系，因此可以先将与所有个位数的互质的个位数打表方便使用。

接下来遍历数组，同时使用一个哈希表记录已遍历过的数中所有最高位出现的次数，那么对于当前遍历到的数v，计算v的个位数，然后枚举与其互质的数，再通过哈希表更新答案，最后再将v的最高位数在哈希表中的计数加上1即可。

最后附上python代码：

```python
class Solution(object):
    def countBeautifulPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        check_digit = {1: [1, 2, 3, 4, 5, 6, 7, 8, 9],
                       2: [1, 3, 5, 7, 9],
                       3: [1, 2, 4, 5, 7, 8],
                       4: [1, 3, 5, 7, 9],
                       5: [1, 2, 3, 4, 6, 7, 8, 9],
                       6: [1, 5, 7],
                       7: [1, 2, 3, 4, 5, 6, 8, 9],
                       8: [1, 3, 5, 7, 9],
                       9: [1, 2, 4, 5, 7, 8]}

        cnt = [0] * 10
        res = 0
        for v in nums:
            last = v % 10
            for first in check_digit[last]:
                res += cnt[first]
            
            while v:
                first = v % 10
                v /= 10
            
            cnt[first] += 1
        
        return res
```
