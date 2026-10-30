---
title: "3389. 使字符串频率相等的最少操作次数"
aliases: ["yiduobo的每日leetcode 3389.使字符串频率相等的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30099638390"
zhihu_id: "30099638390"
zhihu_title: "yiduobo的每日leetcode 3389.使字符串频率相等的最少操作次数"
question_id: "3389"
question: "使字符频率相等的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-character-frequencies-equal/"
difficulty: "Hard"
rating: 2940
created: "2025-03-14T00:21:38+08:00"
updated: "2025-03-14T00:21:38+08:00"
upvotes: 2
comments: 0
---

# 3389. 使字符串频率相等的最少操作次数

> **[yiduobo的每日leetcode 3389.使字符串频率相等的最少操作次数](https://zhuanlan.zhihu.com/p/30099638390) · 知乎 · 2025-03-14 · 赞同 2**
> 力扣：[3389. 使字符频率相等的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-character-frequencies-equal/) · Hard · 灵茶山艾府：[枚举+DP+分类讨论+优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3389.使字符串频率相等的最少操作次数

[3389. 使字符频率相等的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-make-character-frequencies-equal/)

题目给出一个字符串s，可以对s执行以下操作任意次：

从s中删除一个字符。

往s中添加一个字符。

将s中的一个字母变为字母表中的下一个字母，另外注意这个操作不能将'z'变成'a'。

问至少需要执行多少次操作才能使得s中每种字符出现次数都相等。

---

题目要求将s中每种字符的出现次数都变成一样，那么一个自然的想法就是枚举最终字符串中每种出现的次数t，将原始s中的每种字符要么变为出现t次，要么全部去掉。

对于题目中的三种操作，如果仅考虑插入和删除操作是比较好处理的。不妨设字母表中第index种字符在s中出现的次数为cnt[index]，那么：

1、若cnt[index] > t：

此时显然应该删掉cnt[index] - t个字符，所需的操作次数就是cnt[index] - t

2、若cnt[index] \= t：

此时无需操作，操作数为0

3、若cnt[index] \< t：

此时可以考虑添加t - cnt[index]个字符，或者将这cnt[index]个字符全部删除，所需的操作次数就是min(t - cnt[index], cnt[index])

其中情况1和情况2可以合并到一起，即cnt[index] >\= t时，操作次数为cnt[index] - t。

---

最后再考虑融合修改操作的处理方法。

首先可以明确的是，修改操作不应该跨两个字符修改，也就是说最多是将第index - 1种字符修改成第index种字符，而不应该将第index - 2种字符修改成第index - 1种字符，再修改成第index种字符。理由也很简单，对于跨两个字符修改的情况，完全可以先去掉准备修改的第index - 2种字符，然后再插入对应数量的第index种字符，总的操作次数与修改两次的操作次数相同。

另外，由于题目保证了只能向后修改，因此在这里就可以考虑用动态规划求解。

依然是枚举最终字符串中每种字符出现的次数t，令f[index]表示对s中的第0到第index种字符完成操作，且第index种字符的数目调整成了t个时的最少操作次数，g[index]则表示对s中的第0到第index种字符完成操作，且第index种字符的数目调整成了0个时的最少操作次数，那么：

1、对于f[0]和g[0]：

由于无法执行字符变换操作，因此只能将cnt[0]修改成t个来达成f[0]，即f[0] \= abs(cnt[0] - t)。同样的，也只能将全部的cnt[0]个字符去掉才能达成g[0]，即g[0] \= cnt[0]。

2、对于index > 0的情况：

g[index]的情况是比较直观的。由于要将cnt[index]个字符全部去掉，那么自然也不应该从接受上一种字符的变换操作，于是有g[index] \= min(f[index - 1], g[index - 1]) + cnt[index]。

而对于f[index]，由于可能出现从index - 1的字符变换的操作存在，因此需要分情况讨论：

2-1）若cnt[index] >\= t：

此时不应该接受上一种字符的变换操作，有f[index] \= min(f[index - 1], g[index - 1]) + cnt[index] - t

2-2）若cnt[index] \< t：

此时如果不接受上一种字符的变换操作，所需的操作次数就是min(f[index - 1], g[index - 1]) + t - cnt[index]。可以先使用这个值来更新f[index]。

接下来如果要接受上一种字符，则需要根据上一种字符的数量进一步分情况讨论。方便起见，记目前缺少的字符数量t - cnt[index]为d，那么：

2-2-1）若cnt[index - 1] > t：

若之前被删除字符的数目，即cnt[index - 1] - t大于等于d，那么从中取d个字符执行变换操作，就可以填补当前字符的缺口，对于第index种字符则无需操作，于是有f[index] \= f[index - 1]。

反之若之前被删除字符的数目小于d，那么在这里则还需要填补d - (cnt[index - 1] - t)个字符，所需的操作次数就是d - (cnt[index - 1] - t)。需要注意这里不应该考虑从第index - 1种字符串强行取d个字符进行变换，其他全部删除这种方案，因为这样一来所需的操作次数就是cnt[index - 1] > t，而采取上面填补的方案需要的操作数为d - (cnt[index - 1] - t)，而d \= t - cnt[index] \< t，显然是不优的。对于这种情况，就有f[index] \= f[index - 1] + d - (cnt[index - 1] - t)。

综合起来，就有f[index] \= f[index - 1] + max(0, d - (cnt[index - 1] - t)。

2-2-2）若cnt[index - 1] \< t：

此时显然不需要考虑先插入若干个第index - 1种字符，再变换成第index种字符这种方案，因为这样必然不如直接插入第index种字符。也就是说这种情况下只需要考虑将第index - 1种字符中取出部分变换为第index种字符，然后将剩下的全部去掉。

那么当cnt[index - 1] >\= d时，对于第index种字符就无需操作，于是有f[index] \= g[index - 1]。

反之当cnt[index - 1] \< d时，还需要补充d - cnt[index - 1]个字符，于是有f[index] \= g[index - 1] + d - cnt[index - 1]。

综合起来，就有f[index] \= g[index - 1] + max(0, d - cnt[index - 1])。

计算完成后，最终答案就是min(f[-1], g[-1])。另外注意到每一列的f和g都只与上一轮有关，于是可以使用变量迭代省去f和g的空间。

最后附上python代码：

```python
class Solution(object):
    def makeStringGood(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        cnt = [0] * 26
        for char in s:
            cnt[ord(char) - 97] += 1
        
        ma = max(cnt)
        res = len(s)

        for t in range(1, ma + 1):
            f = abs(cnt[0] - t)
            g = cnt[0]

            for index in range(1, 26):
                if cnt[index] >= t:
                    new_f = min(f, g) + cnt[index] - t
                else:
                    new_f = min(f, g) + t - cnt[index]
                    if cnt[index - 1] > t:
                        new_f = min(new_f, f + max(0, t - cnt[index] - (cnt[index - 1] - t)))
                    elif cnt[index - 1] < t:
                        new_f = min(new_f, g + max(0, t - cnt[index] - cnt[index - 1]))
                new_g = min(f, g) + cnt[index]

                f, g = new_f, new_g

            res = min(res, min(f, g))

        return res
```
