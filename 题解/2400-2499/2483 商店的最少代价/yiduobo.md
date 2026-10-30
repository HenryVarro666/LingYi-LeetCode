---
title: "2483. 商店的最少代价"
aliases: ["yiduobo的每日leetcode 2483.商店的最少代价"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bian-li", "题单/动态规划", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/589190599"
zhihu_id: "589190599"
zhihu_title: "yiduobo的每日leetcode 2483.商店的最少代价"
question_id: "2483"
question: "商店的最少代价"
problem_url: "https://leetcode.cn/problems/minimum-penalty-for-a-shop/"
difficulty: "Medium"
rating: 1495
created: "2022-12-05T00:12:50+08:00"
updated: "2022-12-05T00:12:50+08:00"
upvotes: 0
comments: 0
---

# 2483. 商店的最少代价

> **[yiduobo的每日leetcode 2483.商店的最少代价](https://zhuanlan.zhihu.com/p/589190599) · 知乎 · 2022-12-05 · 赞同 0**
> 力扣：[2483. 商店的最少代价](https://leetcode.cn/problems/minimum-penalty-for-a-shop/) · Medium · 灵茶山艾府：[前后缀分解，一次遍历优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2483.商店的最少代价

[力扣](https://leetcode.cn/problems/minimum-penalty-for-a-shop/)

题目给出一个字符串，要求找出一个分割点，其左侧字符N的数目加上右侧字符Y的数目最小。对于这类问题，常规的做法就是先进行正反两趟遍历，预处理出前缀N的数目数组以及后缀Y的数目数组，最后再枚举所有分割点，根据前缀N和后缀Y之和来更新答案。

不过对于本题，也存在不需要使用额外空间的做法。

不妨设字符串中一共有k个字符Y，且长度为i的前缀中N的数量为cnt[i]。如果以位置p为分割点，那么其左侧一共有cnt[p]个字符N，从而可以推导出其左侧一共有p - cnt[p]个字符Y，而其右侧就有k - (p - cnt[p])个字符Y，因此总的代价就是cnt[p] + k - (p - cnt[p]) \= k + cnt[p] + cnt[p] - p

对于上面这个式子，由于k是常量，为了使得最终的代价最小，实际上就是要找出使得cnt[p] + cnt[p] - p最小的p，于是可以初始化答案和cnt为0，然后从左向右一趟遍历，在遍历过程中计算对应的cnt，并使用cnt和当前下标来更新最终答案。

最后附上python代码：

```python
class Solution(object):
    def bestClosingTime(self, customers):
        """
        :type customers: str
        :rtype: int
        """

        min_cnt = 0
        res = 0

        cnt = 0
        for index, c in enumerate(customers):
            if c == 'N':
                cnt += 1
            if cnt + cnt - (index + 1) < min_cnt:
                res = index + 1
                min_cnt = cnt + cnt - (index + 1)
        
        return res
```
