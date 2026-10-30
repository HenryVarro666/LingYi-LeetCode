---
title: "1686. 石子游戏VI"
aliases: ["yiduobo的每日leetcode 1686.石子游戏VI"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/game-theory", "leetcode/sorting", "题单/数学算法", "题单/数学算法/四-博弈论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/445908339"
zhihu_id: "445908339"
zhihu_title: "yiduobo的每日leetcode 1686.石子游戏VI"
question_id: "1686"
question: "石子游戏 VI"
problem_url: "https://leetcode.cn/problems/stone-game-vi/"
difficulty: "Medium"
rating: 2001
created: "2021-12-16T00:01:35+08:00"
updated: "2021-12-16T00:01:36+08:00"
upvotes: 2
comments: 0
---

# 1686. 石子游戏VI

> **[yiduobo的每日leetcode 1686.石子游戏VI](https://zhuanlan.zhihu.com/p/445908339) · 知乎 · 2021-12-16 · 赞同 2**
> 力扣：[1686. 石子游戏 VI](https://leetcode.cn/problems/stone-game-vi/) · Medium · 灵茶山艾府：[[灵茶山艾府题解/solutions/1686 石子游戏 VI · 详细解释为什么要按照 a-i-+b-i- 排序（Python-Java-C++-Go-JS-Rust）|详细解释为什么要按照 a[i]+b[i] 排序（Python/Java/C++/Go/JS/Rust）]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1686.石子游戏VI

[力扣](https://leetcode-cn.com/problems/stone-game-vi/)

对于第i块石头而言，如果被alice拿了，alice收益除了常规的aliceValues[i]外，还有一个隐藏收益就是bob不能拿这块石头了。如果这块石头对应的bobValues[i]很高的话，那么alice拿了之后实际上降低了bob的总收益。同理，对bob来说也一样，因此每块石头的价值可以认为是自己拿了这块石头的价值，加上对手不能拿这块石头的价值，也就是说对于第i块石头，其价值就是aliceValues[i] + bobValues[i]。

由于可以任意选择剩下的石头，那么自然是从价值高的石头开始拿，因此可以将石头按aliceValues[i] + bobValues[i]从大到小进行排序，然后两个人依次拿这些石头，最后通过两个人手上石头数的大小判断谁胜谁负。

最后附上python代码：

```python
class Solution(object):
    def stoneGameVI(self, aliceValues, bobValues):
        """
        :type aliceValues: List[int]
        :type bobValues: List[int]
        :rtype: int
        """

        merge_list = sorted(zip(aliceValues, bobValues), key=lambda d:(d[0] + d[1]), reverse=True)
        alice = bob = 0
        for index in range(len(merge_list)):
            if index & 1:
                bob += merge_list[index][1]
            else:
                alice += merge_list[index][0]
        
        if alice > bob:
            return 1
        elif alice == bob:
            return 0
        else:
            return -1
```
