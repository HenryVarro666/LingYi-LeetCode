---
title: "706. 设计哈希映射"
aliases: ["yiduobo的每日leetcode 706.设计哈希映射"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/322594936"
zhihu_id: "322594936"
zhihu_title: "yiduobo的每日leetcode 706.设计哈希映射"
question_id: "706"
question: "设计哈希映射"
problem_url: "https://leetcode.cn/problems/design-hashmap/"
created: "2020-12-01T00:03:06+08:00"
updated: "2020-12-01T00:03:06+08:00"
upvotes: 0
comments: 0
---

# 706. 设计哈希映射

> **[yiduobo的每日leetcode 706.设计哈希映射](https://zhuanlan.zhihu.com/p/322594936) · 知乎 · 2020-12-01 · 赞同 0**
> 力扣：[706. 设计哈希映射](https://leetcode.cn/problems/design-hashmap/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

706.设计哈希映射

[力扣](https://leetcode-cn.com/problems/design-hashmap/)

与上一题类似，我在这里也是开了一个1000001的数组，用来保存下标到具体数值的映射，初始化为-1。当新来一个数时，将数组对应的元素置为这个数即可。

最后附上python代码：

```python
class MyHashMap(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.f = [-1] * 1000001

    def put(self, key, value):
        """
        value will always be non-negative.
        :type key: int
        :type value: int
        :rtype: None
        """
        self.f[key] = value

    def get(self, key):
        """
        Returns the value to which the specified key is mapped, or -1 if this map contains no mapping for the key
        :type key: int
        :rtype: int
        """
        return self.f[key]

    def remove(self, key):
        """
        Removes the mapping of the specified value key if this map contains a mapping for the key
        :type key: int
        :rtype: None
        """
        self.f[key] = -1

# Your MyHashMap object will be instantiated and called as such:
# obj = MyHashMap()
# obj.put(key,value)
# param_2 = obj.get(key)
# obj.remove(key)
```
