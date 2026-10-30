---
title: "3996. 偶数次骑士移动"
aliases: ["yiduobo的每日leetcode 3996.偶数次骑士移动"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/brainteaser", "leetcode/math", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2063372633476015726"
zhihu_id: "2063372633476015726"
zhihu_title: "yiduobo的每日leetcode 3996.偶数次骑士移动"
question_id: "3996"
question: "偶数次骑士移动"
problem_url: "https://leetcode.cn/problems/even-number-of-knight-moves/"
difficulty: "Easy"
rating: 1260
created: "2026-07-22T21:26:16+08:00"
updated: "2026-07-22T21:26:16+08:00"
upvotes: 1
comments: 0
---

# 3996. 偶数次骑士移动

> **[yiduobo的每日leetcode 3996.偶数次骑士移动](https://zhuanlan.zhihu.com/p/2063372633476015726) · 知乎 · 2026-07-22 · 赞同 1**
> 力扣：[3996. 偶数次骑士移动](https://leetcode.cn/problems/even-number-of-knight-moves/) · Easy · 灵茶山艾府：[判断奇偶性，O(1) 一行（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3996.偶数次骑士移动

<https://leetcode.cn/problems/even-number-of-knight-moves/description/>

题目给出两个整数数组start和target，每个数组的形式都是[x, y]，表示标准8 \* 8国际象棋棋盘上的一个格子。

若一个骑士可以用偶数次移动从start移动到target，那么就返回true，否则返回false。

骑士的一次合法移动是，沿一个方向移动两格，然后再沿与其垂直的方向移动一格。

首先，在8 \* 8的棋盘上，一个马可以从任意一个格子出发，经过一系列跳跃，跳到棋盘上的另一个格子，也就是说不会出现无法从start跳到target的情况。

另一方面，对于每次跳跃操作，相对于跳跃的起点，坐标之和的变化必然为奇数。更进一步的，进行了偶数次跳跃后，左边之和的变化为偶数，反之则为奇数。

基于以上两点，就可以通过start和target坐标之和的差来判断是否能通过偶数次移动从start到达target。若这个差为偶数，则说明可以，否则说明不行。

最后附上python代码：

```python
class Solution(object):
    def canReach(self, start, target):
        """
        :type start: List[int]
        :type target: List[int]
        :rtype: bool
        """
        
        return (sum(target) + sum(start)) % 2 == 0
```
