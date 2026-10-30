---
title: "1611. 使整数变为0的最少操作次数"
aliases: ["yiduobo的每日leetcode 1611.使整数变为0的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "题单/位运算", "题单/贪心算法", "题单/位运算/九-其他", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/435014474"
zhihu_id: "435014474"
zhihu_title: "yiduobo的每日leetcode 1611.使整数变为0的最少操作次数"
question_id: "1611"
question: "使整数变为 0 的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-one-bit-operations-to-make-integers-zero/"
difficulty: "Hard"
rating: 2345
created: "2021-11-19T00:02:22+08:00"
updated: "2021-11-19T00:02:22+08:00"
upvotes: 0
comments: 0
---

# 1611. 使整数变为0的最少操作次数

> **[yiduobo的每日leetcode 1611.使整数变为0的最少操作次数](https://zhuanlan.zhihu.com/p/435014474) · 知乎 · 2021-11-19 · 赞同 0**
> 力扣：[1611. 使整数变为 0 的最少操作次数](https://leetcode.cn/problems/minimum-one-bit-operations-to-make-integers-zero/) · Hard · 灵茶山艾府：[逆向思维+公式推导（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1611.使整数变为0的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-one-bit-operations-to-make-integers-zero/)

首先，观察题目给出的两种操作，可以发现高位上的1如果想要消去，那么必须将后续的低位变为2的幂次的形式，那么这里应该是有递归的做法的。

对于一个形如1XX...XX的数而言，首先要将其变为11000...00的形式，然后将最高位的1消去，再处理后面这个100...00。对于这个问题倒是很好求解，因为对于这个剩下的100...00，同样也需要将其变为1100...00的形式，是一个很典型的递归问题。而对于10XX...XX以及11XX..XX这两种情况，要变成1100...00则是不同操作，不过我在这里没有想得太清楚。

不得以只好尝试另外的方法。不妨从0开始倒推，先看看4位二进制表示下要倒推回各个数需要的步数：

0、初始化为0000

1、执行操作1，从0000变为0001

2、执行操作2，从0001变为0011

3、执行操作1，从0011变为0010

4、执行操作2，从0010变为0110

5、执行操作1，从0110变为0111

6、执行操作2，从0111变为0101

7、执行操作1，从0101变为0100

8、执行操作2，从0100变为1100

9、执行操作1，从1100变为1101

10、执行操作2，从1101变为1111

11、执行操作1，从1111变为1110

12、执行操作2，从1110变为1010

13、执行操作1，从1010变为1011

14、执行操作2，从1011变为1001

15、执行操作1，从1001变为1000

仔细观察一下，就会发现其中很有意思的规律。

如果头尾开始两两进行配对，可以发现

0000与1000分别需要0和15步

0001与1001分别需要1和14步

0011与1011分别需要2和13步

更一般的写法，为

x与x- 2^k需要的步数分别为2^(k + 1) - 1 - y以及y

根据上面这个结论，就可以每次都找出最大的满足2^k小于等于x的k，然后改为求解将x - 2^k变为0的步数y，那么2^(k + 1) - 1 - y就是将x变为0所需的步数了。重复这个过程，直到x变为0为止，那么最终的答案就是

2^(k1 + 1) - 1 - (2^(k2 + 1) - 1 - (2^(k3 + 1) - 1 - ...)))

如果将括号打开，那么最终答案就是奇数项的2^k - 1之和，减去偶数项的2^k - 1之和。

于是现在的做法就是将x从最高位开始逐位分离，设当前轮分离的位置为第k位，那么奇数轮的分离则将答案加上2^(k + 1) - 1，偶数轮的分离则减去2^(k + 1) - 1。重复该过程直到x变为0为止。

最后附上python代码：

```python
class Solution(object):
    def minimumOneBitOperations(self, n):
        """
        :type n: int
        :rtype: int
        """

        pow2 = [1]
        while pow2[-1] < n:
            pow2.append(pow2[-1] + pow2[-1])
        
        p = len(pow2) - 1
        res = 0
        flag = 1
        while n > 0:
            while p > 0 and pow2[p] > n:
                p -= 1
            
            res += flag * (pow2[p] + pow2[p] - 1)
            flag = -flag
            n -= pow2[p]

        return res
```
