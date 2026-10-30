---
title: "1125. 最小的必要团队"
aliases: ["yiduobo的每日leetcode 1125.最小的必要团队"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/动态规划/专题-输出具体方案-打印方案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/376143976"
zhihu_id: "376143976"
zhihu_title: "yiduobo的每日leetcode 1125.最小的必要团队"
question_id: "1125"
question: "最小的必要团队"
problem_url: "https://leetcode.cn/problems/smallest-sufficient-team/"
difficulty: "Hard"
rating: 2251
created: "2021-05-28T21:28:10+08:00"
updated: "2021-05-28T21:28:10+08:00"
upvotes: 0
comments: 0
---

# 1125. 最小的必要团队

> **[yiduobo的每日leetcode 1125.最小的必要团队](https://zhuanlan.zhihu.com/p/376143976) · 知乎 · 2021-05-28 · 赞同 0**
> 力扣：[1125. 最小的必要团队](https://leetcode.cn/problems/smallest-sufficient-team/) · Hard · 灵茶山艾府：[状压 0-1 背包，查表法 vs 刷表法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1125.最小的必要团队

[力扣](https://leetcode-cn.com/problems/smallest-sufficient-team/)

刚1124题想着996，这一题就想着优化组织架构，这一定是某一套题里面的两个小题。。。

回到题目，由于这里的skill最多只有16种，因此很容易想到使用状态压缩动态规划来解决问题。令f[i][state]表示前i个员工，拥有state中的技能时最少需要的员工数量。

那么我们首先需要预处理出每个员工具有的技能，接下来枚举每个员工，对于当前的员工i，设其拥有的技能为p[i]，那么我们需要枚举所有可能的state，接下来就有

f[i][new_state] \= min(f[i][new_state], f[i - 1][state] + 1)

其中new_state \= state | p[i]

注意到这里f[i]的状态只与f[i - 1]有关，同时由于这里的转移条件是按位或，因此也无需考虑正顺循环产生叠加的情况，那么就可以直接优化掉i这一维，变成

f[new_state] \= min(f[new_state], f[state] + 1)

其中new_state \= state | p[i]

由于题目最终需要求出具体的人员名单，因此我们对于每个new_state都需要记录其使用哪个state转移而来，同时还需要记录这个转移是使用了哪个员工的技能。

在动态规划结束之后，我们从state \= (1 \<\< n) - 1开始倒推，将过程中所有用到的员工加入答案即可。

最后附上python代码：

```python
class Solution(object):
    def smallestSufficientTeam(self, req_skills, people):
        """
        :type req_skills: List[str]
        :type people: List[List[str]]
        :rtype: List[int]
        """

        n = len(req_skills)
        skill_dict = {}
        for index, skill in enumerate(req_skills):
            skill_dict[skill] = index
        
        p = []
        for skill_list in people:
            tmp = 0
            for skill in skill_list:
                tmp |= (1 << skill_dict[skill])
            p.append(tmp)
        
        f = [None] * (1 << n)
        f[0] = 0
        fa = [None] * (1 << n)
        use = [None] * (1 << n)
        for i in range(len(p)):
            for state in range(1 << n):
                if f[state] is not None:
                    new_state = state | p[i]
                    if f[new_state] is None or f[new_state] > f[state] + 1:
                        f[new_state] = f[state] + 1
                        fa[new_state] = state
                        use[new_state] = i
            
        res = []
        now = (1 << n) - 1
        while now != 0:
            res.append(use[now])
            now = fa[now]
        
        return res
```
