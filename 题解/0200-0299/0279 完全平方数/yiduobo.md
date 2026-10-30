---
title: "279. 完全平方数"
aliases: ["yiduobo的每日leetcode 279.完全平方数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/breadth-first-search", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/图论算法", "题单/数学算法", "题单/LeetCode-热题-100", "题单/动态规划/三-背包", "题单/图论算法/一-图的遍历", "题单/数学算法/一-数论", "题单/LeetCode-热题-100/动态规划"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/153492831"
zhihu_id: "153492831"
zhihu_title: "yiduobo的每日leetcode 279.完全平方数"
question_id: "279"
question: "完全平方数"
problem_url: "https://leetcode.cn/problems/perfect-squares/"
difficulty: "Medium"
created: "2020-07-02T21:50:35+08:00"
updated: "2020-07-02T21:50:35+08:00"
upvotes: 1
comments: 0
---

# 279. 完全平方数

> **[yiduobo的每日leetcode 279.完全平方数](https://zhuanlan.zhihu.com/p/153492831) · 知乎 · 2020-07-02 · 赞同 1**
> 力扣：[279. 完全平方数](https://leetcode.cn/problems/perfect-squares/) · Medium · 灵茶山艾府：[两种方法：完全背包 / BFS 最短路（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

279.完全平方数<https://leetcode-cn.com/problems/perfect-squares/>

第一眼看上去是动态规划的题目，f[i]表示数字i最少由几个完全平方数组成，那么：

1、若i本身是完全平方数，那么f[i] \= 1

2、若i不是完全平方数，那么j从1到sqrt(i)循环，表示从数字i - j \* j加上完全平方数j \* j从而得到数字i，于是有f[i] \= min(f[i - j \* j]) + 1

一趟扫描，对于非完全平方数每次需要查找sqrt(i)次，因此最终的时间复杂度为O(n \* sqrt(n))

不过仔细观察前200的f数组，可以发现f最大不超过4，其中等于4的有

7，15，23，28，31，39，47，55，60，63，71，79，87，92，95，103，111，112，119，124，127，135，143，151，156，159，167，175，183，188，191，199

观察前几项，自然地会想到将里面模8余7的数选出来 ，那么就是

7，15，23，31，39，47，55，63，71，79，87，95，103，111，119，127，135，143，151，159，167，175，183，191，199

剩下的数为28，60，92，112，124，156，188，分解掉4之后就是

28 \= 4 \* 7，60 \= 4 \* 15，92 \= 4 \* 23，124 \= 4 \* 31， 156 \= 4 \* 39，188 \= 4 \* 47

最后还剩下112，有

112 \= 16 \* 7

于是猜测，16\* 15， 16 \* 23， 16 \* 31等数都是4，可以在小范围内得到验证。

更一般的，若某个数x除以4^k之后，模8余7，那么其对应的f[x]就是4，在小范围内也得到了了验证。

虽然不知道如何证明，但是在小范围内是正确的，另外当n过大时，动态规划的时间复杂度应该是处理不了的，于是想当然的就运用了上面的规律。这次运气不错，这个规律是正确的。

现在的做法为：

1、先判断n是否为完全平方数，如果是，那么f[n] \= 1。

2、接下来利用上面的规律判断n是否满足f[n] \= 4。

3、若上面两步都不满足，那么f[n]一定是2或者3。对于2和3的情况暂时没想到好的处理方法，还是需要j从1到根号n枚举，判断n - j \* j是否为完全平方数。如果是，那么f[n] \= 2，否则f[n] \= 3。

于是最终的时间复杂度为O(sqrt(n))

最后附上python代码，注释掉的部分为动态规划的代码：

```python
class Solution(object):
    def numSquares(self, n):
        """
        :type n: int
        :rtype: int
        """

        '''
        f = []
        f.append(1)

        for i in range(1, n + 1):
            t = int(sqrt(i))
            if t * t == i:
                f.append(1)
            else:
                f.append(f[-1] + 1)
                for j in range(2, t + 1):
                    f[-1] = min(f[-1], f[i - j * j] + 1)

        return f[n]
        '''

        t = int(sqrt(n))
        if t * t == n:
            return 1

        pow4 = 1
        while n % (pow4 * 4) == 0:
            pow4 *= 4

        if n / pow4 % 8 == 7:
            return 4

        for j in range(1, t + 1):
            tmp = int(sqrt(n - j * j))
            if tmp * tmp + j * j == n:
                return 2

        return 3
```
