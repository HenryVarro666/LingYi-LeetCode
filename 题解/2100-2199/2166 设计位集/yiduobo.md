---
title: "2166. 设计位集"
aliases: ["yiduobo的每日leetcode 2166.设计位集"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/design", "leetcode/string"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/533480375"
zhihu_id: "533480375"
zhihu_title: "yiduobo的每日leetcode 2166.设计位集"
question_id: "2166"
question: "设计位集"
problem_url: "https://leetcode.cn/problems/design-bitset/"
difficulty: "Medium"
created: "2022-06-25T00:05:59+08:00"
updated: "2022-06-25T00:05:59+08:00"
upvotes: 0
comments: 0
---

# 2166. 设计位集

> **[yiduobo的每日leetcode 2166.设计位集](https://zhuanlan.zhihu.com/p/533480375) · 知乎 · 2022-06-25 · 赞同 0**
> 力扣：[2166. 设计位集](https://leetcode.cn/problems/design-bitset/) · Medium · 灵茶山艾府：[懒标记法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2166.设计位集

[力扣](https://leetcode.cn/problems/design-bitset/)

题目要求设计一个简单的位集，支持给出的一系列操作。

既然是位集那肯定需要一个数组来储存每一位上的值，接下来逐个分析操作：

1）fix以及unfix，分别是将某位上的数变为1以及将某位上的数变为0，这个操作是很简单的

2）flip，翻转整个数组。这个操作的复杂度非常高，且没有调用次数限制，那么肯定是不能老老实实遍历数组翻转。具体实现的方法可以先看完后面的操作在决定

3）all、one、count，分别是判断位集中是否每一位都是1、是否存在至少一个1、位集中1的数目。对于这三个操作，只需要使用一个变量cnt记录当前位集中1的数目就都能满足了。cnt在fix、unfix、filp操作时都会变化，但是都可以在O(1)的时间内计算出变化后的cnt

4）toString，要求输出每一位上的情况。这个操作的执行次数不超过5次，那么完全可以每次请求的时候一趟遍历统计出答案就行了

回过头来再来考虑flip操作。由于flip操作是针对全局的，那么偶数次的flip操作就相当于没有flip，因此可以设置一个标记，表示当前是否flip过。但是需要的注意的是，在两次flip操作之间的fix以及unfix的效果是相反的，因此在执行fix和unfix操作时需要根据flip操作来进行适配。而对于cnt，在flip时是需要将cnt变为size - cnt就行了。

这样一来，除了最多执行5次的toString操作外，其他操作都可以在O(1)的时间内完成了。

最后附上python代码：

```python
class Bitset(object):

    def __init__(self, size):
        """
        :type size: int
        """
        self.size = size
        self.arr = [0] * size
        self.cnt = 0
        self.filp_flag = False

    def fix(self, idx):
        """
        :type idx: int
        :rtype: None
        """
        if self.filp_flag:
            target = 1
        else:
            target = 0

        if self.arr[idx] == target:
            self.arr[idx] = 1 - target
            self.cnt += 1

    def unfix(self, idx):
        """
        :type idx: int
        :rtype: None
        """
        if self.filp_flag:
            target = 0
        else:
            target = 1
        
        if self.arr[idx] == target:
            self.arr[idx] = 1 - target
            self.cnt -= 1

    def flip(self):
        """
        :rtype: None
        """
        self.filp_flag = not self.filp_flag
        self.cnt = self.size - self.cnt

    def all(self):
        """
        :rtype: bool
        """
        return self.cnt == self.size

    def one(self):
        """
        :rtype: bool
        """
        return self.cnt > 0

    def count(self):
        """
        :rtype: int
        """
        return self.cnt

    def toString(self):
        """
        :rtype: str
        """
        if self.filp_flag:
            return ''.join([str(1 - x) for x in self.arr])
        else:
            return ''.join([str(x) for x in self.arr])

# Your Bitset object will be instantiated and called as such:
# obj = Bitset(size)
# obj.fix(idx)
# obj.unfix(idx)
# obj.flip()
# param_4 = obj.all()
# param_5 = obj.one()
# param_6 = obj.count()
# param_7 = obj.toString()
```
