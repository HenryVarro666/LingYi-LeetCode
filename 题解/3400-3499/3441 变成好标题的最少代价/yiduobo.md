---
title: "3441. 变成好标题的最少代价"
aliases: ["yiduobo的每日leetcode 3441.变成好标题的最少代价"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "题单/动态规划", "题单/贪心算法", "题单/动态规划/五-划分型-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-输出具体方案-打印方案", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1891708539459858479"
zhihu_id: "1891708539459858479"
zhihu_title: "yiduobo的每日leetcode 3441.变成好标题的最少代价"
question_id: "3441"
question: "变成好标题的最少代价"
problem_url: "https://leetcode.cn/problems/minimum-cost-good-caption/"
difficulty: "Hard"
rating: 2765
created: "2025-04-05T05:26:33+08:00"
updated: "2025-04-05T05:26:33+08:00"
upvotes: 1
comments: 0
---

# 3441. 变成好标题的最少代价

> **[yiduobo的每日leetcode 3441.变成好标题的最少代价](https://zhuanlan.zhihu.com/p/1891708539459858479) · 知乎 · 2025-04-05 · 赞同 1**
> 力扣：[3441. 变成好标题的最少代价](https://leetcode.cn/problems/minimum-cost-good-caption/) · Hard · 灵茶山艾府：[两种方法：枚举字母+DP / 中位数贪心+DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3441.变成好标题的最少代价

[3441. 变成好标题的最少代价 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-cost-good-caption/description/)

题目给出一个长度为n的字符串caption，如果字符串中每个字符都位于连续出现至少3次的组中，那么就称这个字符串是好标题。

例如aaabbb和aaaaccc都是好标题，但是aabbb和ccccd都不是好标题。

现在可以对字符串执行任意次操作，每次操作可以选择某个下标index，将caption[index]变为其在字母表中的前一个字符或者后一个字符。需要注意在这里不能将a变成z，也不能将z变成a。

现在要求使用尽量少的操作次数，将caption变为好标题。如果存在多种可行的好标题，则返回字典序最小的那个。若无法得到好标题，则返回空字符。

首先考虑特殊情况。当caption的长度小于3时，必然无法得到好标题，此时直接返回空字符串。

反过来，若caption的长度大于等于3时，在不考虑代价的情况下可以将其全部变为某种字符，也就是说必然可以得到好标题。接下来考虑如何计算最少操作次数，以及对应的好标题。

一种自然的想法是使用动态规划来进行计算，因为连续出现的组是非常明显的划分问题。令f[index]表示将caption[0]到caption[index]这一段变为好标题所需的最少操作次数，那么对于f[index]，可以枚举最后这一段的起点p，那么就有f[index] \= min(f[p - 1] + cost(p, index))，其中cost(p, index)是将caption[p]到caption[index]这一段变为相同字符所需的最少操作次数。

可以发现，即使不考虑计算cost的开销，在这里的时间复杂度依然是O(n^2)的，需要进行优化。

注意到题目中对于好标题的限制是基于长度为3的组，那么对于p的选择，index - p的大小就不应该大于等于6，因为所有长度大于等于6的组都可以至少拆分出一个长度为3的组出去，而将两个较短的组中字符分别变为相同所需的代价，显然小于等于将整个大组中所有字符变为相同的代价，因此p只需考虑index - 2、index - 3、index - 4这三个位置就行了。

另一方面，对于将caption[p]到caption[index]变为相同这一问题，则可以使用经典的贪心法，将所有字符都变为中位数字符就行了。由于p的取值范围优先，在这里可以直接排序然后一趟遍历，无需进行额外的优化。

接下来的问题就是如何得到字典序最小的字符串。对于字典序最小方案这类问题，一种常见的处理方法就是倒序遍历，然后记录在当前f取最优值时对应的最优后缀字符串。这种处理方法的原理与基数排序类似，越重要的东西就放到越后面再处理。

那么在这里就可以将f\[index\]的定义修改为将caption\[index\]到caption\[-1\]这一段变为好标题所需的最少操作次数，然后p的取值变为index + 2、index + 3、index + 4之一。另外为了能构造出最终答案，还需要使用nxt记录每个位置是从哪里转移过来的，即nxt\[index\]表示f\[index\]是从f\[nxt\[index\]\]转移过来的。

当然，在这里直接记录f[index]对应的整个后缀字符串显然是不行的，因为这样的话时间复杂度就又退化回O(n^2)了，但是依然可以利用至少连续出现3次这一性质，令fill[index]表示当f[index]取最优值时应该将caption[index]修改成什么字符，那么：

1、对于p \= index + 2时：

此时需要将caption[index]、caption[index + 1]、caption[index + 2]都变为这三个字符的中位数字符，不妨设为m[index, 3]表示caption[index: index + 3]这些字符的中位数字符。那么此时得到的后缀字符串的前缀s就是m[index, 3]重复3次，再加上fill[index + 3]重复3次。

这里m[index, 3]重复3次是因为将caption[index]到caption[index + 2]都变成了m[index, 3]，然后fill[index + 3]重复3次是因为对于f[index + 3]而言，其首字符，也就是fill[index + 3]至少连续出现了3次。

这种情况所需的总代价cost \= f[index + 3] + calc(index, 3)，这里calc(index, 3)表示将caption[index: index + 3]都变为m[index, 3]所需的代价，计算方法不变，依然是将caption[index: index + 3]这些字符从小到大进行排序，那么m[index, 3]就是排序后字符数组中下标为1的字符。接下来一趟遍历，计算将这些字符都变为m[index, 3]所需的代价即可。

2、对于p \= index + 3时：

与情况1类似，此时得到的前缀s应该是m[index, 4]重复4次，再加上fill[index + 4]重复3次，cost则为f[index + 3] + calc(index, 4)。

3、对于p \= index + 4时：

同样的，此时的前缀s应该是m[index, 5]重复5次，再加上fill[index + 5]重复3次，cost则为f[index + 5] + calc(index, 5)。

接下来就可以对比上面三种情况，取其中最小的cost作为f[index]，然后将最小的cost对应的，且字典序最小的s的首字符s[0]作为fill[index]，然后记录nxt[index]为最小的cost以及字典序最小的s对应的p + 1即可。

值得一提的是，上面的s只对比了前缀的前6个字符，但是也已经足够了，因为对于前6个字符相同，且对应的cost也相同的情况，相当于从caption[index]开始，至少连续出现了6次相同的字符，那么分离掉前3个字符后，无论第7个字符是什么，前6个字符中剩下的后3个字符也达成了单独成组的条件，因此完全可以先将前3个字符先分离出去形成一段，也就是直接取p \= index + 2这种。

计算完成后，只需从index \= 0开始向后构造答案。对于当前的index，其填充了nxt[index] - index个fill[index]，将这些字符加入答案，然后将index迭代到nxt[index]，直到index来到字符串末尾为止。

最后附上python代码：

```python
class Solution(object):
    def minCostGoodCaption(self, caption):
        """
        :type caption: str
        :rtype: str
        """
        
        if len(caption) < 3:
            return ''
        
        n = len(caption)
        f = [None] * (n + 1)
        fill = [None] * (n + 1)
        nxt = [None] * (n + 1)

        f[n] = 0
        fill[n] = '@'

        def calc(char_list):
            m = len(char_list)
            mid = (m - 1) // 2
            target = char_list[mid]
            cost = 0
            for index in range(mid):
                cost += ord(char_list[mid]) - ord(char_list[index])
            for index in range(mid + 1, m):
                cost += ord(char_list[index]) - ord(char_list[mid])
            return cost

        for index in range(n - 3, -1, -1):
            best_cost = None
            best_nxt = None
            best_s = ""

            if index + 3 <= n and f[index + 3] is not None:
                char_list = sorted(list(caption[index: index + 3]))
                cost = f[index + 3] + calc(char_list)
                s = char_list[1] * 3 + fill[index + 3] * 3
                if best_cost is None or cost < best_cost or (cost == best_cost and s < best_s):
                    best_cost = cost
                    best_nxt = index + 3
                    best_s = s
            
            if index + 4 <= n and f[index + 4] is not None:
                char_list = sorted(list(caption[index: index + 4]))
                cost = f[index + 4] + calc(char_list)
                s = char_list[1] * 4 + fill[index + 4] * 3
                if best_cost is None or cost < best_cost or (cost == best_cost and s < best_s):
                    best_cost = cost
                    best_nxt = index + 4
                    best_s = s
            
            if index + 5 <= n and f[index + 5] is not None:
                char_list = sorted(list(caption[index: index + 5]))
                cost = f[index + 5] + calc(char_list)
                s = char_list[2] * 5 + fill[index + 5] * 3
                if best_cost is None or cost < best_cost or (cost == best_cost and s < best_s):
                    best_cost = cost
                    best_nxt = index + 5
                    best_s = s
            
            if best_cost is not None:
                f[index] = best_cost
                nxt[index] = best_nxt
                fill[index] = best_s[0]
        
        res = ""
        index = 0
        while index != n:
            res += fill[index] * (nxt[index] - index)
            index = nxt[index]
        
        return res
```
