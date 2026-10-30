---
title: "2029. 石子游戏IX"
aliases: ["yiduobo的每日leetcode 2029.石子游戏IX"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/game-theory", "题单/数学算法", "题单/贪心算法", "题单/数学算法/四-博弈论", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/508218841"
zhihu_id: "508218841"
zhihu_title: "yiduobo的每日leetcode 2029.石子游戏IX"
question_id: "2029"
question: "石子游戏 IX"
problem_url: "https://leetcode.cn/problems/stone-game-ix/"
difficulty: "Medium"
rating: 2277
created: "2022-05-01T23:32:04+08:00"
updated: "2022-05-01T23:32:04+08:00"
upvotes: 0
comments: 0
---

# 2029. 石子游戏IX

> **[yiduobo的每日leetcode 2029.石子游戏IX](https://zhuanlan.zhihu.com/p/508218841) · 知乎 · 2022-05-01 · 赞同 0**
> 力扣：[2029. 石子游戏 IX](https://leetcode.cn/problems/stone-game-ix/) · Medium · 灵茶山艾府：[两种方法：计算最大回合数 / 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2029.石子游戏IX

[力扣](https://leetcode-cn.com/problems/stone-game-ix/)

题目决定胜负的方式有两种，第一种是移除的石子之和为3的倍数，第二种则是石子全部用完了。对于3的倍数，一个很自然的想法就是将石子对3取模，按余数分为3类。

对于这三类，首先余0这一类不能一来就出，但是可以在中途任意时候出，相当于转换了先手和后手。对于余1和余2这两类，除了最开始这一操作之外，其他的操作都必须根据已经移除的石子模3余1还是余2来决定，从这个角度来说，余1和余2可以认为是完全等价的，那么在这里就只需要关心这两种石子的堆数。

记模3余0的石子堆数为zero，对于余1和余2的，则记较多的那一种的堆数为ma，较少的为mi。

接下来开始分情况讨论。

1、如果mi和ma都等于0，那么alice一开始只能移除zero这一类，直接就输了

2、如果mi等于0且ma大于0，那么alice一开始只能移除一次ma这一类。在接下来的移除序列中，只能再出现一次ma以及若干次zero。

因此当ma小于等于2时，可以顺利移除完所有的石子，此时alice是必败的。

而当ma大于2时，就看轮到谁来选第三次的ma。由于zero这一类可以随时插进来，那么最终序列的长度就是2 + zero。若这个值为奇数，说明alice进行了最后一次操作，此时bob必败。反过来若为偶数，则是alice必败。

总结以上两类情况，就是当mi等于0时，只有当ma大于2且zero为奇数时alice必胜，其他情况都是alice必败。

3、如果mi和ma都大于0，此时alice有两种可选的策略，即先移除ma这一类，或者先移除mi这一类。同样是分开讨论：

3-1）alice第一次移除了ma这一类，那么在不考虑zero这一类的情况下，移除的序列必然是

ma -> ma -> mi -> ma -> mi -> ...

当ma - mi \<\= 2时，按照这个序列可以将所有石子都移除掉，因此在这种情况下alice选择先移除ma这一类就是必败的。

当ma - mi > 2是，最终的序列必然是以ma这一类结尾的，同时还有用不掉的ma这一类，此时同样是考察序列长度的奇偶性。在不加入zero这一类时，序列的长度为偶数，那么若zero为偶数，alice必败，否则alice必胜。

综合起来就是，只有当zero为奇数且ma - mi > 2时，alice才会选择先移除ma这一类，而在其他情况下alice如果先移除ma这一类都是必败的。

3-2）alice第一次移除了mi这一类，那么在不考虑zero这一类的情况下，移除的序列必然是

mi -> mi -> ma -> mi -> ma -> ... -> mi -> ma

与上面略有不同，由于mi \<\= ma，因此在这里必然是以ma这一类收场，且必然还存在没有用掉的ma这一类。在不加入zero这一类时，序列的长度为奇数，那么若zero为偶数，alice必胜，否则alice必败。

总结以上两类情况，就是当zero为偶数时，alice必胜，否则若ma - mi > 2，也还是alice必胜，否则alice必败。

根据以上结论，只需要一趟遍历，统计每种石子的数量，并按照上面的结论分情况讨论即可。

最后附上python代码：

```python
class Solution(object):
    def stoneGameIX(self, stones):
        """
        :type stones: List[int]
        :rtype: bool
        """

        zero = one = two = 0
        for stone in stones:
            if stone % 3 == 0:
                zero += 1
            elif stone % 3 == 1:
                one += 1
            else:
                two += 1

        ma, mi = one, two
        if ma < mi:
            ma, mi = mi, ma
        
        if mi == 0:
            return ma > 2 and zero % 2 == 1
        
        if zero % 2 == 0:
            return True

        return ma - mi > 2
```
