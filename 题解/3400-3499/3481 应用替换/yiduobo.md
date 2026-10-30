---
title: "3481. 应用替换"
aliases: ["yiduobo的每日leetcode 3481.应用替换"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "题单/图论算法", "题单/图论算法/二-拓扑排序"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897401650886468292"
zhihu_id: "1897401650886468292"
zhihu_title: "yiduobo的每日leetcode 3481.应用替换"
question_id: "3481"
question: "应用替换"
problem_url: "https://leetcode.cn/problems/apply-substitutions/"
difficulty: "Medium"
created: "2025-04-21T22:20:26+08:00"
updated: "2025-04-21T22:20:26+08:00"
upvotes: 0
comments: 0
---

# 3481. 应用替换

> **[yiduobo的每日leetcode 3481.应用替换](https://zhuanlan.zhihu.com/p/1897401650886468292) · 知乎 · 2025-04-21 · 赞同 0**
> 力扣：[3481. 应用替换](https://leetcode.cn/problems/apply-substitutions/) · Medium · 灵茶山艾府：[记忆化搜索](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3481.应用替换

[3481. 应用替换 - 力扣（LeetCode）](https://leetcode.cn/problems/apply-substitutions/description/)

题目给出一个replacements映射，映射的数目不超过10组，其中每组都是一个双值列表[key, value]，key是一个大写字母，而value是一个长度最多为8，且其中可能包含0个或者更多格式为%\<key>%的占位符的非空字符串。所有的key都各不相同，同时不存在循环依赖的情况。

另外给出一个可能包含格式为%key%占位符的字符串text，其中每个key对应replacements中的一个键。

现在要求返回将所有%\<key>%都替换后的text字符串。

使用一个哈希表mapping记录每种key对应的去除掉所有占位符后得到的最终字符串，接下来遍历replacements中的所有映射，对于当前遍历到的[key, value]，使用一个指针p从value头部开始向后遍历。

若当前的value\[p\]为'%'，那么说明value\[p + 1\]是另一个key，此时应该递归求解value\[p + 1\]。为了得到value\[p + 1\]对应的value，则还需要使用一个哈希表replacements_dict来记录每种key对应的value，那么此时递归求解的就是\[value\[p + 1\], replacements_dict\[value\[p + 1\]\]\]。将得到的结果添加到mapping\[key\]中，然后将p向后移动三步，也就是跳过%key%这个部分需要的移动。

若当前的value[p]不为'%'，说明value[p]是一个常规的字符，此时应该将其加入到mapping[key]中，然后将p向后移动一步。

得到所有的[key, value]对应的mapping后，只需对text进行一趟遍历，将其中的%key%都替换为mapping[key]即可。

最后附上python代码：

```python
class Solution(object):
    def applySubstitutions(self, replacements, text):
        """
        :type replacements: List[List[str]]
        :type text: str
        :rtype: str
        """
        
        mapping = {}
        replacements_dict = {}
        for key, value in replacements:
            replacements_dict[key] = value

        def get(key, value, mapping):
            if key not in mapping:
                parts = []
                p = 0
                while p < len(value):
                    if value[p] == '%':
                        parts.append(get(value[p + 1], replacements_dict[value[p + 1]], mapping))
                        p += 3
                    else:
                        parts.append(value[p])
                        p += 1
                
                mapping[key] = ''.join(parts)
            
            return mapping[key]

        for key, value in replacements:
            if key not in mapping:
                get(key, value, mapping)
        
        res = []
        p = 0
        while p < len(text):
            if text[p] == '%':
                res.append(mapping[text[p + 1]])
                p += 3
            else:
                res.append(text[p])
                p += 1
        
        return ''.join(res)
```
