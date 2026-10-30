---
title: "LCP 38. 守卫城堡"
aliases: ["yiduobo的每日leetcode LCP38.守卫城堡"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/575338115"
zhihu_id: "575338115"
zhihu_title: "yiduobo的每日leetcode LCP38.守卫城堡"
question_id: "LCP 38"
question: "守卫城堡"
problem_url: "https://leetcode.cn/problems/7r/"
created: "2022-10-20T05:37:08+08:00"
updated: "2022-10-20T05:37:08+08:00"
upvotes: 0
comments: 0
---

# LCP 38. 守卫城堡

> **[yiduobo的每日leetcode LCP38.守卫城堡](https://zhuanlan.zhihu.com/p/575338115) · 知乎 · 2022-10-20 · 赞同 0**
> 力扣：[LCP 38. 守卫城堡](https://leetcode.cn/problems/7r/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP38.守卫城堡

[力扣](https://leetcode.cn/problems/7rLGCR/)

之前有提到过，这类棋盘格问题的一个常规解法是转化为二分图然后做网络流求解。不过对于本题，由于列数高达10000，那么跑网络流大概率会有时间效率的问题，只能老老实实用状态压缩动态规划来处理。

如果要使用动态规划，有一个比较难处理的点就是传送门。本题的传送门与常规传送门不同，并不是两两成对而是到处连通的，也正是基于这一点，可以使用一个替代方案。

由于所有传送门都连通，那么一旦有一座传送门失守，相当于所有传送门都沦陷了，于是在一开始就可以决定一个大方针，即防守城堡以及所有传送门，或者仅防守城堡。

对于前者，就可以视所有传送门为城堡，必须防止恶魔到达任意城堡。

对于后者，则可以视所有传送门为恶魔，只需防止恶魔到达唯一的城堡。

到了这里，问题就简化成了地图上有空地、障碍、恶魔、城堡四种元素，问能否通过增加障碍使得恶魔无法到达任意城堡。令f[i][state]表示前i列，两行的地图元素组成为state，且恶魔无法到达城堡，所需增加的最小障碍数量。这里的state为两位的4进制数，分别是0对应空地，1对应障碍，2对应恶魔能够到达当前列的这一行，3对应从当前列的这一行出发可以到达某座城堡。

可以发现，实际上可以操作的空间只有当前列的两行中存在有空地时，可以选择是否增加障碍。另外，如果当前列的两行中，一行是空地，另一行是恶魔或者城堡，如果选择不在空地上增加障碍，那么就需要将空地的这一行同样视为恶魔或者城堡。

除此之外，对于其他的地图元素，是无法进行任何操作的。

那么对于f[i]：

1、首先通过grid[0][i]和grid[1][i]获取当前列的地图元素，分别记为first和second

2、若first + second \= 5，那么说明当前列的两行中一行是恶魔，另一行是城堡，此时没有任何操作空间，因为恶魔已经到达城堡了

3、否则就枚举上一轮的所有合法状态prev_state。对于边界情况，即i \= 0时，prev_state可以默认为0。

对于prev_state，同样是先计算出上一轮的两行prev_first以及prev_second。若prev_first + first \= 5，或者prev_second + second \= 5，那么说明要么是恶魔从上一轮到达了这一轮的城堡，要么是恶魔从这一轮出发往前走到达了之前的某个城堡，无论哪种情况都是不行的，因此直接跳过这个prev_state

接下来，考虑当前这一轮可能出现的状态。在这里使用两个数组first_candidate与second_candidate记录当前这一列的两行可能出现的状态。

首先是第一行。

只有当first \= 0，即当前列的第一行是空地时，才有一些操作空间：

3-1）若prev_first是0或1时，即上一列的第一行是空地或者石头，那么当前列的这一行就可以保持不变。此时可以将[0, 0]加入到first_candidate中，表示当前列是空地，没有增加额外障碍物的代价

3-2）若prev_first是2或3时，即恶魔可以到达上一列的第一行，或者可以通过上一列的第一行到达之前的城堡，那么由于当前列的第一行是空地，因此同样可以让恶魔到达当前列的第一行，或者通过当前列的第一行到达之前的城堡。此时就应该将[prev_first, 0]加入到first_candidate中，表示当前列沿袭了上一列的地图元素，没有增加额外障碍物的代价

3-3）无论之前是什么情况，对于当前列总是可以在第一行设置额外的障碍物，那么也应该将[1, 1]加入到first_candidate中，表示在当前列的第一行设置额外的障碍物，代价为1

另外，当first !\= 0时，当前列第一行的状态就只能是first，那么在这种情况下，则需要将[first, 0]加入到candidate中，表示当前列的第一行地图元素是first，同时没有设置障碍物的代价

接下来对于第二行，所有操作与第一行完全对称，这里就不展开了

4、得到first_candidate和second_candidate后，则可以两两枚举其中的状态，组合得到本列的最终状态。对于枚举到的[first_state, first_cost]和[second_state, second_cost]：

4-1）若first_state + second_state \= 5，说明这种情况下让恶魔到达了城堡，是不合法的状态，直接跳过

4-2）若first_state和second_state中有一方等于0，即空地，而另一方大于等于2，即为城堡或者恶魔，那么需要将空地这一方同样视为城堡或者恶魔，因为可以通过空地上下移动，到达另一方。于是在编码最终的state时需要注意不能依然按照0进行编码，而需要按照上下两列都是恶魔或者都是城堡来进行编码

4-3）其他情况下，则按照常规的编码方式进行编码

得到当前组合下的编码state后，则有

f[i][state] \= min(f[i][state], f[i - 1][prev_state] + first_cost + second_cost)

其含义为从上一列，两行的状态为prev_state这种情况下变为当前列state这种状态，同时为了达成state需要first_cost来为第一行设置障碍，second_cost来为第二行设置障碍。

所有列都遍历完成后，min(f[-1])就是当前大方针下的答案了。

分别按照防守传送门和放弃传送门的大方针进行两轮动态规划，二者答案中的较小值就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def guardCastle(self, grid):
        """
        :type grid: List[str]
        :rtype: int
        """

        n = len(grid[0])

        def check():
            f = [[None] * 16 for _ in range(n)]
            for i in range(n):
                first = mapping[grid[0][i]]
                second = mapping[grid[1][i]]
                if first + second == 5:
                    return n * 2 + 1

                if i == 0:
                    max_prev_state = 0
                else:
                    max_prev_state = 15
                for prev_state in range(max_prev_state + 1):
                    prev_first = prev_state / 4
                    prev_second = prev_state % 4
                    if prev_first + first == 5 or prev_second + second == 5:
                        continue

                    if i > 0 and f[i - 1][prev_state] is None:
                        continue
                    
                    if i == 0:
                        last_w = 0
                    else:
                        last_w = f[i - 1][prev_state]

                    first_candidate = []
                    second_candidate = []

                    if first == 0:
                        if prev_first == 0 or prev_first == 1:
                            first_candidate.append([0, 0])    
                        else:
                            first_candidate.append([prev_first, 0])
                        first_candidate.append([1, 1])
                    else:
                        first_candidate.append([first, 0])
                    
                    if second == 0:
                        if prev_second == 0 or prev_second == 1:
                            second_candidate.append([0, 0])
                        else:
                            second_candidate.append([prev_second, 0])
                        second_candidate.append([1, 1])
                    else:
                        second_candidate.append([second, 0])

                    for first_state, first_cost in first_candidate:
                        for second_state, second_cost in second_candidate:
                            if first_state + second_state == 5:
                                continue
                            if first_state == 0 and second_state >= 2:
                                state = second_state * 4 + second_state
                            elif second_state == 0 and first_state >= 2:
                                state = first_state * 4 + first_state
                            else:
                                state = first_state * 4 + second_state
                            
                            if f[i][state] is None or f[i][state] > last_w + first_cost + second_cost:
                                f[i][state] = last_w + first_cost + second_cost

            res = n * 2 + 1
            for state in range(16):
                if f[-1][state] is not None:
                    res = min(res, f[-1][state])
            
            return res

        res = n * 2 + 1
        mapping = {}
        mapping['.']=  0
        mapping['#'] = 1
        mapping['S'] = 2
        mapping['C'] = 3
        mapping['P'] = 2
        res = min(res, check())
        mapping['P'] = 3
        res = min(res, check())
        
        if res == n * 2 + 1:
            res = -1
        return res
```
