---
title: "2833. 距离原点最远的点"
aliases: ["yiduobo的每日leetcode 2833.距离原点最远的点"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659363253"
zhihu_id: "659363253"
zhihu_title: "yiduobo的每日leetcode 2833.距离原点最远的点"
question_id: "2833"
question: "距离原点最远的点"
problem_url: "https://leetcode.cn/problems/furthest-point-from-origin/"
difficulty: "Easy"
rating: 1294
created: "2023-10-02T23:32:33+08:00"
updated: "2023-10-02T23:32:33+08:00"
upvotes: 0
comments: 0
---

# 2833. 距离原点最远的点

> **[yiduobo的每日leetcode 2833.距离原点最远的点](https://zhuanlan.zhihu.com/p/659363253) · 知乎 · 2023-10-02 · 赞同 0**
> 力扣：[2833. 距离原点最远的点](https://leetcode.cn/problems/furthest-point-from-origin/) · Easy · 灵茶山艾府：[贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2833.距离原点最远的点

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/furthest-point-from-origin/)

序列中的下划线可以人工控制，但是L和R是无法变更的，于是可以先一趟遍历，使用变量cnt统计下划线出现的次数，同时根据L和R计算当前的下标位置now。

接下来，若now处于正半轴，那么就应该继续向右走，对应的答案就是now + cnt，反过来，若now处于负半轴，那么就应该继续向左走，此时对应的答案就是cnt - now。

最后附上python代码：

```python
class Solution(object):
    def furthestDistanceFromOrigin(self, moves):
        """
        :type moves: str
        :rtype: int
        """

        cnt = 0
        now = 0
        for char in moves:
            if char == '_':
                cnt += 1
            elif char == 'L':
                now -= 1
            else:
                now += 1
        
        if now >= 0:
            now += cnt
        else:
            now -= cnt
        
        return abs(now)
```
