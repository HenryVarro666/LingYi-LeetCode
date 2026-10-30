---
title: "1452. 收藏清单"
aliases: ["yiduobo的每日leetcode 1452.收藏清单"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/411898251"
zhihu_id: "411898251"
zhihu_title: "yiduobo的每日leetcode 1452.收藏清单"
question_id: "1452"
question: "收藏清单"
problem_url: "https://leetcode.cn/problems/people-whose-list-of-favorite-companies-is-not-a-subset-of-another-list/"
created: "2021-09-18T22:54:33+08:00"
updated: "2021-09-18T22:54:33+08:00"
upvotes: 1
comments: 0
---

# 1452. 收藏清单

> **[yiduobo的每日leetcode 1452.收藏清单](https://zhuanlan.zhihu.com/p/411898251) · 知乎 · 2021-09-18 · 赞同 1**
> 力扣：[1452. 收藏清单](https://leetcode.cn/problems/people-whose-list-of-favorite-companies-is-not-a-subset-of-another-list/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1452.收藏清单

[力扣](https://leetcode-cn.com/problems/people-whose-list-of-favorite-companies-is-not-a-subset-of-another-list/)

如果将清单中的每个单词视为某种字符，那么题目中的每个清单就都可以视为一个字符串，而题目就变成了给出若干字符串，问有哪些字符不是其他字符串的子串。之前遇到过一模一样的题目，当时使用的是哈希，在这里我采用的是从长到短枚举每个清单，然后使用kmp算法来进行判断。

另外，当判断“字符”相等时，如果直接对比字符串，复杂度就比较高了，可以首先将清单中的所有字符串都收集起来，并建立起字符串到自然数的映射，然后判断自然数相等即可。

最后附上python代码：

```python
class Solution(object):
    def peopleIndexes(self, favoriteCompanies):
        """
        :type favoriteCompanies: List[List[str]]
        :rtype: List[int]
        """

        mapping_dict = {}
        fav_list = []
        company_cnt = 0
        for fav in favoriteCompanies:
            fav_list.append([])
            for company in fav:
                if company not in mapping_dict:
                    mapping_dict[company] = company_cnt
                    company_cnt += 1
                fav_list[-1].append(mapping_dict[company])
        
            fav_list[-1] = sorted(fav_list[-1])

        res = []
        n = len(fav_list)
        for index in sorted(range(n), key=lambda d:len(fav_list[d]), reverse = True):
            flag = True
            for c in res:
                if self.check(fav_list[index], fav_list[c]):
                    flag = False
                    break
            if flag:
                res.append(index)
        
        return sorted(res)

    def check(self, list1, list2):
        p = 0
        for num in list1:
            while p < len(list2) and list2[p] != num:
                p += 1
            if p == len(list2):
                return False
        
        return True
```
