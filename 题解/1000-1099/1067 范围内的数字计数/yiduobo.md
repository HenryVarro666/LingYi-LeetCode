---
title: "1067. 范围内的数字计数"
aliases: ["yiduobo的每日leetocde 1067.范围内的数字计数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/动态规划", "题单/动态规划/十-数位-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/608658260"
zhihu_id: "608658260"
zhihu_title: "yiduobo的每日leetocde 1067.范围内的数字计数"
question_id: "1067"
question: "范围内的数字计数"
problem_url: "https://leetcode.cn/problems/digit-count-in-range/"
difficulty: "Hard"
created: "2023-02-23T00:26:54+08:00"
updated: "2023-02-23T00:26:54+08:00"
upvotes: 0
comments: 0
---

# 1067. 范围内的数字计数

> **[yiduobo的每日leetocde 1067.范围内的数字计数](https://zhuanlan.zhihu.com/p/608658260) · 知乎 · 2023-02-23 · 赞同 0**
> 力扣：[1067. 范围内的数字计数](https://leetcode.cn/problems/digit-count-in-range/) · Hard · 灵茶山艾府：[做法同 233 题，贡献法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1067.范围内的数字计数

[力扣](https://leetcode.cn/problems/digit-count-in-range/)

对于这类数位有关的问题，经典的处理方法是使用数位动态规划，而对于某些有较好性质的问题，则可以使用组合数学来进行求解。我在这里采用的是组合数学的方法。

首先还是先将问题进行转化。求解low到high之间d出现的次数，可以转化为求解1到high之间d出现的次数，减去1到low - 1之间d出现的次数，那么问题就转化成了给出一个数now，如何高效求解1到now之间d出现的次数。

接下来，对于一个n位数而言，如果忽略掉前导0的影响，那么其中有k的数位为d的情况就有C(n, k) \* 9^(n - k)，其中C(n, k)表示在这n个数位中选择k个数位填充d的方案数量，而9^(n - k)则表示其他不是d的n - k位填充的方案数量。对于这些情况，每种情况都可以提供k个d，因此一共就是C(n, k) \* 9^(n - k) \* k个d。

需要特别注意的是，在这里是允许前导0出现的，但是在实际计算中，前导0是不合法的，因此需要使用其他的方式计算，具体的计算方式在后面会说明。

回到这个n位数。这里数位为d的数量k的取值范围是1到n，因此所有n位数中d出现的次数就是

s[n] \= C(n, 1) \* 9^(n - 1) \* 1 + C(n, 2) \* 9^(n - 2) \* 2 + ... + C(n, n) \* 9^(n - n) \* n

在这里将C(n, k) \* k单独拿出来计算，就有

C(n, k) \* k \= k \* n! / ((n - k)! \* k!) \= n! / ((n - k)! \* (k - 1)!) \= n \* (n - 1)! / (((n - 1) - (k - 1))! \* (k - 1)!)

即C(n, k) \* k \= n \* C(n - 1, k - 1)

带入回s[n]当中，就有

s[n] \= n \* (C(n - 1, 0) \* 9^(n - 1) + C(n - 1, 1) \* 9^(n - 2) + ... + C(n - 1, n - 1) \* 9^(n - n))

括号中的式子是二项式(9 + 1)^(n - 1)的展开，因此最终就有

s[n] \= n \* 10^(n - 1)

根据上面这个式子先将所有的s提前计算出来，然后对于当前处理的数now，不妨设其长度为length，接下来从高位开始逐位分离每一位数。对于当前处理的第index位上的数digit：

1、首先从0到digit - 1进行枚举v，若index大于0，或者v大于0，或者d大于0，那么就将s[length - 1 - index]累加到答案当中。

这样做的理由是此处枚举v就表示计算的是形如XX...Xv......的整数中，v右侧省略号的部分中有多少个d。

v右侧省略号的部分一共是length - 1 - index个数位，因此在包含前导0的情况下就一共有s[length - 1 - index]个d，而这里的限定条件index、v、d三者至少有一样大于0则是考虑到对于d等于0时，不能将前导0计算进去，而对于d不等于0的情况，前导0并不影响最终d的计数。

2、接下来，对于XX...Xv......中v以及v左侧XX...X而言，其中也可能包含有d。

对于这种情况，就需要使用两个变量same和delta，分别记录XX...X中d出现的次数，以及当前的v是否就等于d。

对于这些d而言，在v右侧省略号中的length - 1 - index位中一共有10^(length - 1 - index)个数，那么XX...Xv这个部分一共就会带来(same + delta) \* 10^(length - 1 - index)个d，将这个值也累加到答案中。同样的，在这里也需要满足index、v、d这三者中至少有一样大于0。

3、遍历完v之后，就来到了边界digit。接下来将index这一位固定为digit，然后继续向后考虑。若存在digit等于d，那么还需要将same更新为same加1。

全部遍历完成后，还需要将same加入到答案中，因为now自身在上面这个计算过程中是没有被考虑进去的，而now中d出现的数目就是same，因此还需要将same加入到答案中。

上面的部分讨论了d大于0的情况，而对于d等于0的情况而言，由于不能有前导0存在因此不能直接套用上面的计算方式。一种可行的转化思路是先强行安插一个最高位，这样一来就不存在前导0的问题了。具体来说，就是从0到length - 2枚举所有的index，将0到index - 1这些为设置为0，将index这一位设置成1到9，那么就可以形成一个合法的不存在前导0的n - index位数。对于这个数而言，其最右侧的n - index - 1位中0出现的次数就是s[n - index - 1]，因此在所有的n - index位数当中，一共就有9 \* s[n - index - 1]个0，此时只需随着index的遍历讲这些结果累加起来即可。

需要注意的是，对于0的情况，now自身依然是没有被计算进去的，因此计算0时依然需要将same加入到答案中。

最后附上python代码：

```python
class Solution(object):
    def digitsCount(self, d, low, high):
        """
        :type d: int
        :type low: int
        :type high: int
        :rtype: int
        """

        cnt = [0]
        pow10 = [1]
        for index in range(1, len(str(high))):
            cnt.append(index * 10 ** (index - 1))
            pow10.append(pow10[-1] * 10)

        def calc(now):
            if now == 0:
                return 0
            
            num_list = [int(x) for x in str(now)]

            length = len(num_list)
            res = 0
            same = 0
            for index, digit in enumerate(num_list):
                digit = int(digit)
                for v in range(digit):
                    if v == d:
                        delta = 1
                    else:
                        delta = 0

                    if index != 0 or v > 0 or d > 0:
                        res += pow10[length - 1 - index] * (same + delta) + cnt[length - 1 - index]

                if digit == d:
                    same += 1

            if d == 0:
                for index in range(length - 1):
                    res += 9 * cnt[index]

            return res + same

        return calc(high) - calc(low - 1)
```
