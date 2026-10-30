---
title: "380. 常数时间插入、删除和获取随机元素"
aliases: ["yiduobo的每日leetcode 380.常数时间插入、删除和获取随机元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/166195203"
zhihu_id: "166195203"
zhihu_title: "yiduobo的每日leetcode 380.常数时间插入、删除和获取随机元素"
question_id: "380"
question: "常数时间插入、删除和获取随机元素"
problem_url: "https://leetcode.cn/problems/insert-delete-getrandom-o1/"
created: "2020-08-02T23:48:44+08:00"
updated: "2020-08-02T23:48:44+08:00"
upvotes: 0
comments: 0
---

# 380. 常数时间插入、删除和获取随机元素

> **[yiduobo的每日leetcode 380.常数时间插入、删除和获取随机元素](https://zhuanlan.zhihu.com/p/166195203) · 知乎 · 2020-08-02 · 赞同 0**
> 力扣：[380. 常数时间插入、删除和获取随机元素](https://leetcode.cn/problems/insert-delete-getrandom-o1/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

380.常数时间插入、删除和获取随机元素<https://leetcode-cn.com/problems/insert-delete-getrandom-o1/>

对于常数时间内插入和删除的要求，自然是想到使用哈希表来完成任务，可以使用dict或者set。

而对于获取随机元素的要求，则是需要某种线性的结构，于是想到了list。

到了这里，自然就想到使用dict来保存每个数在list中的位置。

于是：

1、对于插入操作，将插入的元素添加到list的末尾，同时使用dict保存对应的位置。

2、对于删除操作，将待删除的元素与list的末尾进行交换，同时更新原始某尾元素在dict中的值，并截取掉list的末尾。

3、对于随机取操作，使用randint获取0到len - 1中的某个数，然后返回list对应下标的元素。

最后附上python代码：

```python
import random

class RandomizedSet(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.num_dict = {}
        self.num_list = []

    def insert(self, val):
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        if val in self.num_dict:
            return False

        self.num_dict[val] = len(self.num_list)
        self.num_list.append(val)
        return True

    def remove(self, val):
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        :type val: int
        :rtype: bool
        """
        if val not in self.num_dict:
            return False
        tmp = self.num_list[-1]
        self.num_dict[tmp] = self.num_dict[val]
        self.num_list[self.num_dict[val]] = tmp
        self.num_dict.pop(val)
        self.num_list.pop()
        return True

    def getRandom(self):
        """
        Get a random element from the set.
        :rtype: int
        """
        return self.num_list[random.randint(0, len(self.num_list) - 1)]

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
```
