---
title: "3461. 判断操作后字符串中的数字是否相等I & 3463. 判断操作后字符串中的数字是否相等II"
aliases: ["yiduobo的每日leetcode 3461.判断操作后字符串中的数字是否相等I && 3463.判断操作后字符串中的数字是否相等II", "3461. 判断操作后字符串中的数字是否相等I", "3463. 判断操作后字符串中的数字是否相等II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/math", "leetcode/combinatorics", "leetcode/hard", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1895232522004173149"
zhihu_id: "1895232522004173149"
zhihu_title: "yiduobo的每日leetcode 3461.判断操作后字符串中的数字是否相等I && 3463.判断操作后字符串中的数字是否相等II"
question_id: ["3461", "3463"]
question: ["判断操作后字符串中的数字是否相等 I", "判断操作后字符串中的数字是否相等 II"]
problem_url: ["https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-i/", "https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-ii/"]
difficulty: ["Easy", "Hard"]
rating: 2286
created: "2025-04-14T22:50:10+08:00"
updated: "2025-04-14T22:50:10+08:00"
upvotes: 0
comments: 0
---

# 3461. 判断操作后字符串中的数字是否相等I & 3463. 判断操作后字符串中的数字是否相等II

> **[yiduobo的每日leetcode 3461.判断操作后字符串中的数字是否相等I && 3463.判断操作后字符串中的数字是否相等II](https://zhuanlan.zhihu.com/p/1895232522004173149) · 知乎 · 2025-04-14 · 赞同 0**
> 力扣：[3461. 判断操作后字符串中的数字是否相等 I](https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-i/) · Easy · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3463. 判断操作后字符串中的数字是否相等 II](https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-ii/) · Hard · 灵茶山艾府：[两种方法：欧拉定理 / 扩展 Lucas（Python/Java/C++/Go）](../3463%20判断操作后字符串中的数字是否相等%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3461.判断操作后字符串中的数字是否相等I

[3461. 判断操作后字符串中的数字是否相等 I - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-i/description/)

3463.判断操作后字符串中的数字是否相等II

[3463. 判断操作后字符串中的数字是否相等 II - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-digits-are-equal-in-string-after-operations-ii/description/)

题目给出一个由数字组成的字符串s，重复执行以下操作，直到字符串恰好包含两个数字：

1、从第一个数字开始，对s中的每一对相邻数字，计算这两个数字之和模10

2、使用计算得到的新数字依次替换s的每一个字符，并保持原本的顺序

若s最后剩下的两个数字相同，则返回true，否则返回false。

两题的题设一样，第二题的数据规模较大，s的长度可以来到10^5。

按照题目的数据规模，直接暴力模拟显然是不行的，只能想办法找找规律。

方便起见，在这里不妨先考虑不模10的情况，然后把每一轮的结果都写下来：

| s[0] | s[1] | s[2] | s[3] | s[4] | s[5] | ... | s[-1] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| s[0] +<br>s[1] | s[1] +<br>s[2] | s[2] +<br>s[3] | s[3] + <br>s[4] | s[4] + <br>s[5] | ... | s[-2] +<br>s[-1] |  |
| s[0] + <br>s[1] \* 2 +<br>s[2] | s[1] + <br>s[2] \* 2 +<br>s[3] | s[2] + <br>s[3] \* 2 +<br>s[4] | s[3] + <br>s[4] \* 2 +<br>s[5] | ... | s[-3] +<br>s[-2] \* 2 +<br>s[-1] |  |  |
| s[0] +<br>s[1] \* 3 +<br>s[2] \* 3 +<br>s[3] | s[1] + <br>s[2] \* 3 +<br>s[3] \* 3 +<br>s[4] | s[2] +<br>s[3] \* 3 +<br>s[4] \* 3 +<br>s[5] | ... | s[-4] + <br>s[-3] \* 3 +<br>s[-2] \* 3 +<br>s[-1] |  |  |  |
| s[0] + <br>s[1] \* 4 + <br>s[2] \* 6 +<br>s[3] \* 4 +<br>s[4] | s[1] + <br>s[2] \* 4 +<br>s[3] \* 6 + <br>s[4] \* 4 +<br>s[5] | ... | s[-5] + <br>s[-4] \* 4 +<br>s[-3] \* 6 +<br>s[-2] \* 4 +<br>s[-1] |  |  |  |  |
| ... | ... | ... |  |  |  |  |  |

由于最后得到的两项的计算是对称的，那么在这里不妨先考虑左侧这一项，然后再推广到右侧这一项。

观察最左侧这一列可以发现，每次迭代被累加到这一列中的元素的系数恰好是按照[1]、[1, 1]、[1, 2, 1]、[1, 3, 3, 1]、[1, 4, 6, 4, 1]、...，这样排布下来的。更具体的，对于s中原始的第k项，若k不为s的最后一项，那么其在最后得到的s[0]中出现的次数为C(n - 2, k)，其中n为s的长度。

这是找规律得到出来的式子，当然也可以有更形式化的证明。对于s中原始的第k项，其在第一次迭代中将被累加到第k - 1项以及第k项各一次，在第二次迭代中将被累加到第k - 2项一次，第k - 1项两次，第k项一次，在第三次迭代中将被累加到第k - 3项一次，第k - 2项三次，第k - 1项三次，第k项一次，以此类推。在这里就可以认为是上述的[1]、[1, 1]、[1, 2, 1]、[1, 3, 3, 1]、...，这些次数，按第k项为右侧边界对齐。由于长度为n的s一共会迭代n - 2轮，因此最后这一行迭代完的结果就是按照[C(n - 2, 0), C(n - 2, 1) , ..., C(n - 2, n - 2)]这样排布的。又由于最后一项C(n - 2, n - 2)是对齐的第k项，那么最左侧，也就是第0项就是C(n - 2, n - 2 - k)，等价于C(n - 2, k)。

---

到了这里，就得到了原始的s中每一项累加的系数，接下来需要计算这些项乘以系数累加起来模10的结果。由于n的规模很大，那么在计算C(n - 2, k)的时候需要边算边取模，不可避免的又涉及到了乘法逆元。不过需要特别注意的是，本题中是对10取模，而10不是质数，因此之前的很多方法都不在适用。

一般的方法应该是利用欧拉函数来处理，不过本题中这个10也是很特殊的，可以想办法分解出2和5来进行计算。具体来说，对于C(n - 2, k) \= (n - 2)! / (k! \* (n - 2 - k)!)，需要计算的依然是除号下方的两项阶乘在模10下的逆元，在这里就可以先对式子中的这些阶乘先分离出所有的因子2以及因子5，那么对于分离完所有的2和5之后得到的值v，记inv[v]为v在模10下的逆元，那么显然有inv[v] ≡ inv[v % 10] (mod 10)，又由于v中已经不包含因子2和因子5，因此v % 10只可能是1、3、7、9这四种值之一。接下来只需手动凑一凑，就可以得到

inv[1] ≡ 1 (mod 10)

inv[3] ≡ 7 (mod 10)

inv[7] ≡ 3 (mod 10)

inv[9] ≡ 9 (mod 10)

接下来对于C(n - 2, k)，记f[x]为x!中分离掉所有的因子2和因子5之后，再模10得到的结果。对于f的计算，可以一趟遍历，对于当前遍历到的v，先通过不断模2和模5的操作分离掉v中的2和5，然后通过f[-1] \* v % 10得到对应的f[v]，在这个过程中还可以顺便计算x!中因子2和因子5的数量p2以及p5。

在不考虑因子2和因此5的情况下，可以先计算c \= f\[n - 2\] \* inv\[f\[k\]\] \* inv\[f\[n - 2 - k\]\] % 10，也就是C(n - 2, k)去除掉所有因子2和因此5之后模10的结果。

接下来考虑分子和分母中因子2和因子5的数量之差sp2以及sp5，这两个值可以通过p2以及p5得到，那么：

1、若sp2 > 0且sp5 > 0：

此时的式子中包含因子2和因子5至少各一个，因此式子必然是10的倍数，模10之后的结果为0

2、若sp2 > 0且sp5 \= 0：

C(n - 2, k) ≡ 2^sp2 \* c % 10 (mod 10)

对于前面的2^sp2，其模10的取值会按照[2, 4, 8, 6]的次序循环。记p2_mod \= [2, 4, 8, 6]，那么就可以通过p2_mod[(sp2 - 1) % 4]来得到2^sp2 % 10的结果，因此最终结果为

C(n - 2, k) ≡ p2_mod[(sp2 - 1) % 4] \* c (mod 10)

3、若sp2 \= 0且sp5 > 0:

由于5的任意次方模10都等于5，因此此时就有

C(n - 2, k) ≡ 5 \* c (mod 10)

4、若sp2 \= 0且sp5 \= 0：

此时没有2和5的影响，直接就有

C(n - 2, k) ≡ c (mod 10)

---

有了上面的结果，就可以初始化最左侧加和left为s[0]，然后从下标1开始遍历到n - 2，分别计算对应的C(n - 2, k)模10的余数，再乘以对应的元素值后累加到left中即可。

而对于最右侧加和right的计算，按照上面第k项对齐的思路可以发现，其在第n - 2次迭代时在第n - 1项中作用的次数就应该是C(n - 2, n - 1 - k)，因此按相同的处理方法一趟遍历，计算出对应的c，然后根据分子和分母中2和5的数量计算出最终C(n - 2, n - 1 - k)模10的余数，再乘以对应的元素之后累加到right中即可。

全部计算完成后，对于left是否等于right即可得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def hasSameDigits(self, s):
        """
        :type s: str
        :rtype: bool
        """
        
        p2 = [0]
        p5 = [0]
        num = [1]
        f = [1]

        n = len(s)
        for v in range(1, n - 1):
            p2.append(p2[-1])
            p5.append(p5[-1])
            while v % 2 == 0:
                p2[-1] += 1
                v //= 2
            while v % 5 == 0:
                p5[-1] += 1
                v //= 5
            num.append(v)
            f.append(f[-1] * v % 10)
        
        inv = {1: 1, 3: 7, 7: 3, 9: 9}
        p2_mod = [2, 4, 8, 6]

        left = int(s[0])
        for index in range(1, n - 1):
            c = f[n - 2] * inv[f[index]] * inv[f[n - 2 - index]] % 10
            sp2 = p2[n - 2] - p2[index] - p2[n - 2 - index]
            sp5 = p5[n - 2] - p5[index] - p5[n - 2 - index]
            if sp2 > 0:
                if sp5 > 0:
                    c = 0
                else:
                    c *= p2_mod[(sp2 - 1) % 4]
                    c %= 10
            elif sp5 > 0:
                c *= 5
                c %= 10
            
            left += int(s[index]) * c
            left %= 10
        
        right = int(s[-1])
        for index in range(1, n - 1):
            c = f[n - 2] * inv[f[index - 1]] * inv[f[n - 1 - index]] % 10
            sp2 = p2[n - 2] - p2[index - 1] - p2[n - 1 - index]
            sp5 = p5[n - 2] - p5[index - 1] - p5[n - 1 - index]
            if sp2 > 0:
                if sp5 > 0:
                    c = 0
                else:
                    c *= p2_mod[(sp2 - 1) % 4]
                    c %= 10
            elif sp5 > 0:
                c *= 5
                c %= 10
            
            right += int(s[index]) * c
            right %= 10
        
        return left == right
```
