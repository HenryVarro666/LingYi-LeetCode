---
title: "LCP 59. 搭桥过河"
aliases: ["yiduobo的每日leetcode LCP59.搭桥过河"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/578857297"
zhihu_id: "578857297"
zhihu_title: "yiduobo的每日leetcode LCP59.搭桥过河"
question_id: "LCP 59"
question: "搭桥过河"
created: "2022-10-31T06:18:03+08:00"
updated: "2022-10-31T06:18:58+08:00"
upvotes: 2
comments: 0
---

# LCP 59. 搭桥过河

> **[yiduobo的每日leetcode LCP59.搭桥过河](https://zhuanlan.zhihu.com/p/578857297) · 知乎 · 2022-10-31 · 赞同 2**
> 力扣：LCP 59. 搭桥过河

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP59.搭桥过河

[力扣](https://leetcode.cn/problems/NfY1m5/)

非常有数学技巧的一题，写着写着仿佛有一种回到学生时代刚开始学习如何相关知识的错觉。

最基础的动态规划算法是很容易想到的。令f[i][j]表示走到第i + 1段木头，且这一段木头的起点位置在j时所需的最小操作次数。那么对于f[i][j]，就有

f[i][j] \= min(f[i - 1][k]) + abs(wood[i][0] - j)

这里要求第i段木头与最后这段木头重叠，那么：

1、当第i段木头的尾部与最后这段木头的头部重叠时，有

k + wood[i - 1][1] - wood[i - 1][0] \= j

2、当第i段木头的头部与最后这段木头的尾部重叠时，有

k \= j + wood[i][1] - wood[i][0]

综合起来，就是j - (wood[i - 1][1] - wood[i - 1][0]) \<\= k \<\= j + wood[i][1] - wood[i][0]

如果用length表示木头的长度，那么转移方程就可以写作

f[i][j] \= min(f[i - 1][k]) + abs(wood[i][0] - j)，其中j - length[i - 1] \<\= k \<\= j + length[i]

---

当然，对于本题这么巨大的数据规模而言，上面基础的动态规划算法必然是不行的，需要想办法进行优化。观察转移方程可以发现，这是两个凸函数的叠加，也就是说，如果将j视为自变量，f[i][j]就是关于j的一个凸函数。

具体的证明我已经不太记得了，不过对于本题，可以选择从图像出发得到一些思路。

首先，当i \= 0时，有f[0][j] \= abs(wood[0][0] - j)，这个绝对值函数画出来应该是一个V字形。在这里有一个性质是，若j \< wood[0][0]，那么j越靠近wood[0][0]，也就是j越大，对应的f[0][j]就越小。反过来，若j > wood[0][0]，那么j越靠近wood[0][0]，也就是j越小，对应的f[0][j]就越小。

接下来，当i \= 1时，有f[1][j] \= min(f[0][k]) + abs(wood[1][0] - j)。根据i \= 0的结论，在这里可以将f[1][j]写作分段函数的形式，即

1、当j \< wood\[0\]\[0\] - length\[1\]时，f\[0\]\[k\]中k的落点必然是小于wood\[0\]\[0\]的，因此此时的min(f\[0\]\[k\])就是k取最大值，也就是k \= j + length\[1\]，于是就有f\[1\]\[j\] \= f\[0\]\[j + length\[1\]\] + abs(wood\[1\]\[0\] - j)

2、当wood[0][0] - length[1] \<\= j \<\= wood[0][0] + length[0]时，f[0][k]的k都可以选择落在wood[0][0]，此时min(f[0][k])就是0，于是就有f[1][j] \= abs(wood[1][0] - j)

3、当wood\[0\]\[0\] + length\[0\] \< j时，f\[0\]\[k\]中k的落点必然是大于wood\[0\]\[0\]的，因此此时的min(f\[0\]\[k\])就是k取最小值，也就是k \= j - length\[0\]，于是就有f\[1\]\[j\] \= f\[0\]\[j - length\[0\]\] + abs(wood\[1\]\[0\] - j)

可以发现，这里f[1][j]的函数画出来应该是一个某一侧斜边出现了折线，且底部的点被拉长的不规则V形，但是整体还是呈现一个随着j的增加，f[1][j]将逐渐减小，再逐渐增大的过程。不妨设f[1][j]中间取最小值的这一段的起始和终止位置分别为start和end，那么在这里同样具有类似的性质：

1、若j \< start，那么j越靠近start，也就是j越大，对应的f[1][j]就越小

2、若start \<\= j \<\= end，那么这一段中f[1][j]取值相同，且为f[1]的最小值

3、若end \< j，那么j越靠近end，也就是j越小，对应的f[1][j]就越小

那么更一般的，不妨设f[i - 1][j]对应的函数图像依然是不规则V形，且最小值的起止位置为start和end，那么对于f[i][j]：

1、若j \< start - length\[i\]，此时f\[i - 1\]\[k\]中k的落点必然是小于start的，因此当k \= j + length\[i\]时有f\[i - 1\]\[k\]最小，因此就有f\[i\]\[j\] \= f\[i - 1\]\[j + length\[i\]\] + abs(wood\[i\]\[0\] - j)

2、若start - length[i] \<\= j \<\= end + length[i - 1]，此时f[i - 1][k]中k的落点就可以落在start到end之间，此时就有f[i][j] \= f[i - 1][start] + abs(wood[i][0] - j)

3、若end + length\[i - 1\] \< j，此时f\[i - 1\]\[k\]中k的落点必然是大于end的，因此当k \= j - length\[i - 1\]时有f\[i - 1\]\[k\]最小，因此就有f\[i\]\[j\] \= f\[i - 1\]\[j - length\[i - 1\]\] + abs(wood\[i\]\[0\] - j)

---

到了这里，虽然有了上面f[i][j]关于f[i - 1][j]的方程，但是如果一个个值计算的话，时空复杂度以及太高了。

观察f[i][j]的函数，其可以分为f[i - 1]相关的这部分以及绝对值abs(wood[i][0] - j)这部分，在这里不妨尝试分开考虑。对于前面关于f[i - 1]相关的部分，记为part1[i][j]，那么：

当j \< start - length\[i\]时，part1\[i\]\[j\] \= f\[i - 1\]\[j + length\[i\]\]

当start - length[i] \<\= j \<\= end + length[i - 1]时，part1[i][j] \= f[i - 1][start]

当end + length\[i - 1\] \< j时，part1\[i\]\[j\] \= f\[i - 1\]\[j - length\[i - 1\]\]

可以发现，在这里part1\[i\]相当于在part1\[i - 1\]的基础上，将原来的取最小值的区间\[start, end\]扩充到了\[start - length\[i\], end + length\[i - 1\]\]，而其他部分并没有产生变化。那么在这里就可以使用两个偏移量start_bias和end_bias记录当前f对应的start和end在最开始f\[0\]的基础上产生了多少偏移，这样一来就完全不需要关心part1相关的迭代了。

---

接下来，则是需要想办法将part2[i][j] \= abs(wood[i][0] - j)这个绝对值函数叠加到part1这个不规则的V上面去。一个自然的想法是维护V所有折线的两个端点。由于f可以认为是绝对值函数叠加而来的，而题目中绝对值函数关于变量j的斜率要么是1，要么是-1，那么n个叠加在一起，斜率的取值范围就是n到-n，也就是说最多需要维护2n + 1条折线。不过在具体实现上，由于part2[i][j]的最值点wood[i][0]可以落在f[i - 1]这条折线的任意位置，那么相当于需要更新wood[i][0]两侧所有的折线，必须使用某种高级数据结构来处理，实现起来会非常麻烦。

在这里有一个经典的技巧是，不妨认为所有斜率的折线都出现了，那么这里所有折线的斜率就必然是从n开始逐条减1，直到降到0，也就是来到start到end对应的区间，然后再逐条加1，直到增加到n。由于本题我们只需要关心start到end这一段，那么在这里就只需要维护维护这些折线上的所有端点，而无需关心斜率了。当然，在这里可能出现某种斜率并没有出现的情况，此时可以通过加入相同的点，形成一条长度为0的线段来填充对应的斜率。

接下来的问题就是如何更新这些点。

由于在这里我们只需要关心start和end，那么就可以使用两个堆left和right分别维护start和start左侧的点以及end和end右侧的点，其中left为大顶堆，right为小顶堆，那么left和right的堆顶就刚好是start和end这两个点。接下俩，那么对于当前的wood[i][0]：

1、若wood[i][0] \< start，那么start左侧所有的折线斜率都要减上1，同时start自身必然是落在abs(wood[i][0] - j)上升的这一侧的，也就是说start因为这个影响成为了斜率为1的上升折线的起点，此时就需要将start从left移动到right。另一方面，对于wood[i][0]自身而言，将其加入到left中后，其所在折线的右半部分因为abs(wood[i][0] - j)上升这一侧的影响，与wood[i][0]所在折线的左半部分有一个斜率的脱节，那么在这里还需要再将wood[i][0]加入到left中一次，通过构造一条长度为0的线段来规避这个脱节的问题

2、若start \<\= wood[i][0] \<\= end，那么此时相当于在左右两个分别给了一个-1和1的斜率，而新的start和end则都变成了wood[i][0]因此只需将wood[i][0]分别加入left和right就行了

3、若end \< wood[i][0]，此时与情况1完全对称，只需将end从right移动到left，并将wood[i][0]加入到right中两次即可

需要注意的是，由于折线的start和end是受到start_bias和end_bias，因此在上述的堆操作中都必须带着start_bias和end_bias进行操作。

---

到了这里，就可以在O(nlogn)的时间内维护所有的f[i]对应的折线了，但是此时还有一个问题就是，最终这条折线中，start到end这一段对应的f值到底是多少。

回顾一下上面的三种情况：

1、wood[i][0] \< start。在wood[i][0]加入后，新的斜率为1的折线的左端点为原来的start，也就是说f[i][start]依然是f[i]的最小值之一，而start在abs(wood[i][0] - j)这里将使得f[i][start]的取值在原有的f[i - 1][start]的基础上增加start - wood[i][0]，因此此时的最小值就可以在上一轮最小值的基础上加上start - wood[i][0]

2、start \<\= wood[i][0] \<\= end。这种情况下，最小值不会产生变化

3、end \< wood[i][0]。与情况1类似，此时新的斜率为-1的折线的右端点为原来的end，也就是说f[i][end]依然是f[i]的最小值之一，而end在abs(wood[i][0] - j)这里将使得f[i][end]的取值在原有的f[i - 1][end]的基础上增加wood[i][0] - end，因此此时的最小值就可以在上一轮最小值的基础上加上wood[i][0] - end

一开始f[0]对应的最小值显然为0，接下来就随着曲线端点的迭代同步计算这个最小值即可。

最后附上python代码：

```python
class Solution(object):
    def buildBridge(self, num, wood):
        """
        :type num: int
        :type wood: List[List[int]]
        :rtype: int
        """

        left_heap = []
        right_heap = []
        res = 0
        start_bias = 0
        end_bias = 0

        n = len(wood)
        for index in range(n):
            x, y = wood[index]
            if index == 0:
                left_heap.append(-x)
                right_heap.append(x)
            else:
                now_length = y - x
                last_length = wood[index - 1][1] - wood[index - 1][0]
                start_bias -= now_length
                end_bias += last_length

                now_start = -left_heap[0] + start_bias
                now_end = right_heap[0] + end_bias

                if x < now_start:
                    heapq.heappop(left_heap)
                    heapq.heappush(left_heap, start_bias - x)
                    heapq.heappush(left_heap, start_bias - x)
                    heapq.heappush(right_heap, now_start - end_bias)
                    res += now_start - x
                elif now_start <= x <= now_end:
                    heapq.heappush(left_heap, start_bias - x)
                    heapq.heappush(right_heap, x - end_bias)
                else:
                    heapq.heappop(right_heap)
                    heapq.heappush(right_heap, x - end_bias)
                    heapq.heappush(right_heap, x - end_bias)
                    heapq.heappush(left_heap, start_bias - now_end)
                    res += x - now_end

        return res
```
