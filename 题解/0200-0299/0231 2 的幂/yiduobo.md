---
title: "231. 2的幂"
aliases: ["yiduobo的每日leetcode 231. 2的幂"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/一-基础题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/149854649"
zhihu_id: "149854649"
zhihu_title: "yiduobo的每日leetcode 231. 2的幂"
question_id: "231"
question: "2 的幂"
problem_url: "https://leetcode.cn/problems/power-of-two/"
difficulty: "Easy"
created: "2020-06-21T20:06:47+08:00"
updated: "2020-06-21T20:06:47+08:00"
upvotes: 0
comments: 0
---

# 231. 2的幂

> **[yiduobo的每日leetcode 231. 2的幂](https://zhuanlan.zhihu.com/p/149854649) · 知乎 · 2020-06-21 · 赞同 0**
> 力扣：[231. 2 的幂](https://leetcode.cn/problems/power-of-two/) · Easy · 灵茶山艾府：[O(1) 位运算，一行写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

231\. 2的幂<https://leetcode-cn.com/problems/power-of-two/>

可以不断模2来判断，不过这样做的时间复杂度是O(logn)，有更好的做法。

注意到2的幂在二进制表示下一定是1000....000的形式，于是我们可以通过n &\= n - 1去除掉最低位的1，然后判断n是否等于0。

最后附上python代码：

```python
class Solution(object):
    def isPowerOfTwo(self, n):
        """
        :type n: int
        :rtype: bool
        """

        if n <= 0:
            return False

        return n & (n - 1) == 0
```
