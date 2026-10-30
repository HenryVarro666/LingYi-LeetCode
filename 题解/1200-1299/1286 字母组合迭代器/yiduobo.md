---
title: "1286. 字母组合迭代器"
aliases: ["yiduobo的每日leetcode 1286.字母组合迭代器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/389073660"
zhihu_id: "389073660"
zhihu_title: "yiduobo的每日leetcode 1286.字母组合迭代器"
question_id: "1286"
question: "字母组合迭代器"
problem_url: "https://leetcode.cn/problems/iterator-for-combination/"
created: "2021-07-12T22:39:19+08:00"
updated: "2021-07-12T22:39:19+08:00"
upvotes: 0
comments: 0
---

# 1286. 字母组合迭代器

> **[yiduobo的每日leetcode 1286.字母组合迭代器](https://zhuanlan.zhihu.com/p/389073660) · 知乎 · 2021-07-12 · 赞同 0**
> 力扣：[1286. 字母组合迭代器](https://leetcode.cn/problems/iterator-for-combination/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1286.字母迭代组合器

[力扣](https://leetcode-cn.com/problems/iterator-for-combination/)

首先可以明确的是，最小的组合就是字典序最小的k个字母，因此初始的第一个字符串是字典序最小的k个字母组成的字符串。最大的组合则是字典序最大的k个字母，因此最后一个字符串是字典序最大的k个字母组成的字符串，那么对于hasNext，就只需要检测当前字符串是否为最大的k个字符组成的字符串。

接下来考虑下一个字符是如何构成的。显然，我们应该优先考虑替换低位的字符，再替换高位的字符。于是我们应当从后向前进行扫描，对于当前字符char，若未使用的字符中存在某个字符的字典序大于char，那么说明我们可以通用将char替换掉来得到答案。为了求得下一个字符串，因此应当将char替换成剩下字符中字典序最小，且大于char的字符，而对于char后面的部分，则应该使用剩下未使用的字符从小到大排布。

最后附上python代码：

```python
class CombinationIterator(object):

    def __init__(self, characters, combinationLength):
        """
        :type characters: str
        :type combinationLength: int
        """
        self.char_list = characters[:]
        self.n = len(self.char_list)
        self.k = combinationLength
        self.now = None

    def next(self):
        """
        :rtype: str
        """
        if self.now is None:
            self.now = range(self.k)
            self.used = [True] * self.k + [False] * (self.n - self.k)
        else:
            self.rest_max = -1
            for index in range(self.n - 1, -1, -1):
                if not self.used[index]:
                    self.rest_max = index
                    break

            for index in range(self.k - 1, -1, -1):
                if self.now[index] < self.rest_max:
                    p = index
                    break
                self.used[self.now[index]] = False

            self.used[self.now[p]] = False
            self.now[p] += 1
            while self.used[self.now[p]]:
                self.now[p] += 1
            self.used[self.now[p]] = True
            tmp = self.now[p] + 1
            p += 1
            while p < self.k:
                while tmp < self.n and self.used[tmp]:
                    tmp += 1
                
                self.now[p] = tmp
                p += 1
                self.used[tmp] = True
                tmp += 1

        return ''.join([self.char_list[x] for x in self.now])

    def hasNext(self):
        """
        :rtype: bool
        """
        return self.now != range(self.n - self.k, self.n)

# Your CombinationIterator object will be instantiated and called as such:
# obj = CombinationIterator(characters, combinationLength)
# param_1 = obj.next()
# param_2 = obj.hasNext()
```
