---
title: "3366. 最小数组和"
aliases: ["yiduobo的每日leetcode 3366.最小数组和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/dynamic-programming", "leetcode/sorting", "题单/动态规划", "题单/贪心算法", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/一-贪心策略", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/27987668743"
zhihu_id: "27987668743"
zhihu_title: "yiduobo的每日leetcode 3366.最小数组和"
question_id: "3366"
question: "最小数组和"
problem_url: "https://leetcode.cn/problems/minimum-array-sum/"
difficulty: "Medium"
rating: 2040
created: "2025-03-05T00:08:06+08:00"
updated: "2025-03-05T00:08:06+08:00"
upvotes: 1
comments: 0
---

# 3366. 最小数组和

> **[yiduobo的每日leetcode 3366.最小数组和](https://zhuanlan.zhihu.com/p/27987668743) · 知乎 · 2025-03-05 · 赞同 1**
> 力扣：[3366. 最小数组和](https://leetcode.cn/problems/minimum-array-sum/) · Medium · 灵茶山艾府：[两种方法：DP / 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3366.最小数组和

<https://leetcode.cn/problems/minimum-array-sum/>

题目给出一个整数数组nums以及三个整数k、op1和op2，可以对nums执行一下操作：

操作1：选择nums中的某个下标i，将nums[i]除以2向上取整。最多可以执行此操作op1次，且对于每个下标最多只能执行一次。

操作2：选择nums中的某个下标i，若nums[i]大于等于k，就将nums[i]减去k。最多可以执行此操作op2次，且对于每个下标最多只能执行一次。

两种操作可以应用于同一下标，但是每种操作只能对同一个下标执行一次。

问执行任意次操作后，nums中所有元素的最小和是多少。

题目中有一种除法操作和一种减法操作，那么直观上来看：

1、应该尽量先执行除法操作再执行减法操作，因为先执行减法操作的话除法操作的效果会打折扣。这里说的尽量是因为有可能先执行除法操作的话就无法执行减法操作了。

2、应该让除法操作应用在尽量大的数字上，这样的收益最大；相对的，减法操作只要能够执行，得到的收益则没有差别。

基于以上两点，就可以先将nums分为3个部分。其中：

1、第一部分part1包含所有大于等于k \* 2 - 1的数。这些数字可以先执行除法操作再执行减法操作。

2、第二部分part2包含所有大于等于k，且小于k \* 2 - 1的数。这些数字可以执行减法操作再执行除法操作，或者单独执行除法操作，但是不能先执行除法操作再执行减法操作。

3、第三部分part3包含剩下的小于k的数。这些数字只能执行除法操作。

---

可以发现，其中part1的数字又是最大的那一批，那么根据最开始的结论2，就可以先将part1中的数字从大到小进行排序，然后依次先执行除法操作再执行减法操作。

在处理完part1后，可能还余下一些可用的减法操作和除法操作。由于余下的减法操作只能作用在part2中，那么在这里就应该先用完这些减法操作，再执行除法操作。对于减法操作，在这里应该作用在part2中较小的数字上，因为先执行减法操作再执行除法操作是不优的，但是除法操作应该尽量执行在较大的数字上，所以减法操作就应该尽量作用在较小的数字上。

在对part2中的数执行完减法操作后，将其并入part3，从大到小进行排序后同样依次执行除法操作即可。

---

需要特别注意的是，由于本题的除法操作是除以2向上取整，那么在这里对于part2中被减数和k的奇偶性还有值得讨论的地方。具体来说，就是先执行减法再执行除法时，由于奇偶性不同以及除以2向上取整的影响，可能会使得上面的贪心算法不是最优。

例如对于part2 \= [6, 7]，k \= 5，且还可以执行恰好两次除法操作和一次减法操作时，按上面的描述应该让减法操作作用在6上，就需要对[1, 7]各执行一次除法操作，得到的结果为1 + 4 \= 5。而如果让减法操作作用在7上，接下来需要对[6, 2]各执行一次除法操作，得到的结果为3 + 1 \= 4，实际上是更优的。

出现上面情况的理由是对于一组x和y，若x为偶数，y为奇数，k为奇数，且x \< y，那么

将减法执行在x上后得到的结果就是

(x - k + 1) // 2 + (y + 1) // 2 \= x // 2 - (k - 1) // 2 + (y + 1) // 2 \= x // 2 + (y - k + 2) // 2

将减法执行在y上后得到的结果就是

x // 2 + (y - k) // 2

可以发现上面的式子结果比下面的多1

更进一步的，对于x、y、k的奇偶性，以及是否有后续的除法操作分情况进行讨论。在这里默认x \< y。

1、后续没有除法操作：

对于这种情况，减法操作执行在x或y上实际上没有区别

2、后续只有一次除法操作：

对于这种情况，由于x \< y，那么无论减法操作在那边收益都是一样的，而除法操作执行在y上必然是优于执行在x上的，因此对于这种情况符合对part2的处理方法，即让较小的x执行减法操作，让较大的y执行除法操作

3、后续有两次出发操作：

首先若k为偶数，那么无论谁执行减法操作都无法消除除以2向上取整带来的影响，因为偶数作为被减数时，差的奇偶性与被减数的奇偶性相同，因此对于这种情况依然符合对part2的处理方法。

接下来若k为奇数且x同样为奇数时，x - k后除以2不会受到向上取整的影响，因此对于这种情况依然符合对part2的处理方法。

最后就是k为奇数且x为偶数时，若y为奇数，也就是上面举例说明的情况，这种情况下就应该让y执行减法操作，与上面对part2的处理方法就不同了，需要进行修正。

---

由于part2在执行减法操作后需要与part3合并后再执行除法操作，因此在执行减法操作时还无法确定当前值是否会执行除法操作，也就不能在处理part2时就直接根据奇偶性来进行修正。

我在这里的处理方法是使用一个哈希表mk_dict记录那些数是某个偶数减去奇数k得到的，也就是说对于part2中的某个v，若v为偶数，k为奇数，且v执行了减法操作，那么就将mk_dict[v - k]加上1。除此之外，还需要使用一个变量rest_odd记录part2中没有执行过减法操作的奇数数目。

接下来在将part2合并到part3中，从大到小排序然后依次执行除法操作时，若当前元素v对应的mk_dict[v]大于0，那么说明rest_odd中的所有奇数都执行了除法操作，因为按照part2中的处理顺序，rest_odd对应的没有执行过减法操作的奇数必然是大于v + k的，因此会优先于v执行除法操作。

如果此时的rest_odd大于0，那么就应该中rest_odd选出一个元素y，将v还原为v + k，然后让y来执行减法操作。对于这种情况，由于(y + 1) // 2已经被累加到了答案中，而替换后的结果应该是

(v + k) // 2 + (y - k) // 2 \= (v + 1) // 2 + (k + 1) // 2 - 1 + (y + 1) // 2 - (k + 1) // 2

化简后就是

(v + 1) // 2 + (y + 1) // 2 - 1

那么在这里只需继续将(v + 1) // 2累加到答案中，然后将答案减去1，同时将rest_odd减去1即可。

最后附上python代码：

```python
class Solution(object):
    def minArraySum(self, nums, k, op1, op2):
        """
        :type nums: List[int]
        :type k: int
        :type op1: int
        :type op2: int
        :rtype: int
        """
        
        part1 = []
        part2 = []
        part3 = []

        for v in nums:
            if v >= k * 2 - 1:
                part1.append(v)
            elif v >= k:
                part2.append(v)
            else:
                part3.append(v)

        res = 0

        part1.sort(reverse=True)
        for v in part1:
            if op1:
                v = (v + 1) // 2
                op1 -= 1
            if op2:
                v -= k
                op2 -= 1
            res += v
        
        part2.sort()
        mk_dict = {}
        rest_odd = 0
        for index, v in enumerate(part2):
            if op2:
                if v % 2 == 0 and k % 2 == 1:
                    mk_dict[v - k] = mk_dict.get(v - k, 0) + 1
                part2[index] -= k
                op2 -= 1
            elif v % 2 == 1:
                rest_odd += 1

        part3.extend(part2)
        part3.sort(reverse=True)
        for v in part3:
            if op1:
                if mk_dict.get(v, 0) > 0 and rest_odd > 0:
                    mk_dict[v] -= 1
                    rest_odd -= 1
                    res -= 1
                v = (v + 1) // 2
                op1 -= 1
            res += v
        
        return res
```
