---
title: "1449. 数位成本和为目标值的最大数字"
aliases: ["yiduobo的每日leetcode 1449.数位成本和为目标值的最大数字"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/三-背包", "题单/动态规划/专题-输出具体方案-打印方案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/411549539"
zhihu_id: "411549539"
zhihu_title: "yiduobo的每日leetcode 1449.数位成本和为目标值的最大数字"
question_id: "1449"
question: "数位成本和为目标值的最大数字"
problem_url: "https://leetcode.cn/problems/form-largest-integer-with-digits-that-add-up-to-target/"
difficulty: "Hard"
rating: 1927
created: "2021-09-17T22:44:50+08:00"
updated: "2021-09-17T22:44:50+08:00"
upvotes: 0
comments: 0
---

# 1449. 数位成本和为目标值的最大数字

> **[yiduobo的每日leetcode 1449.数位成本和为目标值的最大数字](https://zhuanlan.zhihu.com/p/411549539) · 知乎 · 2021-09-17 · 赞同 0**
> 力扣：[1449. 数位成本和为目标值的最大数字](https://leetcode.cn/problems/form-largest-integer-with-digits-that-add-up-to-target/) · Hard · 灵茶山艾府：[完全背包 + 输出具体方案（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1449.数位成本为目标值的最大数字

[力扣](https://leetcode-cn.com/problems/form-largest-integer-with-digits-that-add-up-to-target/)

拿到题目可以发现是很明显的背包问题，即f[i]表示成本和为i所能得到的最大数字。不过在这里，直接保存数字显然是不行的，因为在极限情况下，这个数字可能长达5000位。

接下来分析一下数字的构成。首先，显然有数字的数目越多，数字就越大。接下来，为了使得数字最大，肯定是要将数字按从大到小填充高位到低位。

根据上面两个结论，此时就无需储存具体构成的数字，而是只需要储存选择了哪些数字集合。对于两个数字集合A和B，首先判断哪个长度更长，若长度相同，则可以从9开始向1进行遍历，判断哪个集合中当前的数字更多。

于是现在得到了一种做法。令f[i][0]表示数位和为target时所能拿到的最多数字数组，f[i][j]则表示此种情况下数字j的个数。对于f[i]，从1到9遍历，设当前遍历到num，其对应的代价为c。若满足i \= c，或i > c同时f[i - c][0] > 0，那么就有：

1、若f[i][0] \< f[i - c][0] + 1，说明在f[i - c]的基础上再加入num的数字总数要多余当前f[i]的数字总数，因此此时应当将f[i]赋值为f[i - c]，同时将f[i][0]以及f[i][num]都加上1

2、若f[i][0] \= f[i - c][0] + 1，且对比各个数位时发现f[i - c]在加入num之后要由于f[i][0]，那么此时同样是将f[i]复制为f[i - c]，并将f[i][0]以及f[i][num]都加上1

动态规划结束后，若此时的f[target][0] \= 0，说明没有可行的选择方案，那么返回'0'，否则按9到1的顺序遍历f[target]，并组合出最终答案返回。

另外，还有一个小优化是对于两个cost相同的数字，较小的那个就没有用了，于是可以先遍历一趟cost数组，选出其中有用的数字。

最后附上python代码：

```python
class Solution(object):
    def largestNumber(self, cost, target):
        """
        :type cost: List[int]
        :type target: int
        :rtype: str
        """

        cost_dict = {}
        for num in range(9, 0, -1):
            c = cost[num - 1]
            if c not in cost_dict:
                cost_dict[c] = num
        
        f = [[0] * 10 for _ in range(target + 1)]
        for i in range(1, target + 1):
            for c, num in cost_dict.items():
                if i == c or (i > c and f[i - c][0] > 0):
                    if f[i][0] < f[i - c][0] + 1:
                        f[i] = f[i - c][:]
                        f[i][0] += 1
                        f[i][num] += 1
                    elif f[i][0] == f[i - c][0] + 1:
                        flag = False
                        tmp = f[i - c][:]
                        tmp[num] += 1
                        for compare_num in range(9, 0, -1):
                            if f[i][compare_num] < tmp[compare_num]:
                                flag = True
                                break
                            elif f[i][compare_num] > tmp[compare_num]:
                                break
                        
                        if flag:
                            f[i] = f[i - c][:]
                            f[i][0] += 1
                            f[i][num] += 1
        
        if f[target][0] == 0:
            return '0'
        return ''.join([str(num) * f[target][num] for num in range(9, 0, -1)])
```
