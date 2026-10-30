---
title: "1338. 数组大小减半"
aliases: ["yiduobo的每日leetcode 1338.数组大小减半"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/array", "leetcode/hash-table", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/396046213"
zhihu_id: "396046213"
zhihu_title: "yiduobo的每日leetcode 1338.数组大小减半"
question_id: "1338"
question: "数组大小减半"
problem_url: "https://leetcode.cn/problems/reduce-array-size-to-the-half/"
difficulty: "Medium"
rating: 1303
created: "2021-08-03T22:34:05+08:00"
updated: "2021-08-03T22:34:05+08:00"
upvotes: 1
comments: 0
---

# 1338. 数组大小减半

> **[yiduobo的每日leetcode 1338.数组大小减半](https://zhuanlan.zhihu.com/p/396046213) · 知乎 · 2021-08-03 · 赞同 1**
> 力扣：[1338. 数组大小减半](https://leetcode.cn/problems/reduce-array-size-to-the-half/) · Medium · 灵茶山艾府：[计数+从大到小贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1338.数组大小减半

[力扣](https://leetcode-cn.com/problems/reduce-array-size-to-the-half/)

题目只需要删除超过一半的数，并没有要求恰好删去一半的数，因此我们应该先从出现次数较多的数开始进行删去。

首先统计出每个数出现的次数，然后按次数从大到小进行排序。接下来一趟扫描，计算次数的前缀和，当某一时刻前缀和大于总数的一半时，对应的下标加1即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minSetSize(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        cnt_dict = {}
        for num in arr:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        now = 0
        for index, cnt in enumerate(sorted(cnt_dict.values(), reverse=True)):
            now += cnt
            if now + now >= len(arr):
                return index + 1
```
