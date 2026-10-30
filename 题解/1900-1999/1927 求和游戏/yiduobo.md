---
title: "1927. 求和游戏"
aliases: ["yiduobo的每日leetcode 1927.求和游戏"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/game-theory", "leetcode/probability-and-statistics", "题单/数学算法", "题单/贪心算法", "题单/数学算法/四-博弈论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/486384565"
zhihu_id: "486384565"
zhihu_title: "yiduobo的每日leetcode 1927.求和游戏"
question_id: "1927"
question: "求和游戏"
problem_url: "https://leetcode.cn/problems/sum-game/"
difficulty: "Medium"
rating: 2005
created: "2022-03-24T00:49:30+08:00"
updated: "2022-03-24T00:49:30+08:00"
upvotes: 0
comments: 0
---

# 1927. 求和游戏

> **[yiduobo的每日leetcode 1927.求和游戏](https://zhuanlan.zhihu.com/p/486384565) · 知乎 · 2022-03-24 · 赞同 0**
> 力扣：[1927. 求和游戏](https://leetcode.cn/problems/sum-game/) · Medium · 灵茶山艾府：[两人的具体策略，严谨证明，附 Bob 获胜概率（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1927.求和游戏

[力扣](https://leetcode-cn.com/problems/sum-game/)

首先可以明确的是，如果问号的个数是奇数，那么最后一个问号必然是归alice来操作的，alice一定有办法破坏左右相等，因此此时的答案为true。

接下来考虑两边的问号一样多的情况。

若两边数值不相等，alice可以让大的那一边的问号变成9，让小的那一边的问号变成0。设alice操作了k个较大那一侧的问号，那么bob操作较小那一侧的问号数量也必然是k个，即使bob让这些问号都变成9，也不过是抵消了alice的操作，此时两侧的大小关系并没有发生变化。同时，bob剩下可操作的问号都在较大的这一侧，也就是说bob已经没有办法让左右两侧相等了。

反过来，若左右两侧数值相等，那么当alice操作了一个问号之后，bob只需要在另一侧按同样的数值操作一个问号即可，这样一来两侧最终的结果必然相等，此时bob赢。

那么此时只有当两边已有的数值相等时bob才会赢，否则都是alice赢。

接下来对于两边问号不一样多的情况，如果问号较多的那一边已有的数值和反而比较大，那么一定时alice赢，因为alice只需要将较大这边的问号变成9，将较小那边的问号变成0即可。

接下来考虑更一般的情况，具体来说就偶数个问号，且两侧问号数量不相等，问号较多的一侧数值较小。直接考虑比较复杂，不妨先从小的情况入手。

假设现在有两个问号，此时左右两边的数值和分别为x和y，那么可以分成三种情况：

1、问号都在左侧，那么此时必然有x \< y。令a和b表示alice和bob操作完后问号的值，那么bob的目的就是让式子x + a + b \= y成立。对于这个式子：

1-1）若x > y - 9，此时alice只要让a \= 9，x + a就必然大于y，此时上面的式子就一定不成立

1-2）若x \< y - 9，此时alice只要让a \= 0，那么即使此时bob让b \= 9，此时x + a + b还是小于y，此时上面的式子同样不成立

1-3）此时只剩下x \= y - 9这种情况。对于这种情况，bob可以根据a的值调整b的值，即让b保持b \= 9 - a，就能满足x + a + b \= y

2、问号都在右侧，那么此时必然有x > y。此时需要满足的是x \= y + a + b，那么与情况1相同，此时只有x \= y + 9这种情况时bob才能赢

综合起来，就是ma - mi \= 9，其中ma和mi分别表示当前数值较大的那一侧和较小的那一侧。这里隐藏的条件是mi_q \= 2，ma_q \= 0，即ma这一侧没有问号，mi这一侧有两个问号。

对于这个式子，尝试往更大的情况推广，也就是ma - mi \= (mi_q - ma_q) / 2 \* 9。

证明也很简单，如果ma > mi + (mi_q - ma_q) / 2 \* 9，那么就让alice在ma这一侧的问号全部取9，mi这一侧的问号全部取0。不妨设alice在ma这一侧操作了ma_alice个问号，那么其在mi这一侧操作的问号数量就是(mi_q + ma_q) / 2 - ma_alice，从而推出bob在mi这一侧操作的问号数量为mi_bob \= mi_q - ((mi_q + ma_q) / 2 - ma_alice)。即使bob让这些问号都变成9，那么此时的两侧的情况也只是ma + ma_alice \* 9以及mi + (mi_q - ma_q) / 2 \* 9 + ma_alice \* 9。由于ma > mi + (mi_q - ma_q) / 2 \* 9，那么此时依然是ma这一侧比较大，且此时bob剩下可操作的问号都在ma这一边，因此必然是alice获胜。

反过来，对于ma \< mi + (mi_q - ma_q) / 2 \* 9的情况，alice也是反过来操作，让ma这一侧的问号全部取0，mi这一侧的问号全部取9，同样可以得出alice必胜的结论。

综合起来，就是在偶数个问号，且两侧问号数量不相等，问号较多的一侧数值较小这种情况下，只有满足ma - mi \= (mi_q - ma_q) / 2 \* 9这个式子时bob才能赢，否则都是alice赢。

另外，可以发现最上面讨论的若干种特殊情况其实都符合上面这个等式，因此最终实现时只需要一趟扫描，分别统计两侧数值之和以及问号个数，然后根据上面式子是否相等就能得出alice和bob的输赢情况。

最后附上python代码：

```python
class Solution(object):
    def sumGame(self, num):
        """
        :type num: str
        :rtype: bool
        """

        left_q = right_q = 0
        left_s = right_s = 0
        n = len(num)
        for char in num[:n / 2]:
            if char == '?':
                left_q += 1
            else:
                left_s += int(char)
        
        for char in num[n / 2:]:
            if char == '?':
                right_q += 1
            else:
                right_s += int(char)

        return (left_s - right_s) * 2 != (right_q - left_q) * 9
```
