---
title: "710. 黑名单中的随机数"
aliases: ["yiduobo的每日leetcode 710.黑名单中的随机数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/326829967"
zhihu_id: "326829967"
zhihu_title: "yiduobo的每日leetcode 710.黑名单中的随机数"
question_id: "710"
question: "黑名单中的随机数"
problem_url: "https://leetcode.cn/problems/random-pick-with-blacklist/"
created: "2020-12-02T21:58:55+08:00"
updated: "2020-12-02T21:58:55+08:00"
upvotes: 1
comments: 0
---

# 710. 黑名单中的随机数

> **[yiduobo的每日leetcode 710.黑名单中的随机数](https://zhuanlan.zhihu.com/p/326829967) · 知乎 · 2020-12-02 · 赞同 1**
> 力扣：[710. 黑名单中的随机数](https://leetcode.cn/problems/random-pick-with-blacklist/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

710.黑名单中的随机数

[力扣](https://leetcode-cn.com/problems/random-pick-with-blacklist/)

题目给出一个黑名单，要求从0到n - 1这n个数中随机出一个不在黑名单中的数。设黑名单中的数一共有k个，那么我们就需要从剩下的n - k个中随机出一个数。若0到n - 1 - k这n - k个数中有p个数是黑名单中的数，那么反过来，从n - k到n - 1这k个数中就有k - p个数在黑名单中，从而得知恰好也是p个数不在黑名单中。

于是一个自然的想法就是将0到n - 1 - k之间在黑名单中的这p个数，与n - k到n - 1之间不在黑名单中的这p个数做映射。然后从0到n - k - 1中随机一次选出res，若res存在映射关系，那么返回其对应的数，否则直接返回res。

对于建立映射，我们的做法是使用一个数now来记录当前最小的未被使用过，且不在黑名单当中的数。now初始化为n - k，那么对于每个0到n - k - 1之间且在黑名单中的数x，若now在黑名单中，那么将now加一，直到now不在黑名单中，然后建立起x到now的映射即可。

最后附上python代码：

```python
class Solution(object):

    def __init__(self, N, blacklist):
        """
        :type N: int
        :type blacklist: List[int]
        """
        black_set = set(blacklist)
        self.pos_dict = {}
        self.valid_cnt = N - len(blacklist)
        now = self.valid_cnt
        for num in blacklist:
            if num >= self.valid_cnt:
                continue
            else:
                while now in black_set:
                    now += 1
                self.pos_dict[num] = now
                now += 1

    def pick(self):
        """
        :rtype: int
        """
        res = random.randint(0, self.valid_cnt - 1)
        return self.pos_dict.get(res, res)

# Your Solution object will be instantiated and called as such:
# obj = Solution(N, blacklist)
# param_1 = obj.pick()
```
