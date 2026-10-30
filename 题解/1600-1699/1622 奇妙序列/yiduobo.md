---
title: "1622. 奇妙序列"
aliases: ["yiduobo的每日leetcode 1622.奇妙序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/number-theory", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/八-树状数组和线段树", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/436475529"
zhihu_id: "436475529"
zhihu_title: "yiduobo的每日leetcode 1622.奇妙序列"
question_id: "1622"
question: "奇妙序列"
problem_url: "https://leetcode.cn/problems/fancy-sequence/"
difficulty: "Hard"
rating: 2476
created: "2021-11-22T23:22:46+08:00"
updated: "2021-11-22T23:22:46+08:00"
upvotes: 0
comments: 0
---

# 1622. 奇妙序列

> **[yiduobo的每日leetcode 1622.奇妙序列](https://zhuanlan.zhihu.com/p/436475529) · 知乎 · 2021-11-22 · 赞同 0**
> 力扣：[1622. 奇妙序列](https://leetcode.cn/problems/fancy-sequence/) · Hard · 灵茶山艾府：[懒更新 + 等价转化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1622.奇妙序列

[力扣](https://leetcode-cn.com/problems/fancy-sequence/)

对于一个getIndex操作而言，无论之前经历过什么样的操作，最后都可以将答案写成multi \* x + add的形式，其中x为index位置上的数，而multi和add则是通过前面这些操作计算出来的。

由于数据规模的关系，自然是不可能对每个位置都一直计算出其对应的multi和add，那么当一个getIndex操作出现时，就需要想办法高效地计算出index这个位置对应的multi和add了。

注意到每一个multiAll和addAll操作影响的都是序列的前缀，换言之就是一个连续区间的multi和add产生了变化，因此在这里可以使用线段树来进行求解。

除此之外，回想一下树状数组，一般的树状数组是操作完x这个位置后会对大于等于x的所有位置产生影响，而本题则是操作完x这个位置之后会对小于等于x的所有位置产生影响，那么一个自然的想法就是直接倒过来存储序列。由于这里append操作的上限为100000，那么可以直接开一个大小为100000的数组，然后从后向前填充。当填充的长度为k时，此时的multiAll和addAll操作影响的就是100000 - k + 1到100000这一段区间上的数，此时直接使用树状数组维护multi和add即可。比起线段树树状数组还是容易写一点，因此我采用的是这种做法。

最后附上python代码：

```python
class Fancy(object):

    def __init__(self):
        self.full_size = 100000
        self.index_m = [1] * (self.full_size + 1)
        self.index_a = [0] * (self.full_size + 1)
        self.nums = []
        self.mod = 10 ** 9 + 7

    def append(self, val):
        """
        :type val: int
        :rtype: None
        """
        self.nums.append(val)

    def addAll(self, inc):
        """
        :type inc: int
        :rtype: None
        """
        index = self.full_size - len(self.nums) + 1
        while index <= self.full_size:
            self.index_a[index] += inc
            self.index_a[index] %= self.mod
            index += index & -index

    def multAll(self, m):
        """
        :type m: int
        :rtype: None
        """
        index = self.full_size - len(self.nums) + 1
        while index <= self.full_size:
            self.index_m[index] *= m
            self.index_m[index] %= self.mod
            self.index_a[index] *= m
            self.index_a[index] %= self.mod
            index += index & -index

    def getIndex(self, idx):
        """
        :type idx: int
        :rtype: int
        """
        idx += 1
        if idx > len(self.nums):
            return -1
        
        index = self.full_size - idx + 1
        m = 1
        a = 0
        while index > 0:
            m *= self.index_m[index]
            m %= self.mod
            a = a * self.index_m[index] + self.index_a[index]
            a %= self.mod
            index -= index & -index
        
        return (self.nums[idx - 1] * m + a) % self.mod

# Your Fancy object will be instantiated and called as such:
# obj = Fancy()
# obj.append(val)
# obj.addAll(inc)
# obj.multAll(m)
# param_4 = obj.getIndex(idx)
```
