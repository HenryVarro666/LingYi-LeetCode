---
title: "1169. 查询无效交易"
aliases: ["yiduobo的每日leetcode 1169.查询无效交易"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/379046214"
zhihu_id: "379046214"
zhihu_title: "yiduobo的每日leetcode 1169.查询无效交易"
question_id: "1169"
question: "查询无效交易"
problem_url: "https://leetcode.cn/problems/invalid-transactions/"
created: "2021-06-08T23:52:30+08:00"
updated: "2021-06-08T23:52:30+08:00"
upvotes: 0
comments: 0
---

# 1169. 查询无效交易

> **[yiduobo的每日leetcode 1169.查询无效交易](https://zhuanlan.zhihu.com/p/379046214) · 知乎 · 2021-06-08 · 赞同 0**
> 力扣：[1169. 查询无效交易](https://leetcode.cn/problems/invalid-transactions/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1169.查询无效交易

[力扣](https://leetcode-cn.com/problems/invalid-transactions/)

由于题目中给出的交易总数不超过1000，因此我在这里是采用的比较暴力的做法，先逐个枚举交易，将其中金额超过1000的交易加入答案当中，接下来两两枚举交易，比较这两个交易是否满足名称相同，时间间隔在60分钟以内，且城市不同。若满足，则将这两笔交易都加入到答案当中。

当然，为了在比较名称和城市时避免过多的字符串比较操作，我在逐个枚举交易判断金额的同时也建立了名称到序号以及城市到序号的映射，之后比较时直接比较数字就好了。

最后附上python代码：

```python
class Solution(object):
    def invalidTransactions(self, transactions):
        """
        :type transactions: List[str]
        :rtype: List[str]
        """

        n = len(transactions)
        flag = [False] * n

        name_dict = {}
        name_cnt= 0
        city_dict = {}
        city_cnt = 0

        tmp_list = []

        for i in range(n):
            name, t, m, city = transactions[i].split(',')
            if int(m) > 1000:
                flag[i] = True
            
            if name not in name_dict:
                name_dict[name] = name_cnt
                name_cnt += 1

            if city not in city_dict:
                name_dict[city] = city_cnt
                city_cnt += 1

            tmp_list.append([name, int(t), city])

        for i in range(n - 1):
            for j in range(i + 1, n):
                if tmp_list[i][0] == tmp_list[j][0] and abs(tmp_list[i][1] - tmp_list[j][1]) <= 60 and tmp_list[i][2] != tmp_list[j][2]:
                    flag[i] = flag[j] = True
        
        res = []
        for i in range(n):
            if flag[i]:
                res.append(transactions[i])
        
        return res
```
