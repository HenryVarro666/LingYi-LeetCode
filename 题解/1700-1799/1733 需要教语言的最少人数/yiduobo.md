---
title: "1733. 需要教语言的最少人数"
aliases: ["yiduobo的每日leetcode 1733.需要教语言的最少人数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/enumeration", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452670440"
zhihu_id: "452670440"
zhihu_title: "yiduobo的每日leetcode 1733.需要教语言的最少人数"
question_id: "1733"
question: "需要教语言的最少人数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-people-to-teach/"
difficulty: "Medium"
rating: 1984
created: "2022-01-02T22:15:44+08:00"
updated: "2022-01-02T22:15:44+08:00"
upvotes: 4
comments: 0
---

# 1733. 需要教语言的最少人数

> **[yiduobo的每日leetcode 1733.需要教语言的最少人数](https://zhuanlan.zhihu.com/p/452670440) · 知乎 · 2022-01-02 · 赞同 4**
> 力扣：[1733. 需要教语言的最少人数](https://leetcode.cn/problems/minimum-number-of-people-to-teach/) · Medium · 灵茶山艾府：[两种方法：枚举 / 计数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1733.需要教语言的最少人数

[力扣](https://leetcode-cn.com/problems/minimum-number-of-people-to-teach/)

题目中是不存在a是b的朋友，a也是c的朋友，所以a帮助b和c当中间翻译的情况，也就是说只需要考虑直连的两个朋友之间是否语言相同。那么在这里可以枚举每一对朋友，然后枚举每一种语言，借助哈希表判断这两个人是否都会当前这种语言，如果会那么这两个人就不需要学习额外语言。如果没有一种语言是两个人都会的，那么这两个人就需要学习额外的语言，在这里可以使用一个集合user_set来记录所有需要额外学习语言的人。

得到user_set之后，需要选择一种语言让这些人学习。为了使得学习的人最少，那么显然应该选择user_set中的人会得最多的那种语言，因此可以使用一个哈希表统计user_set中会说各种语言的人数，设其中会的人最多的那种语言有max_user个人会，那么剩下不会这门语言的这些人就需要学习这门语言，因此答案就是len(user_set) - user_set。

最后附上python代码：

```python
class Solution(object):
    def minimumTeachings(self, n, languages, friendships):
        """
        :type n: int
        :type languages: List[List[int]]
        :type friendships: List[List[int]]
        :rtype: int
        """

        learned_set = [set() for _ in range(n)]
        for user_id, user_language in enumerate(languages):
            for language in user_language:
                learned_set[language - 1].add(user_id)
        
        user_set = set()
        for x, y in friendships:
            x -= 1
            y -= 1
            flag = False
            for language in range(n):
                if x in learned_set[language] and y in learned_set[language]:
                    flag = True
                    break
            
            if not flag:
                user_set.add(x)
                user_set.add(y)

        language_cnt = {}
        for user in user_set:
            for language in languages[user]:
                language_cnt[language] = language_cnt.get(language, 0) + 1

        if not language_cnt:
            return 0

        return len(user_set) - max(language_cnt.values())
```
