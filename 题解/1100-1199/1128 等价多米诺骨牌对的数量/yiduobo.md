---
title: "1128. 等价多米诺骨牌对的数量"
aliases: ["yiduobo的每日leetcode 1128.等价多米诺骨牌对的数量"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376254031"
zhihu_id: "376254031"
zhihu_title: "yiduobo的每日leetcode 1128.等价多米诺骨牌对的数量"
question_id: "1128"
question: "等价多米诺骨牌对的数量"
problem_url: "https://leetcode.cn/problems/number-of-equivalent-domino-pairs/"
difficulty: "Easy"
created: "2021-05-29T13:49:40+08:00"
updated: "2021-05-29T13:49:40+08:00"
upvotes: 0
comments: 0
---

# 1128. 等价多米诺骨牌对的数量

> **[yiduobo的每日leetcode 1128.等价多米诺骨牌对的数量](https://zhuanlan.zhihu.com/p/376254031) · 知乎 · 2021-05-29 · 赞同 0**
> 力扣：[1128. 等价多米诺骨牌对的数量](https://leetcode.cn/problems/number-of-equivalent-domino-pairs/) · Easy · 灵茶山艾府：[枚举右，维护左（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1128.等价多米诺骨牌对的数量

[力扣](https://leetcode-cn.com/problems/number-of-equivalent-domino-pairs/)

对于某张多米诺骨牌而言，设其等价的多米诺骨牌一共有k张，那么就可以形成k \* (k - 1) / 2组等价的多米诺骨牌对，因此我们只需要使用哈希表统计每种骨牌出现的次数，然后遍历所有骨牌类型计算答案即可。

至于哈希的方式，注意到这里的数值大小在1到9之间，我采用的是a \* 10 + b这种哈希方式，其中要确保a是小于等于b的。

最后附上python代码：

```python
class Solution(object):
    def numEquivDominoPairs(self, dominoes):
        """
        :type dominoes: List[List[int]]
        :rtype: int
        """

        f = {}
        for x, y in dominoes:
            if x > y:
                x, y = y, x
            key = x * 10 + y
            f[key] = f.get(key, 0) + 1
        
        res = 0
        for cnt in f.values():
            res += (cnt - 1) * cnt / 2
        return res
```
