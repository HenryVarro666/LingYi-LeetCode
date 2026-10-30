---
title: "2306. 公司命名"
aliases: ["yiduobo的每日leetcode 2306.公司命名"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/string", "leetcode/enumeration", "题单/数学算法", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/555395856"
zhihu_id: "555395856"
zhihu_title: "yiduobo的每日leetcode 2306.公司命名"
question_id: "2306"
question: "公司命名"
problem_url: "https://leetcode.cn/problems/naming-a-company/"
difficulty: "Hard"
rating: 2305
created: "2022-08-19T00:38:12+08:00"
updated: "2022-08-19T00:38:12+08:00"
upvotes: 0
comments: 0
---

# 2306. 公司命名

> **[yiduobo的每日leetcode 2306.公司命名](https://zhuanlan.zhihu.com/p/555395856) · 知乎 · 2022-08-19 · 赞同 0**
> 力扣：[2306. 公司命名](https://leetcode.cn/problems/naming-a-company/) · Hard · 灵茶山艾府：[两种方法：按照首字母分组/按照后缀分组（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2306.公司命名

[力扣](https://leetcode.cn/problems/naming-a-company/)

题目的数据规模比较大，直接两两枚举idea肯定是行不通的。注意到题目中是互换idea的首字母，那么不妨从首字母出发来考虑。

根据题目给出的命名规则，首先可以明确的一点是相同首字母的名称是不可能进行互换的。那么对于不同首字母，不妨设cnt[first]表示以first为首字母的单词数目，对于字母first_a和字母first_b，理论上可以产出的公司名称就有cnt[first_a] \* cnt[first_b] \* 2个。

但是注意到样例中coffee和toffee也是不能互换的，原因就在于二者除首字母外完全一样。方便起见，在这里称这种情况为body部分相同。对于first_a和first_b，也可能存在某些idea会出现body相同的情况，这些idea不能与另一方的任意idea进行交换操作。

到了这里，一个自然的想法就是在一开始在统计cnt的同时，也顺便将body分离出来，然后使用body作为key，记录有哪些首字符出现了body相同的情况。然后枚举所有的body，对于某个body，可能有若干个首字母都有同一个body，两两枚举这些首字母，并使用一个数组conflict记录出现相同body的情况总数。

值得一提的是，在这里可以直接这样统计conlict的数量是因为题目保证了idea不会重复出现，因此对于一组first_a和first_b，只需要将conflict[first_a][first_b]和conflict[first_b][first_a]分别加上1就可以了。

有了conflict之后，对于first_a和first_b，conflict[first_a][first_b]和conlict[first_b][first_a]就表示了以first_a和first_b为首字母的idea中不能进行交换的idea数量，因此实际上通过交换first_a和first_b可以得到的合法公司名称的数目就是

(cnt[first_a] - conflict[first_a][first_b]) \* (cnt[first_b] - conflict[first_b][first_a]) \* 2

于是在预处理好cnt和conflict后，只需要枚举所有first_a和first_b，然后计算可以得到的合法公司名称并累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def distinctNames(self, ideas):
        """
        :type ideas: List[str]
        :rtype: int
        """

        cnt_dict = {}
        same_body = {}
        for idea in ideas:
            first_asc = ord(idea[0]) - 97
            cnt_dict[first_asc] = cnt_dict.get(first_asc, 0) + 1
        
            body = idea[1:]
            if body not in same_body:
                same_body[body] = []
            same_body[body].append(first_asc)

        n = len(ideas)
        res = 0

        conflict = [[0] * 26 for _ in range(26)]
        for same_body_ascs in same_body.values():
            for i in range(len(same_body_ascs) - 1):
                for j in range(i + 1, len(same_body_ascs)):
                    conflict[same_body_ascs[i]][same_body_ascs[j]] += 1
                    conflict[same_body_ascs[j]][same_body_ascs[i]] += 1

        for asc_a in range(25):
            for asc_b in range(asc_a + 1, 26):
                if asc_a == asc_b:
                    continue
                
                res += (cnt_dict.get(asc_a, 0) - conflict[asc_a][asc_b]) * (cnt_dict.get(asc_b, 0) - conflict[asc_b][asc_a]) * 2

        return res
```
