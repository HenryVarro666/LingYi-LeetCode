---
title: "1395. 统计作战单位数"
aliases: ["yiduobo的每日leetcode 1395.统计作战单位数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/404326763"
zhihu_id: "404326763"
zhihu_title: "yiduobo的每日leetcode 1395.统计作战单位数"
question_id: "1395"
question: "统计作战单位数"
problem_url: "https://leetcode.cn/problems/count-number-of-teams/"
created: "2021-08-27T22:09:35+08:00"
updated: "2021-08-27T22:09:35+08:00"
upvotes: 0
comments: 0
---

# 1395. 统计作战单位数

> **[yiduobo的每日leetcode 1395.统计作战单位数](https://zhuanlan.zhihu.com/p/404326763) · 知乎 · 2021-08-27 · 赞同 0**
> 力扣：[1395. 统计作战单位数](https://leetcode.cn/problems/count-number-of-teams/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1395.统计作战单位数

[力扣](https://leetcode-cn.com/problems/count-number-of-teams/)

题目要找出单调递增或者单调递减的三元组的数目，一般这种三连不等式的问题，都是先从中间这个人下手，因为这样就可能将问题分割成两个相同的子问题。

对于第index个人，设其前方比这个人高的人有t1个，比这个人矮的人有l1个，其后方比这个人高的人有t2个，比这个人矮的人有l2个，那么我们可以选择t1中的一个配合l2中的一个，或者选择l1中的一个配合t2中的一个，那么一共就有t1 \* l2 + t2 \* l1组可行的答案。

由于每个人的身高都不同，那么对于第index个人而言，其前方一共有0到index - 1一共index个人，若其中有l1个人比这个人矮，那么比这个人高的就有index - l1个人，即t1 \= index - l1。同样的，这个人后方一共有n - index - 1个人，若有l2个人比这个人矮，那么比这个人高的就一共有n - index - 1 - l2个人，即t2 \= n - index - 1 - l2。

根据上面的结论，以第index作为中间人的合法组合数目就可以写成

t1 \* l2 + t2 \* l1 \= (index - l1) \* l2 + (n - index - 1 - l2) \* l1

那么此时问题就转化成了对于每个人，找出其前方和后方有多少人比这个人要矮，这个问题则可以通过正反两趟扫描，配合上树状数据来解决。

另外，这里的rating大小最多只有100000，那么直接使用树状数组也是可以的，不过当rating更大时，则需要通过先排序，将身高映射到顺序上之后再使用树状数组。

最后附上python代码：

```python
class Solution(object):
    def numTeams(self, rating):
        """
        :type rating: List[int]
        :rtype: int
        """

        n = len(rating)
        new_rating = [0] * n
        cnt = 1
        for num, index in sorted([[x, index] for index, x in enumerate(rating)], key=lambda d:d[0]):
            new_rating[index] = cnt
            cnt += 1

        suffix_array = [0] * (n + 1)
        left = []
        for num in new_rating:
            left.append(self.sum(num - 1, suffix_array))
            self.add(num, n, suffix_array)
        
        suffix_array = [0] * (n + 1)
        right = []
        for num in new_rating[::-1]:
            right.append(self.sum(num - 1, suffix_array))
            self.add(num, n, suffix_array)
        right.reverse()

        res = 0
        for index in range(1, n - 1):
            res += left[index] * (n - index - 1 - right[index]) + right[index] * (index - left[index])
        
        return res

    def sum(self, x, suffix_array):
        res = 0
        while x:
            res += suffix_array[x]
            x -= x & -x
        
        return res

    def add(self, x, n, suffix_array):
        while x <= n:
            suffix_array[x] += 1
            x += x & -x
```
