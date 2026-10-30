---
title: "1652. 拆炸弹"
aliases: ["yiduobo的每日leetcode 1652.拆炸弹"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/一-定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/440610386"
zhihu_id: "440610386"
zhihu_title: "yiduobo的每日leetcode 1652.拆炸弹"
question_id: "1652"
question: "拆炸弹"
problem_url: "https://leetcode.cn/problems/defuse-the-bomb/"
difficulty: "Easy"
created: "2021-12-03T00:08:39+08:00"
updated: "2021-12-03T00:08:39+08:00"
upvotes: 1
comments: 0
---

# 1652. 拆炸弹

> **[yiduobo的每日leetcode 1652.拆炸弹](https://zhuanlan.zhihu.com/p/440610386) · 知乎 · 2021-12-03 · 赞同 1**
> 力扣：[1652. 拆炸弹](https://leetcode.cn/problems/defuse-the-bomb/) · Easy · 灵茶山艾府：[O(n) 定长滑动窗口（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1652.拆炸弹

[力扣](https://leetcode-cn.com/problems/defuse-the-bomb/)

题目需要根据给出的k分别进行不同的计算，不过这里k等于0时可以直接返回全0，而另外两种计算都是涉及到静态区间和的。对于静态区间和问题，一种常见的做法就是使用前缀和来替代。

当然，本题有特殊的地方就是这里的区间和是个环状的，因此需要注意处理越界的情况。对于不越界的情况，可以直接计算边界然后利用前缀和相减。而发生越界时，原始的区间和就变成了一个前缀和加上一个后缀和，前缀和这个已经求解出来了，后缀和则同样是用区间和来进行求解，唯一需要注意的地方就是这个越界的长度。对于当前位置index：

1、若k大于0，那么只有可能越过右边界，也就是说此时的index + k必然要大于n - 1。此时从index + 1到n - 1一共有n - 1 - index个数，那么还剩下k - (n - 1 - index)个数需要计算前缀和。由于下标从0开始，那么这里的前缀和就是s[k - (n - 1) - index - 1]了，而这个后缀和自然是s[n - 1] - s[index]。综合起来就是s[n - 1] - s[index] + s[k - (n - 1) - index - 1]

2、若k小于0，那么只有可能越过左边界，也就是说此时的index + k必然要小于0。当然，为了方便计算，也可以将这个界限果然到index + k小于等于0，等于0的情况就相当与前缀和加上一个长度为0的后缀和。此时从index - 1到0一共有index个数，那么还剩下-k - index个数需要计算后缀和，也就是s[n - 1] - s[n - (-k - index) - 1]。另外，当index本身就是0的时候，前缀和就是0，此时的总和就是s[n - 1] - s[n - (-k - index) - 1]，而当index大于0时，则需要额外加上一项前缀和s[index - 1]

最后附上python代码：

```python
class Solution(object):
    def decrypt(self, code, k):
        """
        :type code: List[int]
        :type k: int
        :rtype: List[int]
        """

        n = len(code)
        if k == 0:
            return [0] * n

        s = [code[0]]
        for num in code[1:]:
            s.append(s[-1] + num)

        res = []
        for index in range(n):
            if k > 0:
                if index + k < n:
                    res.append(s[index + k] - s[index])
                else:
                    offset = k - (n - 1 - index) - 1
                    res.append(s[-1] - s[index] + s[offset])
            elif k < 0:
                if index + k > 0:
                    res.append(s[index - 1] - s[index + k - 1])
                else:
                    offset = n - (-k - index) - 1
                    res.append(s[-1] - s[offset])
                    if index > 0:
                        res[-1] += s[index - 1]
        
        return res
```
