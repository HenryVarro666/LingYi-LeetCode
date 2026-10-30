---
title: "4053. 使每个元素变为回文数的最少操作次数"
aliases: ["yiduobo的每日leetcode 4053.使每个元素变为回文数的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2083672564551902690"
zhihu_id: "2083672564551902690"
zhihu_title: "yiduobo的每日leetcode 4053.使每个元素变为回文数的最少操作次数"
question_id: "4053"
question: "使每个元素变为回文数的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-every-element-palindromic/"
difficulty: "Medium"
created: "2026-09-17T00:27:35+08:00"
updated: "2026-09-17T00:27:35+08:00"
upvotes: 0
comments: 0
---

# 4053. 使每个元素变为回文数的最少操作次数

> **[yiduobo的每日leetcode 4053.使每个元素变为回文数的最少操作次数](https://zhuanlan.zhihu.com/p/2083672564551902690) · 知乎 · 2026-09-17 · 赞同 0**
> 力扣：[4053. 使每个元素变为回文数的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-every-element-palindromic/) · Medium · 灵茶山艾府：[两种方法：预处理回文数 / 至多考虑 5 个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4053.使每个元素变为回文数的最少操作次数

<https://leetcode.cn/problems/minimum-operations-to-make-every-element-palindromic/description/>

题目给出一个整数数组nums。

在一次操作中，可以选择一个下标index，并将其增加2或者减少2。

要求计算将nums中所有元素都变为回文数所需的最少操作次数。不同元素可以变成不同的回文数。

题目实际上就是要对数组中的每个元素v都找出同奇偶的前一个回文数mi以及后一个回文数ma。对于这个问题，可以利用贪心来处理。

首先，为了方便起见，可以将其转化为字符串s，然后针对s展开操作。

为了使得操作的次数最少，那么就应该尽量不去修改高位，也就是让s的后半部分去适配前半部分。在这里可以将高位的这一半先分离出来，不妨记为half。

由于题目要求生成的回文数与原数的奇偶性相同，而只有当half的最高位的奇偶性与v的奇偶性相同时，才有可能在不修改half的前提下生成与v同奇偶的回文数，那么：

1、若满足half的最高位与v的奇偶性相同，则可以先尝试反转half作为后半部分构成回文数，将其记为x。

1-1）若x与v的奇偶性相同，那么说明v本身就是回文数，不需要进行任何修改，此时可以直接跳过v了

1-2）若x > v，那么x就是与v同奇偶的下一个回文数ma，接下来还需要找出前一个同奇偶的回文数mi。

对于mi的计算，最直观的想法自然是让half减去1，这样一来，通过half生成的回文数就一定是小于v的。但是这样做可能出现一个问题，就是一旦这次减1操作出现了借位，借到了最高位，甚至导致位数都产生了变化，那么就需要重新考虑最高位的奇偶性是否与v相同的。具体来说：

若产生了位数变化：这种情况只可能出现在原始的half是1000...000，减1之后变成了999...999。在这种情况下，直接通过half得到的回文数x就是1000...0001，且这个回文数大于v，说明v只能1000...000，因此还需要将减一后的half的最高位进一步减去1，也就是必须修改为8999...999的形式。这样一来，得到的mi就必然是8999...9998了。需要注意，中间的9可以是0个。

若没有产生位数变化：这种情况下，需要判断half的最高位的奇偶性是否与v相同。若相同，那么直接通过half生成mi就行了，否则的话同样需要将half的最高位减1，同时将后续的数位都修改为9，再通过half生成mi。

但是需要特别注意的是，若half的最高位就是1，是不能直接减1的。又由于这个1在最高位与v不同奇偶，因此v为偶数，也就是说half必须向下调整到最高位为偶数，因此在这里就又要将half调整为形如8999...999的形式，也就是小于half且最高位为偶数的最大值。

在这里还有一种最特殊的情况，就是half为1，也就是v是个两位数，那么此时对应的mi就是8，而不是由89999...999对称构造出来的回文数8999...9998，即不仅中间的9不要，最后的8也不要了。

1-3）若x \< v，那么x就是与v同奇偶的前一个回文数mi，接下来则需要想办法找出ma。

计算ma的方法与计算mi的方法类似，也是先尝试让half加上1，当然，此时也可能出现因为进位导致的最高位变化甚至位数变化，但是分析后可以发现，实际上在这里不可能产生位数变化，理由是产生位数变化就意味着half一定是999...999，那么得到的x也必然是999...999，不可能小于v，因此这种情况是没必要考虑的。

也就是说，在这里只需要考虑half加1后，最高位的奇偶性是否与v相同。若相同，那么直接通过half生成ma就行了，否则就需要将half的最高位再加上1，然后将后续的数位都修改为0，再通过half生成ma。

与上面的情况相同，这次加1操作也需要处理边界情况，也就是half的最高位为9时，不能直接加1。又由于9与v不同奇偶，因此v一定为偶数，也就是说half必须上调为2000...000，也就是大于half且最高位为偶数的最小值，此时对应的ma就是2000...0002。

2、若不满足half的最高位与v的奇偶性相同，那么ma和mi的计算就直接进入了上1-2与1-3的最后那种情况，即必须调整half的最高位来生成ma与mi。同样的，在这里也需要考虑对half最高位加1和减1可能出现的进位借位以及各种边界情况。

得到了v对应mi与ma之后，将min(ma - v, v - mi) // 2累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0

        for v in nums:
            s = str(v)
            length = len(s)
            half_len = (length + 1) // 2
            half = s[:(length + 1) // 2]
            if int(s[0]) % 2 == v % 2:
                if half_len * 2 == length:
                    x = half + half[::-1]
                else:
                    x = half + half[::-1][1:]
                
                x = int(x)
                if x == v:
                    continue
                
                if x > v:
                    ma = x
                    half = str(int(half) - 1)
                    if len(half) != half_len:
                        mi = int('8' + '9' * (length - 3) + '8')
                    elif int(half[0]) % 2 != v % 2:
                        if half[0] == '1':
                            if length == 2:
                                mi = 8
                            else:
                                mi = int('8' + '9' * (length - 3) + '8')
                        else:
                            h = str(int(half[0]) - 1)
                            mi = int(h + '9' * (length - 2) + h)
                    else:
                        if half_len * 2 == length:
                            x = half + half[::-1]
                        else:
                            x = half + half[::-1][1:]
                        mi = int(x)
                
                else:
                    mi = x
                    half = str(int(half) + 1)
                    if int(half[0]) % 2 != v % 2:
                        if half[0] == '9':
                            ma = int('2' + '0' * (length - 1) + '2')
                        else:
                            h = str(int(half[0]) + 1)
                            ma = int(h + '0' * (length - 2) + h)
                    else:
                        if half_len * 2 == length:
                            x = half + half[::-1]
                        else:
                            x = half + half[::-1][1:]
                        ma = int(x)

            else:
                if half[0] == '1':
                    if length == 2:
                        mi = 8
                    else:
                        mi = int('8' + '9' * (length - 3) + '8')
                else:
                    h = str(int(half[0]) - 1)
                    mi = int(h + '9' * (length - 2) + h)
                
                if half[0] == '9':
                    ma = int('2' + '0' * (length - 1) + '2')
                else:
                    h = str(int(half[0]) + 1)
                    ma = int(h + '0' * (length - 2) + h)

            res += min(ma - v, v - mi) // 2
        
        return res
```
