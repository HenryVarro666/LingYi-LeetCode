---
title: "3116. 单面值组合的第K小金额"
aliases: ["yiduobo的每日leetcode 3116.单面值组合的第K小金额"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "leetcode/binary-search", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/二分算法", "题单/数学算法", "题单/二分算法/二-二分答案", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701260756"
zhihu_id: "701260756"
zhihu_title: "yiduobo的每日leetcode 3116.单面值组合的第K小金额"
question_id: "3116"
question: "单面值组合的第 K 小金额"
problem_url: "https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/"
difficulty: "Hard"
rating: 2387
created: "2024-06-03T01:10:38+08:00"
updated: "2024-06-03T01:10:38+08:00"
upvotes: 1
comments: 0
---

# 3116. 单面值组合的第K小金额

> **[yiduobo的每日leetcode 3116.单面值组合的第K小金额](https://zhuanlan.zhihu.com/p/701260756) · 知乎 · 2024-06-03 · 赞同 1**
> 力扣：[3116. 单面值组合的第 K 小金额](https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/) · Hard · 灵茶山艾府：[二分答案+容斥原理+预处理（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3116.单面值组合的第K小金额

[. - 力扣（LeetCode）](https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/description/)

题目给出若干种面值互不不同且小于等于25的硬币，硬币的种类数量不超过15种，且单独某种硬币的数量都是无限的，问仅通过单独某种硬币可以组成的所有面值中，第k小的面值是多少。

由于题目中的k取值范围可以到2 \* 10^9，因此暴力法显然是行不通的，需要进行优化。

观察样例2，可以发现以coin的两种面值2和5的最小公倍数10为界，各种组合在不断循环。例如前几轮的价值循环为

2、4、5、6、8、10

12、14、15、16、18、20

22、24、25、26、28、30

以此类推

根据这一点，不妨设所有硬币面值的最小公倍数为tot_l，就可以先计算在1到tot_l中有多少种面值可以被单种硬币组合出来，记为tot，然后就可以通过计算k除以tot再乘以tot_l计算出答案中处于靠前的循环中的部分，最后对于k对tot取模剩下的余数，计算其在最后这次循环中处于什么位置。

对于前面这个问题，考虑的是在1到tot_l中有多少中面值可以被组合出来，而对于后面这个问题，则可以通过二分法，同样转化为给出一个面值mid，计算在1到mid中有多少个面值可以被组合出来，然后通过对比这个数量与k对tot取模的结果的大小来更新二分的上下界。

换言之，在这里实际上只需要考虑一个问题，即对于面值v，在1到v之间有多少种面值可以被单种硬币组合出来。

---

不妨设硬币的面值分别为coins[0]、coins[1]、...、coins[n - 1]，那么在1到v之间可以整除这些面值的面值数目分别为v // coins[0]、v // coins[1]、...、v // coins[n - 1]。但是需要注意的是，在这里是可能出现重复计算的，例如2的倍数2、4、6、...，以及3的倍数3、6、9、...，6就会被计算两次，需要考虑去重。

1、首先，在1到v之间可以整除coins[0]、coins[1]、...、coins[n - 1]的面值数量分别为v // coins[0]、v // coins[1]、...、v // coins[n - 1]，可以先将这些数量累加起来。

2、接下来，对于所有同时为coins[i]、coins[j]的倍数的面值数量为v // L[(i, j)]，这里的L[(i, j)]表示的是coins[i]和coins[j]的最小公倍数，且满足i \< j。

对于这些面值，其在步骤1中计算v // coins[i]以及v // coins[j]都被计算了一次，因此对于所有可以整除L[(0, 1)]、L[(0, 2)]、...、L[0, n - 1)]、L[(1, 2)]、L[(2, 2)]、...、L[(2, n - 1)]、...、L[(n - 1, n)]的面值，都应该少计算一次，于是此时就应该分别计算v除以上面L的结果，并将其从答案中减去。

3、接下来，对于所有同时为coins[i]、coins[j]、coins[k]的倍数的面值数量为v // L[(i, j, k)]，这里的L[(i, j, k)]表示的是coins[i]、coins[j]、coins[k]的最小公倍数，且满足i \< j \< k。

对于这些面值，其在步骤1中计算v // coins[i]、v // coins[j]、v // coins[k]时都被计算了一次，即计算了3次。

另一方面，其在步骤2中计算v // L[(i, j)]、v // L[(i, k)]、v // L[(j, k)]时都被少算了一次，即少算了3次。

一来一去，最终对于所有可以整除L[(i, j, k)]的面值，都应该多计算一次。

可以猜测，是不是对于奇数种不同coins的最小公倍数，所有可以整除这种最小公倍数的面值都应该多计算一次，而对于偶数种不同coins的最小公倍数，所有可以整除这种最小公倍数的面值都应该少计算一次。

下面给出证明。不妨设L为c[0]、c[1]、...、c[m - 1]这m种不同面值的最小公倍数，那么在计算c[0]、c[1]、...、c[m - 1]这m中单独的倍数时，被计算了C(m, 1)次，在计算恰好为两种coins的最小公倍数时，被少计算了C(m, 2)次，以此类推。

换言之，当m为奇数时，之前计算的次数为

C(m, 1) - C(m, 2) + C(m, 3) - ... - C(m, m - 1)

由于C(m, i) \= C(m, m - i)，因此上面这个式子的结果恰好为0，也就是说当m为奇数时，需要多计算1次。

另一方面，当m为偶数时，之前计算的次数为

C(m, 1) - C(m, 2) + C(m, 3) - ... + C(m, m - 1)

在这里需要用到二项式定理，令S \= (-1 + 1)^m，那么就有

S \= C(m, 0) \* (-1)^m + C(m, 1) \* (-1)^(m - 1) + ... + C(m, m) \* (-1)^0 \= 0

由于m为偶数，那么就有

S \= C(m, 0) - C(m, 1) + C(m, 2) - ... - C(m, m - 1) + C(m, m) \= 0

其中C(m, 0)以及C(m, m)都等于1，也就是说2 - C(m, 1) + C(m, 2) - ... - C(m, m - 1) \= 0

因此C(m, 1) - C(m, 2) + C(m, 3) - ... + C(m, m - 1) \= 2

也就是说当m为偶数时，需要少计算1次。

根据上面的结论，就可以先枚举所有的硬币种类的组合，计算这种组合的面值的最小公倍数L并记录在数组f中。若此时硬币种类数为奇数种，那么对于所有L的倍数则都应该多计算1次；反之若此时硬币种类数为偶数中，那么对于所有L的倍数则都应该少计算1次。

得到f数组后，对于面值v，就可以枚举f中所有的最小公倍数L以及其对应的加1或减1，计算v // L的结果，然后根据对应加1或者减1来更新对应的可组合面值数。

到了这里，对于面值v，在1到v之间有多少种面值可以被单种硬币组合出来就已经解决了。

---

此时只需要先计算f数组，然后根据f数组以及tot_l计算出对应的tot，然后通过k // tot \* tot_l初始化答案，并将k对tot取模。最后在1到tot_l - 1之间进行二分，对于当前二分到的mid，通过f计算1到mid之间可以组合出的面值数cnt。若cnt小于k，则更新二分的下界，否则更新二分的上界。二分完成后，将二分边界累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def findKthSmallest(self, coins, k):
        """
        :type coins: List[int]
        :type k: int
        :rtype: int
        """

        def gcd(x, y):
            while y:
                x, y = y, x % y
            return x
        
        def get_l(arr):
            l = arr[0]
            for v in arr[1:]:
                l = l * v // gcd(l, v)

            return l

        tot_l = get_l(coins)

        f = []
        for state in range(1, (1 << len(coins))):
            tmp = []
            for index, v in enumerate(coins):
                if state & (1 << index) == (1 << index):
                    tmp.append(v)
            
            if len(tmp) % 2 == 0:
                f.append([get_l(tmp), -1])
            else:
                f.append([get_l(tmp), 1])

        tot = 0
        for l, delta in f:
            tot += tot_l // l * delta

        res = k // tot * tot_l
        k %= tot

        if k > 0:
            left = 1
            right = tot_l - 1
            while left < right:
                mid = (left + right) // 2
                cnt = 0
                for l, delta in f:
                    cnt += mid // l * delta
                
                if cnt < k:
                    left = mid + 1
                else:
                    right = mid
        
            res += left
        
        return res
```
