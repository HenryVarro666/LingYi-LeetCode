---
title: "2683. 相邻值的按位异或"
aliases: ["yiduobo的每日leetcode 2683.相邻值的按位异或"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/649793975"
zhihu_id: "649793975"
zhihu_title: "yiduobo的每日leetcode 2683.相邻值的按位异或"
question_id: "2683"
question: "相邻值的按位异或"
problem_url: "https://leetcode.cn/problems/neighboring-bitwise-xor/"
difficulty: "Medium"
rating: 1518
created: "2023-08-13T22:47:56+08:00"
updated: "2023-08-13T22:47:56+08:00"
upvotes: 0
comments: 0
---

# 2683. 相邻值的按位异或

> **[yiduobo的每日leetcode 2683.相邻值的按位异或](https://zhuanlan.zhihu.com/p/649793975) · 知乎 · 2023-08-13 · 赞同 0**
> 力扣：[2683. 相邻值的按位异或](https://leetcode.cn/problems/neighboring-bitwise-xor/) · Medium · 灵茶山艾府：[推式子（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2683.相邻值的按位异或

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/neighboring-bitwise-xor/description/)

如果存在某个合法的original数组，那么一定可以将其调整为以0开头的形式。若其以1开头，那么就可以将数组中的每个数v都变为1 - v，此时相邻元素间的异或结果不会发生变化，也就是说最终生成的数组依然与derived相同。根据这个结论，就可以令original[0] \= 0，然后根据derived数组反推出original数组。若original头尾的异或值等于derived的最后一个数，那么说明可以构造成功，否则说明无法构造。

更进一步的，在这里有

original[1] \= 0 ^ derived[0]

original[2] \= original[1] ^ derived[1]

...

original[n - 1] \= original[n - 2] ^ derived[n - 2]

将上面的式子逐个带入，就有

original[n - 1] \= derived[0] ^ derived[1] ^ ... ^ derived[n - 2]

而最终要求original[n - 1] ^ 0 \= derived[n - 1]，那么就有

derived[0] ^ derived[1] ^ ... ^ derived[n - 2] ^ derived[n - 1] \= 0

也就是说在这里只需将derived中的每个元素都异或起来，检测结果是否为0就行了。

最后附上python代码：

```python
class Solution(object):
    def doesValidArrayExist(self, derived):
        """
        :type derived: List[int]
        :rtype: bool
        """

        xor = 0
        for v in derived:
            xor ^= v
        
        return xor == 0
```
