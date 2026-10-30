---
title: "3015. 按距离统计房屋对数目I & 3017. 按距离统计房屋对数目II"
aliases: ["yiduobo的每日leetcode 3015.按距离统计房屋对数目I && 3017.按距离统计房屋对数目II", "3015. 按距离统计房屋对数目I", "3017. 按距离统计房屋对数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/图论算法", "题单/图论算法/一-图的遍历", "leetcode/hard", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/二-差分", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/694393501"
zhihu_id: "694393501"
zhihu_title: "yiduobo的每日leetcode 3015.按距离统计房屋对数目I && 3017.按距离统计房屋对数目II"
question_id: ["3015", "3017"]
question: ["按距离统计房屋对数目 I", "按距离统计房屋对数目 II"]
problem_url: ["https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/", "https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-ii/"]
difficulty: ["Medium", "Hard"]
rating: ["1658", "2709"]
created: "2024-04-25T02:28:21+08:00"
updated: "2024-04-25T02:28:21+08:00"
upvotes: 1
comments: 0
---

# 3015. 按距离统计房屋对数目I & 3017. 按距离统计房屋对数目II

> **[yiduobo的每日leetcode 3015.按距离统计房屋对数目I && 3017.按距离统计房屋对数目II](https://zhuanlan.zhihu.com/p/694393501) · 知乎 · 2024-04-25 · 赞同 1**
> 力扣：[3015. 按距离统计房屋对数目 I](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/) · Medium · 灵茶山艾府：[非暴力做法：差分数组+分类讨论（Python/Java/C++/Go）](../3015%20按距离统计房屋对数目%20I/灵茶山艾府.md)
> 力扣：[3017. 按距离统计房屋对数目 II](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-ii/) · Hard · 灵茶山艾府：[两种分类讨论思路（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3015.按距离统计房屋对数目I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/description/)

3017.按距离统计房屋对数目II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-ii/description/)

题目给出一个1到n排列好的数组，其中相邻的数之间存在一条道路。另外再给出两个数x和y，x和y之间也存在一条道路，接下来计算从每个点出发到达其他所有点的最短距离，问每种最短距离出现的次数。

两个题目的题目描述是一样的，3017的数据规模比较大，必须使用O(n)或者O(nlogn)的算法。

为了方便计算，在这里规定x \< y，若不满足直接交换二者就行了，不影响最终结果的计算。

首先考虑特殊情况。若x \= y或者x \= y - 1，那么相当于不存在这条近路，这种情况可以参考样例3。观察结果可以发现是存在很明显的规律的。更进一步的，对于n个节点，其中存在n - 1组距离为1的数对，n - 2组距离为2的数对，以此类推，直到最后的唯一一对距离为n - 1的数对(1, n)，因此最终答案为[(n - 1) \* 2, (n - 2) \* 2, ..., 2, 0]。

---

接下来考虑存在有效近路的情况。加入近路后，题目中的数可以拆分成三个部分：

第一个部分就是x到y之间的数形成的环。

环的长度circle_len可以通过y - x + 1计算得到，那么对于一个长度为circle_len的环。

当circle_len为奇数时，从任意节点出发，向两个方向行走，可以得到两组距离为1的数对，两组距离为2的数对，以此类推，直到最后的两组距离为(circlen_len - 1) / 2的数对。

当circle_len为奇数时，同样是从任意节点出发，向两个方向行走。不过在这里每个数都存在唯一的对角数，因此对于每个数存在唯一一组距离为circle_len / 2的数对，而距离为1到circle_len / 2 - 1的数对则同样存在两组。

计circle_max_dis为环中的最大距离，那么当circle_len为奇数时，一共有circle_len \* 2组大小为1到circle_max_dis的距离；当circle_len为偶数时，一共有circle_len \* 2组大小为1到circle_max_dis - 1的距离，另外还有circle_len组对角数的距离circle_max_dis。

例如circle_len为3时，答案就是[6, 0, 0]；circle_len为4时，答案就是[8, 4, 0, 0]；circle_len为5时，答案就是[10, 10, 0, 0, 0]；circle_len为6时，答案就是[12, 12, 6, 0, 0, 0]。

---

第二个部分是1到x，然后x到y，最后y到n形成的链。

对于链的情况，在最开始的特殊情况中已经说明了。在这里需要特别注意的是，x到y这一段在环中已经计算过了，在链中也会计算以此，因此最后距离为1的情况需要减去2。

---

最后这个部分就是1到x - 1以及y + 1到n这些链上的数，到环中除了x和y之外的数的路径。

这种情况相对比较复杂，而且也不太好找规律。

例如从x - 1出发，到x + 1, x + 2, ..., y - 1这些数的距离。在这里没有x和y的理由是这些距离在第二种情况中已经计算过了。

与环中计算的方式一样，在这里同样可以从x和y两个方向同时出发行走，那么在这里就可以利用第一个部分中的计算方式。

根据第一个部分中的结论，从x出发走到环中的其他数，通过环长度circle_len的奇偶性可以分为两种情况，而从x - 1出发的情况，则可以视为从x - 1到x，然后再从x走到环中的其他数。需要注意的是，在这里需要去除掉x - 1到x以及x - 1到y这两种情况，也就是减去一个距离为1的情况以及距离为2的情况。

更进一步的，对于处于1到x - 1中的数index，同样可以先走x - index步走到x，然后再利用第一个部分的结论。但是有一个问题就是第一个问题中的结论并不是很整齐，因此在累加的时候还是很麻烦的。

既然找规律的方法不太好使，那么不妨来点算法的东西。

可以发现，从每个节点出发的距离都必然是连续的，那么对于从某个点出发的距离为1到k的结果，可以视为在答案数组中的1到k中每个数都加上1，这是一个非常典型的静态区间修改，最后单点求值的情况，是非常适合用差分数组的。

对于上面的情况，从index到x的距离为x - index，接下来环中的两条路线可以拆分开来，一条是1到circle_max_dis，另一条则需要根据环的长度来确定：当环长度为偶数时，另一条的长度就是1到circle_max_dis - 1，反之依然是1到circle_max_dis。

叠加上x - index的距离，再去除掉index到x以及index到y这两个大小为x - index和x - index + 1的距离，那么最终的区间就应该是x - index + 1到x - index + circle_max_dis，以及x - index + 2到x - index + circle_max_dis或者x - index + 2到x - index + 2 + circle_max_dis - 1。

另一侧对于y + 1到n中的index，计算方式也是一样的，不过叠加的距离应该是index - y。

---

在实现上为了统一，对于第一个部分和第二个部分中的距离也可以修改成差分数组的形式，三个部分都计算完毕后，一趟遍历计算每种距离出现的次数即可。

最后附上python代码：

```python
class Solution(object):
    def countOfPairs(self, n, x, y):
        """
        :type n: int
        :type x: int
        :type y: int
        :rtype: List[int]
        """

        if x > y:
            x, y = y, x
        
        if y - x <= 1:
            return [(index - 1) * 2 for index in range(n, 0, -1)]
        
        delta = [0] * (n + 1)
        circle_len = y - x + 1
        circle_dis_max = circle_len // 2
        delta[1] += circle_len * 2
        delta[circle_dis_max + 1] -= circle_len
        if circle_len % 2 == 0:
            delta[circle_dis_max] -= circle_len
        else:
            delta[circle_dis_max + 1] -= circle_len
        
        chain_len = x - 1 + n - y + 2
        for index in range(1, chain_len):
            delta[1] += 2
            delta[chain_len - index + 1] -= 2
        delta[1] -= 2
        delta[2] += 2

        for index in range(x - 1, 0, -1):
            delta[x - index + 1] += 2
            delta[x - index + circle_dis_max + 1] -= 2
            delta[x - index + 2] += 2
            if circle_len % 2 == 0:
                delta[x - index + circle_dis_max] -= 2
            else:
                delta[x - index + circle_dis_max + 1] -= 2

        for index in range(y + 1, n + 1):
            delta[index - y + 1] += 2
            delta[index - y + circle_dis_max + 1] -= 2
            delta[index - y + 2] += 2
            if circle_len % 2 == 0:
                delta[index - y + circle_dis_max] -= 2
            else:
                delta[index - y + circle_dis_max + 1] -= 2

        v = 0
        res = []
        for index in range(1, n + 1):
            v += delta[index]
            res.append(v)
        
        return res
```
