---
title: "1505. 最多K次交换相邻数位后得到的最小整数"
aliases: ["yiduobo的每日leetcode 1505.最多K次交换相邻数位后得到的最小整数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/419683040"
zhihu_id: "419683040"
zhihu_title: "yiduobo的每日leetcode 1505.最多K次交换相邻数位后得到的最小整数"
question_id: "1505"
question: "最多K次交换相邻数位后得到的最小整数"
problem_url: "https://leetcode.cn/problems/minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits/"
created: "2021-10-09T23:58:55+08:00"
updated: "2021-10-09T23:58:55+08:00"
upvotes: 0
comments: 0
---

# 1505. 最多K次交换相邻数位后得到的最小整数

> **[yiduobo的每日leetcode 1505.最多K次交换相邻数位后得到的最小整数](https://zhuanlan.zhihu.com/p/419683040) · 知乎 · 2021-10-09 · 赞同 0**
> 力扣：[1505. 最多K次交换相邻数位后得到的最小整数](https://leetcode.cn/problems/minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1505.最多K次交换相邻数位后得到的最小整数

[力扣](https://leetcode-cn.com/problems/minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits/)

为了使得最后得到的整数最小，自然是需要将小的数交换到高位上去。但是这个交换工程也必须考虑到代价，例如对于210来说，如果可以交换两次，那么应该将0交换到最前面，而如果只能交换一次，那么就应该将1交换到最前面。

于是就可以得到一条交换规则：从高位开始向后逐位处理，每次将可以交换到这个位置上的最小的数交换过来。另外，这里还有一种特殊情况是存在两个相同的最小数都可以交换，此时应该将最靠前，也就是交换代价最小的那个交换到最高位上。这样一来，才能为后续的交换尽可能多地腾出步数来。

确定了交换规则之后，就变成了经典的重排队问题。这个问题之前做过一个完全相同的题目，具体思路就是将交换视为一种插入到最前面的行为，例如样例1中的4321，一般来看是4在第1位，3在第2位，2在第3位，1在第4位，然后相邻位之间发生交换。但是这里由于每次都是将选定位置上的数字移动到当前剩余数字的最前面，那么可以将初始状态视为

\_ \_ \_ \_ 4 3 2 1

其中前面四个下划线表示空余的位置1到位置4，而原始的4321则是占据了第5到第8位。接下来第i轮，就将选定的数字移动到第i位上，此时移动的代价就是选定数字与第i位之间数字的个数。不妨模拟一下对于4321，k \= 4的情况：

首先初始状态为

\_ \_ \_ \_ 4 3 2 1

此时先考察第1位。剩余数字中最小的为1，将其移动到第1位之间隔了3个数字，因此移动的代价为3，小于此时的k \= 4，可以执行移动。移动后得到

1 \_ \_ \_ 4 3 2 \_

此时的k变成了4 - 3 \= 1，接下来考察第2位。剩余数字中最小的为2，将其移动到第2位之间隔了2个数字，移动的代价为2，大于此时的k \= 1，不能执行移动。退而求其次，尝试移动3。将3移动到第2位之间只隔了一个数字4，因此移动的代价为1，可以执行移动。移动后得到

1 4 \_ \_ \_ 3 2 \_

此时的k变成了1 - 1 \= 0，接下来考察第3位。剩余数字中最小的为2，移动代价为1，不能执行移动。另一个数字3移动的代价为0，可以移动。移动后得到

1 4 3 \_ \_ \_ 2 \_

最后第4位，剩余数字中2的移动代价为0，将其移动到第4位，得到最终答案为

1 4 3 2 \_ \_ \_ \_

到了这里，问题就转化成了对于一个数字所在位置p以及其目的地i而言，在i到p之间有多少个数字，这个问题可以用树状数组来进行处理，即使用树状数组维护前缀和的思路。

此时就得到了最终的做法：

1、首先一趟扫描，记录每个数字出现的原始位置加上n + 1作为排队的序列备用，同时将这些位置加入树状数组。

2、接下来从第1位开始逐位进行处理，每一轮遍历0到9，对于当前数字swap_num，通过不中1中记录的位置找到当前剩余数中swap_num第一次出现位置swap_pos，并使用树状数组求解当前处理的位置到swap_pos之间数字的数量。若小于等于k，那么移动当前swap_pos，然后开始处理下一位；若大于k，那么考虑移动下一个数字。

由于移动当前剩余数字中最靠前的数字的代价为0，因此每一轮都必然可以执行移动操作。执行完n轮之后，就得到了最终答案。

最后附上python代码：

```python
class Solution(object):
    def minInteger(self, num, k):
        """
        :type num: str
        :type k: int
        :rtype: str
        """

        n = len(num)
        pos_list = [[] for _ in range(10)]
        suffix_array = [0] * (n + n + 1)
        for index, char in enumerate(num):
            pos_list[int(char)].append(index + n + 1)
            self.add(index + n + 1, n + n, suffix_array, 1)

        n = len(num)
        num_index = [0] * 10
        now_pos = 1
        res = []
        while now_pos <= n:
            for swap_num in range(10):
                if num_index[swap_num] < len(pos_list[swap_num]):
                    swap_pos = pos_list[swap_num][num_index[swap_num]]
                    step = self.sum(swap_pos - 1, suffix_array) - now_pos + 1
                    if step <= k:
                        res.append(str(swap_num))
                        k -= step
                        self.add(now_pos, n + n, suffix_array, 1)
                        self.add(swap_pos, n + n, suffix_array, -1)
                        num_index[swap_num] += 1
                        break

            now_pos += 1

        return ''.join(res)
    
    def add(self, now, max_n, suffix_array, delta):
        while now <= max_n:
            suffix_array[now] += delta
            now += now & -now
        
    def sum(self, now, suffix_array):
        res = 0
        while now:
            res += suffix_array[now]
            now -= now & -now
        
        return res
```
