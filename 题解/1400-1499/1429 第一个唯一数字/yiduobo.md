---
title: "1429. 第一个唯一数字"
aliases: ["yiduobo的每日leetcode 1429.第一个唯一数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/616541876"
zhihu_id: "616541876"
zhihu_title: "yiduobo的每日leetcode 1429.第一个唯一数字"
question_id: "1429"
question: "第一个唯一数字"
problem_url: "https://leetcode.cn/problems/first-unique-number/"
created: "2023-03-24T00:36:24+08:00"
updated: "2023-03-24T00:36:24+08:00"
upvotes: 0
comments: 0
---

# 1429. 第一个唯一数字

> **[yiduobo的每日leetcode 1429.第一个唯一数字](https://zhuanlan.zhihu.com/p/616541876) · 知乎 · 2023-03-24 · 赞同 0**
> 力扣：[1429. 第一个唯一数字](https://leetcode.cn/problems/first-unique-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1429.第一个唯一数字

[力扣](https://leetcode.cn/problems/first-unique-number/)

使用一个数组储存这些数字，同时使用一个哈希表储存每个数字出现的次数。

对于add操作，只需更新这个数组以及哈希表，而对于查询操作，由于题目中不存在删除操作，因此每一次查询操作的答案只会出现在上一次查询的答案之后，于是可以使用一个变量p指向当前查询的答案在数组中出现的下标，那么对于每一次查询操作就可以在上一轮答案的基础上，根据哈希表中该数字出现的次数来确定当前这一次查询的答案。

最后附上python代码：

```python
class FirstUnique(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.p = 0
        self.q = []
        self.cnt = {}

        for num in nums:
            self.add(num)

    def showFirstUnique(self):
        """
        :rtype: int
        """
        while self.p < len(self.q) and self.cnt[self.q[self.p]] > 1:
            self.p += 1
        
        if self.p == len(self.q):
            return -1
        
        return self.q[self.p]

    def add(self, value):
        """
        :type value: int
        :rtype: None
        """
        if value not in self.cnt:
            self.q.append(value)
        
        self.cnt[value] = self.cnt.get(value, 0) + 1

# Your FirstUnique object will be instantiated and called as such:
# obj = FirstUnique(nums)
# param_1 = obj.showFirstUnique()
# obj.add(value)
```
