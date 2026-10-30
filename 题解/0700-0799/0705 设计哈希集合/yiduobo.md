---
title: "705. 设计哈希集合"
aliases: ["yiduobo的每日leetcode 705.设计哈希集合"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/322569545"
zhihu_id: "322569545"
zhihu_title: "yiduobo的每日leetcode 705.设计哈希集合"
question_id: "705"
question: "设计哈希集合"
problem_url: "https://leetcode.cn/problems/design-hashset/"
created: "2020-12-01T00:01:11+08:00"
updated: "2020-12-01T00:01:11+08:00"
upvotes: 0
comments: 0
---

# 705. 设计哈希集合

> **[yiduobo的每日leetcode 705.设计哈希集合](https://zhuanlan.zhihu.com/p/322569545) · 知乎 · 2020-12-01 · 赞同 0**
> 力扣：[705. 设计哈希集合](https://leetcode.cn/problems/design-hashset/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

705.设计哈希集合

[力扣](https://leetcode-cn.com/problems/design-hashset/)

设计哈希表的问题，经典做法有占坑法和链表法。注意到这里需要哈希的数字都在1到1000000之间，所以我选择了偷懒的做法，开一个1000001的数组初始化为false，用数组下标对应具体的数字。当新来一个数时，将该位置的元素置为true即可。

最后附上python代码：

```python
class MyHashSet(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.f = [False] * 1000001

    def add(self, key):
        """
        :type key: int
        :rtype: None
        """
        self.f[key] = True

    def remove(self, key):
        """
        :type key: int
        :rtype: None
        """
        self.f[key] = False

    def contains(self, key):
        """
        Returns true if this set contains the specified element
        :type key: int
        :rtype: bool
        """
        return self.f[key]

# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)
```
