---
title: "1681. 最小不兼容性"
aliases: ["yiduobo的每日leetcode 1681.最小不兼容性"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/445423554"
zhihu_id: "445423554"
zhihu_title: "yiduobo的每日leetcode 1681.最小不兼容性"
question_id: "1681"
question: "最小不兼容性"
problem_url: "https://leetcode.cn/problems/minimum-incompatibility/"
created: "2021-12-15T00:03:27+08:00"
updated: "2021-12-15T00:03:28+08:00"
upvotes: 0
comments: 0
---

# 1681. 最小不兼容性

> **[yiduobo的每日leetcode 1681.最小不兼容性](https://zhuanlan.zhihu.com/p/445423554) · 知乎 · 2021-12-15 · 赞同 0**
> 力扣：[1681. 最小不兼容性](https://leetcode.cn/problems/minimum-incompatibility/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1681.最小不兼容性

[力扣](https://leetcode-cn.com/problems/minimum-incompatibility/)

这一题与经典的圆桌会议问题很像，不同之处在于圆桌会议问题只要求给出合法的分组方案，但是这里还额外要求代价最小。如果只需要给出合法的方案，那么使用网络流建模是很容易的，但是这里要求代价最小，所以只能老老实实使用状态压缩动态规划来做了。

首先考察边界情况。当k等于n时，说明每一组中只有一个数，那么最终答案就必然为0。

接下来考虑k \< n的情况，此时每一组的大小group_size就是n / k。

由于组中的数先后顺序其实是不敏感的，因此可以强制设定每一组中的数是从小到大添加进来的，于是可以先将数组从小到大进行排序。

注意到题目非常贴心地设定了每个数的大小不超过16，那么在这里就可以给出一种状态表示f[state][last]表示当前使用了state表示的这些数，最后使用的数为last时的最小代价。对于f[state][last]而言，可以通过解析state得知当前使用了哪些数，以及每个数使用的个数。记一共使用了cnt个数，那么此时最后一组中的数的个数就是cnt % group_size。若这个数为0，那么说明当前是为新的一组选择数字，那么此时可以选择剩下的任意数。若这个数不为0，说明当前组上一次选择的数为last，此时只能从剩下的大于last的数中进行选择。

不妨设选择了第index个数，那么此时的state就变成了state | (1 \<\< index)，而last自然就是nums[index]。若此时的cnt % group_size恰好等于group_size - 1，就说明将nums[index]加入后当前组就已经满了，需要计算代价cost，然后使用f[state][last] + cost来更新f[state | (1 \<\< index)][nums[index]。

关于计算代价这里，一种可行的做法是枚举state的子集，我在这里采用的是比较trick的做法。对于需要计算代价时的state，一定是可以恰好分成若干组的。由于之前的f[state][last]是最小的代价，因此此时state中的最小值必然只会出现在最后操作的这一组当中，如果出现在其他组当中的话只会让f[state][last]的值更大。换言之，此时计算代价的最大值和最小值就分别是nums[index]以及state中包含的下标对应的最小值。

最后附上python代码：

```python
class Solution(object):
    def minimumIncompatibility(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        nums.sort()
        next = {}
        cnt = {}
        pos = {}
        now = 0
        n = len(nums)
        if k == n:
            return 0
        
        group_size = n / k
        for index in range(n):
            if nums[index] != now:
                next[now] = nums[index]
                now = nums[index]
                pos[nums[index]] = index
            
            cnt[nums[index]] = cnt.get(nums[index], 0) + 1
            
        max_state = 1 << n
        f = [[None] * (nums[-1] + 1) for _ in range(max_state)]
        f[0][0] = 0

        res = -1
        for state in range(max_state):
            for last in range(nums[-1] + 1):
                if f[state][last] is not None:
                    if state == max_state - 1:
                        if res == -1 or res > f[state][last]:
                            res = f[state][last]
                    else:
                        used = {}
                        used_cnt = 0
                        used_min = None
                        for index in range(n):
                            if state & (1 << index):
                                num = nums[index]
                                used[num] = used.get(num, 0) + 1
                                used_cnt += 1
                                if used_min is None:
                                    used_min = num
                    
                        if used_cnt % group_size == 0:
                            now = 0
                        else:
                            now = last
                    
                        while now in next:
                            check_num = next[now]
                            used_check_num = used.get(check_num, 0)
                            if used_check_num < cnt[check_num]:
                                next_state = state | (1 << (pos[check_num] + used_check_num))
                                next_cost = f[state][last]
                                if used_cnt % group_size == group_size - 1:
                                    next_cost += check_num - used_min
                                if f[next_state][check_num] is None or f[next_state][check_num] > next_cost:
                                    f[next_state][check_num] = next_cost
                        
                            now = check_num
                    
        return res
```
