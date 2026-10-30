---
title: "1238. 循环码排序"
aliases: ["yiduobo的每日leetcode 1238.循环码排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/384852038"
zhihu_id: "384852038"
zhihu_title: "yiduobo的每日leetcode 1238.循环码排序"
question_id: "1238"
question: "循环码排序"
problem_url: "https://leetcode.cn/problems/circular-permutation-in-binary-representation/"
created: "2021-06-28T22:35:24+08:00"
updated: "2021-06-28T22:35:24+08:00"
upvotes: 0
comments: 0
---

# 1238. 循环码排序

> **[yiduobo的每日leetcode 1238.循环码排序](https://zhuanlan.zhihu.com/p/384852038) · 知乎 · 2021-06-28 · 赞同 0**
> 力扣：[1238. 循环码排序](https://leetcode.cn/problems/circular-permutation-in-binary-representation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1238.循环码排序

[力扣](https://leetcode-cn.com/problems/circular-permutation-in-binary-representation/)

首先，题目要求找一个循环码，因此实际上我们只需要找出任意一种合法的排列，然后循环移动直到将start移动到首位即可。

接下来我们需要想办法找出一种合法的排列。

不妨设f[0], f[1], ..., f[2^(n - 1) - 1]为0到2^(n - 1) - 1的一种合法排列，那么对于2^(n - 1)到2^n - 1而言

f[0] + 2^(n - 1)，f[1] + 2^(n - 1)，...，f[2^(n - 1) - 1] + 2^(n - 1)

就相当于在原来的f[0]到f[2^(n - 1) - 1]的基础上在最高位上加上了一个1，因此也是一个合法的序列。

另外，f[0]与f[0] + 2^(n - 1)只差一个1，而f[2^(n - 1) - 1]与f[2^(n - 1) - 1] + 2^(n - 1)同样也是差一个1，因此我们只需要将

f[0] + 2^(n - 1)，f[1] + 2^(n - 1)，...，f[2^(n - 1) - 1] + 2^(n - 1)

反过来，然后拼接在原来的p[0]到p[2^(n - 1) - 1]的后面就可以得到0到2^n - 1的合法序列。

例如当n \= 3时，我们已经得到了0到2^(3 - 1) - 1的一个合法序列，为3, 2, 0, 1

其二进制表示为11, 10, 00, 01

我们将最高位添加一个1，就得到了111, 110, 100, 101

这个序列显然是合法的，其对应的分别为7, 6, 4, 5

最后，我们只需要将111, 110, 100, 101倒转过来，得到101, 100, 110, 111，然后拼接在011, 010, 000, 001后面，就得到了一个0到2^3 - 1的合法序列，为

011, 010, 000, 001, 101, 100, 110, 111

也就是3, 2, 0, 1, 5, 4, 6, 7

得到合法序列之后，找到start在其中的位置p，然后将f[:p]并拼接到f[p:]后面即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def circularPermutation(self, n, start):
        """
        :type n: int
        :type start: int
        :rtype: List[int]
        """

        f = [0]
        for index in range(1, n + 1):
            tmp = [x + (1 << (index - 1)) for x in f]
            tmp.reverse()
            f.extend(tmp)
        
        p = 0
        for index, num in enumerate(f):
            if num == start:
                p = index
                break
        
        return f[p:] + f[:p]
```
