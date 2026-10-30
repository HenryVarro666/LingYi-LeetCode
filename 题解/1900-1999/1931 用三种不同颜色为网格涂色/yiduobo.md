---
title: "1931. 用三种不同颜色为网格涂色"
aliases: ["yiduobo的每日leetcode 1931.用三种不同颜色为网格涂色"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/matrix", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/动态规划/十一-优化-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/487729817"
zhihu_id: "487729817"
zhihu_title: "yiduobo的每日leetcode 1931.用三种不同颜色为网格涂色"
question_id: "1931"
question: "用三种不同颜色为网格涂色"
problem_url: "https://leetcode.cn/problems/painting-a-grid-with-three-different-colors/"
difficulty: "Hard"
rating: 2170
created: "2022-03-25T23:32:21+08:00"
updated: "2022-03-25T23:32:21+08:00"
upvotes: 0
comments: 0
---

# 1931. 用三种不同颜色为网格涂色

> **[yiduobo的每日leetcode 1931.用三种不同颜色为网格涂色](https://zhuanlan.zhihu.com/p/487729817) · 知乎 · 2022-03-25 · 赞同 0**
> 力扣：[1931. 用三种不同颜色为网格涂色](https://leetcode.cn/problems/painting-a-grid-with-three-different-colors/) · Hard · 灵茶山艾府：[四种方法：记忆化搜索/递推/矩阵快速幂/BM+Kitamasa（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1931.用三种不同颜色为网格涂色

[力扣](https://leetcode-cn.com/problems/painting-a-grid-with-three-different-colors/)

很有意思的题目，之前应该做过一题是三种颜色填充m \= 3的网格的方案数。这两题都可以使用状态压缩动态规划来做，不过还存在更好的方法。

对于m \= 3的这一题，当时应该是分情况讨论得出了递推公式，然后使用矩阵乘法加快速幂来求解的。对于本题，也可以想办法找出递推公式，但是m \= 5时手动推理就比较困难了，此时则可以借助代码来做一些简单的推理。

首先，需要明确一个概念是本质相同的状态。

例如三个格子中的rbr以及brb，就可以认为是本质相同的。用代码来描述，就是状态中r、g、b中任意两者或者三者进行互换，最终可以得到相同的状态。

除此之外，正反逆序也可以认为本质相同的状态，例如四个格子的rgrb以及brgr。更进一步的，正反逆序加上字符互换同样是本质相同的状态。

在这里定义本质相同状态的原因是这些状态进行状态转移时，下一轮的状态也是本质相同的，从而将分情况讨论的情况数缩减到比较小的规模。

例如m \= 3时，本质不同的状态只有rgr以及rgb这两种，而每种本质不同的状态都包含6个亚种，即

rgr，rbr，grg，gbg，brb，bgb

rgb，rbg，grb，gbr，brg，bgr

如果不对本质相同的状态进行归类，那么递推式中的每一轮都要在这12种状态计算，而对于本质相同的状态，则只有两种需要计算。

而对于本质不同的状态，在这里则可以借助代码来求解。直接一趟dfs，若当前状态在数字互换以及正反逆序后与之前的某个状态一样，那么就将这两个状态归于一类，并建立状态之间的映射。

对于m \= 4的情况，本质不同的状态只有rgrg、rgrb以及rgbr这三种，分别包含6、12、6个亚种

对于m \= 5的情况，本质不同的状态只有rgrgr、rgrgb、rgrbr、rgrbg、rgbrg以及rgbgr，分别包含6、12、6、12、6、6个亚种

可以发现，即使是m \= 5的情况，最终也只是6种状态之间相互倒来倒去，而如果不进行状态归类，则需要梳理48种状态的递推关系。

接下来的问题是如何找到递归关系。设本质不同的状态有l种，那么可以构造出一个l \* l的矩阵base，其中base[i][j]表示如果上一行是本质不同状态中的第i个，那么一共有base[i][j]个亚种归类到本质不同状态中的第j个。

这里以m \= 3的情况举例，需要构造一个2 \* 2的矩阵base。对于base[0][0]，表示的是上一行是rgr形式的状态，那么下一行同样是rgr形式的状态有多少种可能。

在这里很容易得知rgr下一行依然是rgr这种状态有grg、gbg、brb，那么就有base[0][0] \= 3

而对于base[0][1]，表示的则是从rgr这种状态到下一行是rgb这种状态的数目，那么从rgr可以得到grb、brg这两种可行的状态，那么就有base[0][1] \= 2

对于base[1][0]以及base[1][1]也是如法炮制。

当然，上面的例子m \= 3，可以手动枚举，当m更大的时候就需要借助代码帮忙了。对于每种本质不同的状态，都执行一次dfs，计算其下一行可行的本质不同状态有哪些，以及有多少个。

得到base之后，first \* base \* base \* ... \* base就能得到m行n列最终每种本质不同状态的数目，对其求和就是最终答案。而对于上面这个式子，base幂次显然可以用快速幂来进行优化，于是最终的时间复杂度为O(l \* 3^m + l^3 \* log(n))，当m \= 5时l为6，可以认为是很不错的时间复杂度了。

本题给的一个启发是对于找规律类型的题目，在手动推导较繁琐的情况下完全可以借助代码完成部分规律的推导，而不是说找规律的题目就只能靠手动计算找出规律，然后根据规律写出代码。

最后附上python代码：

```python
class Solution(object):
    def colorTheGrid(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """

        self.mod = 10 ** 9 + 7
        if m == 1:
            return 3 * sum(self.quickPow([[2]], 1, n - 1)[-1]) % self.mod
        elif m == 2:
            return 2 * sum(self.quickPow([[3]], 1, n)[-1]) % self.mod
        else:
            self.replace_list = [{0: 1, 1: 0}, {0: 2, 2: 0}, {1: 2, 2: 1}, {0: 1, 1: 2, 2: 0}, {0: 2, 2: 1, 1: 0}]
            self.pow3 = [1]
            for _ in range(m):
                self.pow3.append(self.pow3[-1] * 3)
            self.color_mapping = {}
            color_dict = {}
            
            self.dfs(0, m, [], -1, color_dict)

            color_info = color_dict.items()
            l = len(color_info)
            first_line = []
            color_index = {}
            base = [[0] * l for _ in range(l)]
            
            for index, (color, cnt) in enumerate(color_info):
                first_line.append(cnt)
                color_index[color] = index
            
            for color, cnt in color_info:
                next_line_color = {}
                self.dfs(0, m, [], color, next_line_color)
                for next_color, next_cnt in next_line_color.items():
                    base[color_index[color]][color_index[next_color]] = next_cnt

            final = self.quickPow(base, l, n - 1)
            res = [0] * l
            for i in range(l):
                for j in range(l):
                    res[j] += first_line[i] * final[i][j]
                    res[j] %= self.mod

            return sum(res) % self.mod
    
    def quickPow(self, base, l, n):
        if n == 0:
            ret = [[0] * l for _ in range(l)]
            for i in range(l):
                ret[i][i] = 1
            return ret

        if n == 1:
            return base
        
        tmp = self.quickPow(base, l, n / 2)
        ret = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    ret[i][k] += tmp[i][j] * tmp[j][k]
                    ret[i][k] %= self.mod
        
        if n % 2 == 0:
            return ret
        
        tmp = [[0] * l for _ in range(l)]
        for i in range(l):
            for j in range(l):
                for k in range(l):
                    tmp[i][k] += ret[i][j] * base[j][k]
                    tmp[i][k] %= self.mod
        return tmp

    def check(self, num, final, color_dict):
        if num in color_dict:
            self.color_mapping[final] = num
            color_dict[num] += 1
            return True

        if num in self.color_mapping:
            self.color_mapping[final] = self.color_mapping[num]
            color_dict[self.color_mapping[final]] = color_dict.get(self.color_mapping[final], 0) + 1
            return True
        
        return False

    def dfs(self, level, m, now, last_line, color_dict):
        if level == m:
            final = 0
            reverse_final = 0
            for index, x in enumerate(now):
                final = final * 3 + x
                reverse_final += x * self.pow3[index]
            
            if self.check(final, final, color_dict) or self.check(reverse_final, final, color_dict):
                return

            for mapping in self.replace_list:
                num = 0
                reverse_num = 0
                for index, x in enumerate(now):
                    num = num * 3 + mapping.get(x, x)
                    reverse_num += mapping.get(x, x) * self.pow3[index]
                
                if self.check(num, final, color_dict) or self.check(reverse_num, final, color_dict):
                    return

            color_dict[final] = 1
            return

        for x in range(3):
            if last_line >= 0 and last_line / self.pow3[m - level - 1] % 3 == x:
                continue
            if level > 0 and now[-1] == x:
                continue
            now.append(x)
            self.dfs(level + 1, m, now, last_line, color_dict)
            now.pop()
```
