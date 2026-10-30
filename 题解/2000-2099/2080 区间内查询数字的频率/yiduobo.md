---
title: "2080. 区间内查询数字的频率"
aliases: ["yiduobo的每日leetcode 2080.区间内查询数字的频率"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/一-二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/518027991"
zhihu_id: "518027991"
zhihu_title: "yiduobo的每日leetcode 2080.区间内查询数字的频率"
question_id: "2080"
question: "区间内查询数字的频率"
problem_url: "https://leetcode.cn/problems/range-frequency-queries/"
difficulty: "Medium"
rating: 1702
created: "2022-05-21T23:44:35+08:00"
updated: "2022-05-21T23:44:35+08:00"
upvotes: 0
comments: 0
---

# 2080. 区间内查询数字的频率

> **[yiduobo的每日leetcode 2080.区间内查询数字的频率](https://zhuanlan.zhihu.com/p/518027991) · 知乎 · 2022-05-21 · 赞同 0**
> 力扣：[2080. 区间内查询数字的频率](https://leetcode.cn/problems/range-frequency-queries/) · Medium · 灵茶山艾府：[简洁写法：统计位置+二分查找（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2080.区间内查询数字的频率

[力扣](https://leetcode.cn/problems/range-frequency-queries/)

题目要求找出静态区间中某个特定数字出现的次数，对于这个问题，一个自然的想法就是将区间问题转化为前缀问题，对于询问(l, r, value)，将其分解成区间[0, r]之间value的数量减去区间[0, l - 1]之间value的数量。

如果value的取值范围比较小，那么可以使用哈希表将所有前缀的每种数字出现次数都统计出来。事实上，对于一般由字符串构成的类似问题通常就是这么做的，之前应该碰到过好几题类似的问题了。不过在这里value的取值范围太大，时空复杂度可能都有问题，于是在这里可以采用一种折中的方式。

使用哈希表num_dict记录每个数字出现的所有位置，接下来对于询问(l, r, value)，num_dict[value]就是value出现过的所有位置，那么num_dict[value]中小于等于l - 1的数有多少个，区间[0, l - 1]中value的数量就有多少个。同样的，num_dict[value]中小于等于r的数有多少个，区间[0, r]中value的数量就有多少个。

到了这里，很容易想到在记录每个数字出现的所有位置后将这些位置从小到大进行排序，那么就可以利用二分来求解上面这两个子问题，从而在logn的时间内求出一组询问的解。

最后附上python代码：

```python
class RangeFreqQuery(object):

    def __init__(self, arr):
        """
        :type arr: List[int]
        """
        self.num_dict = {}
        for index, num in enumerate(arr):
            if num not in self.num_dict:
                self.num_dict[num] = []
            self.num_dict[num].append(index)
        
        for num in self.num_dict:
            self.num_dict[num] = sorted(self.num_dict[num])

    def binary_search(self, value, pos):
        if value not in self.num_dict or pos < self.num_dict[value][0]:
            return 0
        
        l = 0
        r = len(self.num_dict[value]) - 1
        while l < r:
            mid = (l + r + 1) >> 1
            if self.num_dict[value][mid] <= pos:
                l = mid
            else:
                r = mid - 1

        return l + 1

    def query(self, left, right, value):
        """
        :type left: int
        :type right: int
        :type value: int
        :rtype: int
        """

        return self.binary_search(value, right) - self.binary_search(value, left - 1)

# Your RangeFreqQuery object will be instantiated and called as such:
# obj = RangeFreqQuery(arr)
# param_1 = obj.query(left,right,value)
```
