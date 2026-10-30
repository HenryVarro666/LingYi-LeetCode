---
title: "351. 安卓系统手势解锁"
aliases: ["yiduobo的每日leetcode 351.安卓系统手势解锁"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/597207756"
zhihu_id: "597207756"
zhihu_title: "yiduobo的每日leetcode 351.安卓系统手势解锁"
question_id: "351"
question: "安卓系统手势解锁"
problem_url: "https://leetcode.cn/problems/android-unlock-patterns/"
created: "2023-01-07T01:38:15+08:00"
updated: "2023-01-07T01:38:15+08:00"
upvotes: 0
comments: 0
---

# 351. 安卓系统手势解锁

> **[yiduobo的每日leetcode 351.安卓系统手势解锁](https://zhuanlan.zhihu.com/p/597207756) · 知乎 · 2023-01-07 · 赞同 0**
> 力扣：[351. 安卓系统手势解锁](https://leetcode.cn/problems/android-unlock-patterns/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

351.安卓系统手势解锁

[力扣](https://leetcode.cn/problems/android-unlock-patterns/)

看上去像组合数学的问题，但是对于处理非法情况感觉没有什么特别好的思路。

另一种可行的做法则是动态规划，令f[state][last]表示当前访问过state这些数字，且最后一个数字为last时的合法手势数目。

对于f[state][last]，可以先计算通过state计算出当前访问过的数字，剔除last后可以重新计算出上一轮的状态pre_state，然后枚举上一轮的最后一个数字prev_last。在这里需要注意，若从prev_last到last穿过了另一个数字，且这个数字之前没有被访问过，那么就不能从f[pre_state][pre_last]转移到f[state][last]，否则就有f[state][last] +\= f[pre_state][pre_last]。

最后附上python代码：

```python
class Solution(object):
    def numberOfPatterns(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """

        max_state = 512
        f = [[0] * 9 for _ in range(max_state)]

        f[0] = 1
        cnt_list = [0] * 10

        check_num = [[-1] * 9 for _ in range(9)]

        check_num[0][2] = check_num[2][0] = 1
        check_num[0][6] = check_num[6][0] = 3
        check_num[0][8] = check_num[8][0] = 4
        check_num[1][7] = check_num[7][1] = 4
        check_num[2][6] = check_num[6][2] = 4
        check_num[2][8] = check_num[8][2] = 5
        check_num[3][5] = check_num[5][3] = 4
        check_num[6][8] = check_num[8][6] = 7

        for state in range(1, 512):
            num_list = []
            for num in range(9):
                if (state & (1 << num)) == (1 << num):
                    num_list.append(num)

            for last in num_list:
                pre_state = state ^ (1 << last)
                if pre_state == 0:
                    f[state][last] += f[0]
                else:
                    for pre_last in num_list:
                        if pre_last == last:
                            continue
                        if check_num[pre_last][last] != -1:
                            check_state = (1 << check_num[pre_last][last])
                            if (pre_state & check_state) != check_state:
                                continue
                        f[state][last] += f[pre_state][pre_last]
            
                cnt_list[len(num_list)] += f[state][last]

        return sum(cnt_list[m : n + 1])
```
