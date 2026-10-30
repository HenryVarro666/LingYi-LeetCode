---
title: "1005. K次取反后最大化的数组和"
aliases: ["yiduobo的每日leetcode 1005.K次取反后最大化的数组和"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/greedy", "leetcode/quickselect", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/366482145"
zhihu_id: "366482145"
zhihu_title: "yiduobo的每日leetcode 1005.K次取反后最大化的数组和"
question_id: "1005"
question: "K 次取反后最大化的数组和"
problem_url: "https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations/"
difficulty: "Easy"
rating: 1275
created: "2021-04-20T23:36:39+08:00"
updated: "2021-04-20T23:36:39+08:00"
upvotes: 0
comments: 0
---

# 1005. K次取反后最大化的数组和

> **[yiduobo的每日leetcode 1005.K次取反后最大化的数组和](https://zhuanlan.zhihu.com/p/366482145) · 知乎 · 2021-04-20 · 赞同 0**
> 力扣：[1005. K 次取反后最大化的数组和](https://leetcode.cn/problems/maximize-sum-of-array-after-k-negations/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1005.K次取反后最大化的数组和

[力扣](https://leetcode-cn.com/problems/maximize-sum-of-array-after-k-negations/)

为了使得数组和最大，一个直观的想法就是对于负数都取反，对于正数则保持不动。注意到对于一个数而言，取反两次相当于没有变化，因此我们在这里可以利用这个性质使用掉多出来的取反次数，那么：

1、若负数的数量大于K，那么我们应当取反最小的K个数

2、若负数的数量大于等于K，那么我们首先应当将负数全部取反，对于剩下的取反次数K’：

2-1）若K’为偶数，那么我们可以利用重复取反使用完这些次数，因此无需进行额外操作

2-2）若K’为奇数，那么最后还必须取反一次。此时所有的数都是大于等于0的，因此应当取反绝对值最小的那个数

根据上面的结论，直观的做法是先进行排序，然后逐条执行，不过注意到这里数组中的都在-100到100之间，那么我们也可以使用dict统计每个数出现的次数，在统计的过程中还可以顺便求出原始数组之后，并找到最小的绝对值min_abs。

接下来从-100开始到-1进行遍历，设当前处理的数为num，出现了cnt次，那么：

1、若cnt \<\= K，那么应该将这cnt个数全部取反，此时应该将K减去cnt，同时数组之和中减少了cnt个num，并加上了cnt个-num，一来一去就是加上了cnt\*2个-num

2、若cnt > K，那么我们只能尽量进行取反，于是此时只有K个num被取反，那么答案就应该加上K \* 2个-num。此时取反的次数已经用完，直接返回答案即可

遍历完成后，若K为奇数，说明还需要取反一次绝对值最小的数，那么将答案减去两倍min_abs即可。

最后附上python代码：

```python
class Solution(object):
    def largestSumAfterKNegations(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        min_abs = 101
        cnt_dict = {}
        res = 0
        for num in A:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
            res += num
            min_abs = min(min_abs, abs(num))

        for num in range(-100, 0):
            if num in cnt_dict:
                cnt = cnt_dict[num]
                if cnt <= K:
                    K -= cnt
                    res -= 2 * cnt * num
                else:
                    res -= 2 * K * num
                    K = 0
                    break
        
        if K > 0 and K % 2 == 1:
            res -= 2 * min_abs

        return res
```
