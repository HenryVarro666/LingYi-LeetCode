---
title: "1535. 找出数组游戏的赢家"
aliases: ["yiduobo的每日leetcode 1535.找出数组游戏的赢家"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/simulation"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/423820734"
zhihu_id: "423820734"
zhihu_title: "yiduobo的每日leetcode 1535.找出数组游戏的赢家"
question_id: "1535"
question: "找出数组游戏的赢家"
problem_url: "https://leetcode.cn/problems/find-the-winner-of-an-array-game/"
difficulty: "Medium"
created: "2021-10-20T23:45:55+08:00"
updated: "2021-10-20T23:45:55+08:00"
upvotes: 0
comments: 0
---

# 1535. 找出数组游戏的赢家

> **[yiduobo的每日leetcode 1535.找出数组游戏的赢家](https://zhuanlan.zhihu.com/p/423820734) · 知乎 · 2021-10-20 · 赞同 0**
> 力扣：[1535. 找出数组游戏的赢家](https://leetcode.cn/problems/find-the-winner-of-an-array-game/) · Medium · 灵茶山艾府：[模拟，附若干进阶问题（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1535.找出数组游戏的赢家

[力扣](https://leetcode-cn.com/problems/find-the-winner-of-an-array-game/)

对于一个长度为n的数组而言，若当前的arr[0]是数组中的最大值，那么无论多少轮比较arr[0]都不会变化。若当前arr[0]不是数组中的最大值，那么必然存在一个比较上限，超过这个上限之后arr[0]就会换人。

考虑极限情况，若当前的arr[0]是数组中的次大值，而数组中的最大值现在位于数组的末尾，那么距离arr[0]换人之前还有arr[1]到arr[n - 2]这一共n - 2个数，也就是说arr[0]至多会赢n - 2轮然后就会换人。从另一个角度来看，就是若某个数赢了n - 1轮，那么无论对于大于等于n - 1的k，最后的赢家都会是这个数。

于是可以先根据k与n - 1的大小修正k，然后模拟这个比较过程，统计当前的arr[0]赢的轮次，直到当前的arr[0]赢够k轮为止。

最后附上python代码：

```python
class Solution(object):
    def getWinner(self, arr, k):
        """
        :type arr: List[int]
        :type k: int
        :rtype: int
        """

        n = len(arr)
        if k >= n - 1:
            k = n - 1
        
        q = arr[:]
        now = q[0]
        p = 1
        cnt = 0
        while p < len(q) and cnt < k:
            if now > q[p]:
                cnt += 1
                q.append(q[p])
            else:
                cnt = 1
                q.append(now)
                now = q[p]
            
            p += 1

        return now
```
