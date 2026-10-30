---
title: "381. O(1)时间插入、删除和获取随机元素-允许重复"
aliases: ["yiduobo的每日leetcode 381.O(1)时间插入、删除和获取随机元素-允许重复"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166408330"
zhihu_id: "166408330"
zhihu_title: "yiduobo的每日leetcode 381.O(1)时间插入、删除和获取随机元素-允许重复"
question_id: "381"
question: "O(1)时间插入、删除和获取随机元素-允许重复"
problem_url: "https://leetcode.cn/problems/insert-delete-getrandom-o1-duplicates-allowed/"
created: "2020-08-03T20:44:28+08:00"
updated: "2020-08-03T20:44:28+08:00"
upvotes: 0
comments: 0
---

# 381. O(1)时间插入、删除和获取随机元素-允许重复

> **[yiduobo的每日leetcode 381.O(1)时间插入、删除和获取随机元素-允许重复](https://zhuanlan.zhihu.com/p/166408330) · 知乎 · 2020-08-03 · 赞同 0**
> 力扣：[381. O(1)时间插入、删除和获取随机元素-允许重复](https://leetcode.cn/problems/insert-delete-getrandom-o1-duplicates-allowed/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

381.O(1)时间插入、删除和获取随机元素-允许重复<https://leetcode-cn.com/problems/insert-delete-getrandom-o1-duplicates-allowed/>

上一题的升级版（传送门在这里：[yiduobo：yiduobo的每日leetcode 380.常数时间插入、删除和获取随机元素](https://zhuanlan.zhihu.com/p/166195203)），不过这里有重复元素出现，那么之前使用dict储存元素在list中位置的操作就需要变成dict不直接储存元素在list中的位置，而是储存一个set，通过这个set储存元素在list中的位置。其他的各项操作则是与上一题保持一致。

最后附上python代码：

```python
import random

class RandomizedCollection(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.pos_dict = {}
        self.num_list = []

    def insert(self, val):
        """
        Inserts a value to the collection. Returns true if the collection did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        ret = False
        if val not in self.pos_dict:
            ret = True
            self.pos_dict[val] = set()

        self.pos_dict[val].add(len(self.num_list))
        self.num_list.append(val)
        return ret

    def remove(self, val):
        """
        Removes a value from the collection. Returns true if the collection contained the specified element.
        :type val: int
        :rtype: bool
        """
        if val not in self.pos_dict:
            return False

        val_pos = self.pos_dict[val].pop()
        tmp = self.num_list[-1]
        self.num_list[val_pos] = tmp
        self.pos_dict[tmp].add(val_pos)
        self.pos_dict[tmp].remove(len(self.num_list) - 1)
        if not self.pos_dict[val]:
            self.pos_dict.pop(val)
        self.num_list.pop()

        return True

    def getRandom(self):
        """
        Get a random element from the collection.
        :rtype: int
        """
        return self.num_list[random.randint(0, len(self.num_list) - 1)]

# Your RandomizedCollection object will be instantiated and called as such:
# obj = RandomizedCollection()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
```
