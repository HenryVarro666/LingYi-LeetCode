---
title: "1004. 最大连续1的个数II"
aliases: ["yiduobo的每日leetcode 1004.最大连续1的个数II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/二-不定长滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/366474992"
zhihu_id: "366474992"
zhihu_title: "yiduobo的每日leetcode 1004.最大连续1的个数II"
question_id: "1004"
question: "最大连续1的个数 III"
problem_url: "https://leetcode.cn/problems/max-consecutive-ones-iii/"
difficulty: "Medium"
rating: 1656
created: "2021-04-20T23:25:35+08:00"
updated: "2021-04-20T23:25:35+08:00"
upvotes: 0
comments: 0
---

# 1004. 最大连续1的个数II

> **[yiduobo的每日leetcode 1004.最大连续1的个数II](https://zhuanlan.zhihu.com/p/366474992) · 知乎 · 2021-04-20 · 赞同 0**
> 力扣：[1004. 最大连续1的个数 III](https://leetcode.cn/problems/max-consecutive-ones-iii/) · Medium · 灵茶山艾府：[滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1004.最大连续1的个数II

[力扣](https://leetcode-cn.com/problems/max-consecutive-ones-iii/)

首先考虑特殊情况，若数组中初始全都是0，那么答案就是K。

接下来，若数组中存在1，那么整个数组必然是

00...0 11...1 00...0 ... 00...0 11...1 00...0的形式，其中头部和尾部这两段连续的0也可以为空。

那么一个直观的想法就是优先填满各段1之间的0，然后再去填充头部和尾部这两段0。于是我们可以先分别求得各段0和1的数量：

1、若此时所有0的数量小于等于K，那么答案显然是n

2、若此时除去头部和尾部之外0的总数小于等于K，那么就意味着我们可以将所有1连成一串，并且剩下的额度还可以额外填充头部和尾部的0，因此答案为1的总数加K

3、其他情况下，就需要用到熟悉的滑动窗口法。具体来说就是利用上面统计出的各段0和1的数量，计算以每一段1作为窗口的右边界时最长连续1的数量是多少。此时头部和尾部的0显然没有填充的必要，因此我们可以先舍去这两个部分，那么样例2

00 11 00 111 0 1111 000 11111

统计出来的结果就是

[0\*2，1\*2，0\*2，1\*3，0\*1，1\*2，0\*3，1\*4，0\*0]

舍去头尾的0得到

[1\*2，0\*2，1\*3，0\*1，1\*2，0\*3，1\*4]

我们使用两个指针l和r，分别指向当前区间涵盖的最左侧1以及最右侧1，初始情况下l和r都指向0，也就是对应数组中的1\*2这个位置。

接下来，每一轮都尝试将r向右移动到下一段1的位置，期间将会经过0的部分。此时就需要判断当前剩下的K与这一段0数量的大小。若可以顺利移动，那么就将K减去这些0的个数，否则就需要将l向右移动，同时l后面的一段1不再需要填充，因此应当回收掉。每次移动后都更新答案，直到r到末尾为止。

还是以样例2举例：

1、初始状态下，l和r都是0，此时剩下的K为3，已经取得的1的个数为1\*2中的2。

使用2 + 3 \= 5更新答案

2、接下来将r移动到1\*3这个位置，那么需要跨过0\*2，因此需要使用K中的2个额度。

此时的K为1

已经取得的1的个数新增了0\*2中被填充的2以及1\*3中的3，一共为2 + 2 + 3 \= 7

那么此时应该使用1 + 7 \= 8更新答案

3、接下来将r移动到1\*2这个位置，那么需要跨过0\*1，恰好K中还余下1个额度

此时的K就变为了0

已经取得的1的个数新增了0\*1中被填充的1以及1\*2中的2，一共为7 + 1 + 2 \= 10

那么此时应该用0 + 10 \= 10更新答案

4、最后将r移动到1 \* 4这个位置，那么需要跨过0\*3，但此时K中没有余下的额度，因此需要将l向后移动以回收中间的0：

将l从头部的1\*2移动到1\*3，并回收掉后面的0\*2，此时已经取得的1的个数由10变为了10 - 2 - 2 \= 6，K则变为2，K的额度依然不够

继续将l向后移动，此时从1\*3移动到了第二个1\*2，并回收掉后面的0\*1，此时已经取得的1的个数由6变为了6 - 3 - 1 \= 2，K则变为3，此时K的额度已经足够了

使用掉3的额度之后，此时剩余的K依然为0

已经取得的1则新增了0\*3中的3以及1\*4中的4，一共为2 + 3 + 4 \= 9

那么此时应该用0 + 9 \= 9 更新答案

遍历完成后，最终答案就是第3步中的10。

最后附上python代码：

```python
class Solution(object):
    def longestOnes(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        n = len(nums)
        l = 0
        while l < n and nums[l] == 0:
            l += 1
        
        if l == n:
            return k
        
        r = n - 1
        while r >= 0 and nums[r] == 0:
            r -= 1
        
        p = l
        while p + 1 <= r and nums[p + 1] == 1:
            p += 1
        
        one = [p - l + 1]
        zero = []
        p += 1
        while p <= r:
            last_p = p
            while p + 1 <= r and nums[p + 1] == 0:
                p += 1
            zero.append(p - last_p + 1)
            p += 1

            last_p = p
            while p + 1 <= r and nums[p + 1] == 1:
                p += 1
            one.append(p - last_p + 1)
            p += 1
        
        s0 = sum(zero)
        if s0 + l + n - 1 - r <= k:
            return n
        elif s0 <= k:
            return r - l + 1 + s0 - k
        else:
            bound = 0
            now = one[0]
            res0 = k
            res1 = now

            for index in range(1, len(one)):
                while bound < index - 1 and k < zero[index - 1]:
                    k += zero[bound]
                    now -= one[bound]
                    bound += 1
                if k >= zero[index - 1]:
                    now += one[index]
                    k -= zero[index - 1]
                else:
                    now = one[index]
                    bound = index

                res1 = max(res1, now)
            
            return res0 + res1
```
