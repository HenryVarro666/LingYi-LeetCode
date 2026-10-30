---
title: "1409. 查询带键的排列"
aliases: ["yiduobo的每日leetcode 1409.查询带键的排列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/406288335"
zhihu_id: "406288335"
zhihu_title: "yiduobo的每日leetcode 1409.查询带键的排列"
question_id: "1409"
question: "查询带键的排列"
problem_url: "https://leetcode.cn/problems/queries-on-a-permutation-with-key/"
created: "2021-09-02T23:20:57+08:00"
updated: "2021-09-02T23:20:57+08:00"
upvotes: 0
comments: 0
---

# 1409. 查询带键的排列

> **[yiduobo的每日leetcode 1409.查询带键的排列](https://zhuanlan.zhihu.com/p/406288335) · 知乎 · 2021-09-02 · 赞同 0**
> 力扣：[1409. 查询带键的排列](https://leetcode.cn/problems/queries-on-a-permutation-with-key/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1409.查询带键的排列

[力扣](https://leetcode-cn.com/problems/queries-on-a-permutation-with-key/)

题目要求找出对应元素在数组中的位置，然后将该元素移动到数组的最前面。如果直接模拟，将出现数组块移动的情况，这个复杂度是O(n)的，因此最终的时间复杂度为O(n^2)。

这里有两种优化的思路，第一个是直接优化数组块移动，此时可以使用平衡二叉树或者块状链表，相对比较复杂。

另一种思路则是将问题进行转化。题目要求元素在数组中的位置，那么实际上就是要求数组中有多少元素的下标小于指定元素的下标。由于这里我们并不在意下标的绝对值，而只需要知道其相对值，因此我们在移动元素时可以通过指定更小的下标来达到移动的目的。

具体来说，例如样例中的[1, 2, 3, 4, 5]，其对应的下标分别为[0, 1, 2, 3, 4]。

首先查询的是3，其下标为2，下标数组中有0、1这两个下标小于2，因此这一轮查询的答案为2。接下来是移动操作。我们可以将3的下标置为-1，那么此时的下标为[0, 1, -1, 3, 4]

接下来查询的是1，其下标为0，下标数组中只有-1这个下标小于1，因此这一轮查询的答案为1。接下来是移动操作。我们可以将1的下标置为-2，那么此时的下标为[-2, 1, -1, 3, 4]

根据上面的做法，我们可以使用树状数组来完成查询以及移动操作，这样一来时间复杂度就优化到了O(nlogn)。

需要注意的是，树状数组的下标必须是正数，因此我们可以想将数组下标往后偏移len(queries) + 1个位置，这样一来就可以保证每次操作的下标都是正数了。

最后附上python代码：

```python
class Solution(object):
    def processQueries(self, queries, m):
        """
        :type queries: List[int]
        :type m: int
        :rtype: List[int]
        """

        n = len(queries)
        maxn = m + n
        suffix_array = [0] * (maxn + 1)
        now = [0] * m
        for index in range(m):
            now[index] = n + index + 1
            self.add(now[index], 1, suffix_array, maxn)
            
        res = []
        for index, pos in enumerate(queries):
            pos -= 1
            self.add(now[pos], -1, suffix_array, maxn)
            res.append(self.sum(now[pos], suffix_array))
            now[pos] = n - index
            self.add(now[pos], 1, suffix_array, maxn)
        
        return res

    def add(self, x, delta, suffix_array, maxn):
        while x <= maxn:
            suffix_array[x] += delta
            x += x & -x
        
    def sum(self, x, suffix_array):
        res = 0
        while x:
            res += suffix_array[x]
            x -= x& -x
        
        return res
```
