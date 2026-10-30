---
title: "2271. 毯子覆盖的最多白色砖块数"
aliases: ["yiduobo的每日leetcode 2271.毯子覆盖的最多白色砖块数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sorting", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550035530"
zhihu_id: "550035530"
zhihu_title: "yiduobo的每日leetcode 2271.毯子覆盖的最多白色砖块数"
question_id: "2271"
question: "毯子覆盖的最多白色砖块数"
problem_url: "https://leetcode.cn/problems/maximum-white-tiles-covered-by-a-carpet/"
difficulty: "Medium"
rating: 2022
created: "2022-08-05T00:08:46+08:00"
updated: "2022-08-05T00:08:46+08:00"
upvotes: 0
comments: 0
---

# 2271. 毯子覆盖的最多白色砖块数

> **[yiduobo的每日leetcode 2271.毯子覆盖的最多白色砖块数](https://zhuanlan.zhihu.com/p/550035530) · 知乎 · 2022-08-05 · 赞同 0**
> 力扣：[2271. 毯子覆盖的最多白色砖块数](https://leetcode.cn/problems/maximum-white-tiles-covered-by-a-carpet/) · Medium · 灵茶山艾府：[排序 + 滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2271.毯子覆盖的最多白色砖块数

[力扣](https://leetcode.cn/problems/maximum-white-tiles-covered-by-a-carpet/)

题目中可以得到最优解的覆盖方式可能有很多种，不过可以明确的是，其中必然有某种最优方案是用毯子从某一段白色砖块的起点开始进行覆盖的。

一个简单的证明是如果某种最优方案中毯子并不是从某一段白色砖块的起点开始，那么设毯子覆盖的最左侧位置为p，且p不是任何白色砖块段落的起点，那么此时有两种情况：

1、p所处的位置不是白色砖块，且p右侧最近的白色砖块位置为q。

此时如果将毯子的起点从p移动到q，那么实际上覆盖的区域就去掉了[p, q- 1]这一段，同时新加入了[p + carpetLen, q + carpetLen - 1]这一段。由于p到q - 1直接没有任何白色砖块，因此这样移动后覆盖的白色砖块只会变多

2、p所处的位置是白色砖块，且p左侧最近的白色砖块段的起点为q。此时将p移动到q，那么实际上覆盖的区域就加入了[q, p - 1]这一段，同时去掉了[q + carpetLen, p + carpetLen - 1]这一段。由于新加入的这一段[q, p - 1]中全都是白色砖块，因此这样移动后覆盖的白色砖块同样是只会变多

综合上面两种情况，就说明必然有某种最优方案是用毯子从某一段白色砖块的起点开始覆盖。

根据这个结论，就可以枚举毯子覆盖在哪一段白色砖块的起点，然后计算当前情况下覆盖住了多少白色砖块。至于计算覆盖住的白色砖块，则可以通过排序后二分或者排序后利用单调性，使用双指针来进行求解。

我在这里利用的是单调性，不过需要注意的是，在确定了毯子覆盖的起点后，其终点可能覆盖住完整的白色砖块段，也可能在某个白色砖块段中间，这种情况下计算覆盖砖块时需要特别注意。

最后附上python代码：

```python
class Solution(object):
    def maximumWhiteTiles(self, tiles, carpetLen):
        """
        :type tiles: List[List[int]]
        :type carpetLen: int
        :rtype: int
        """

        sorted_tiles = sorted(tiles, key=lambda d:d[0])
        n = len(sorted_tiles)
        end_pos = sorted_tiles[0][0] + carpetLen - 1

        p = 0
        now = sorted_tiles[0][1] - sorted_tiles[0][0] + 1
        while p + 1 < n and sorted_tiles[p + 1][0] <= end_pos:
            p += 1
            now += sorted_tiles[p][1] - sorted_tiles[p][0] + 1
        
        if end_pos >= sorted_tiles[p][1]:
            res = now
        else:
            res = now - (sorted_tiles[p][1] - sorted_tiles[p][0] + 1) + (end_pos - sorted_tiles[p][0] + 1)
        
        for head_index in range(1, n):
            end_pos = sorted_tiles[head_index][0] + carpetLen - 1
            now -= sorted_tiles[head_index - 1][1] - sorted_tiles[head_index - 1][0] + 1
            while p + 1 < n and sorted_tiles[p + 1][0] <= end_pos:
                p += 1
                now += sorted_tiles[p][1] - sorted_tiles[p][0] + 1
            
            if end_pos >= sorted_tiles[p][1]:
                res = max(res, now)
            else:
                res = max(res, now - (sorted_tiles[p][1] - sorted_tiles[p][0] + 1) + (end_pos - sorted_tiles[p][0] + 1))
        
        return res
```
