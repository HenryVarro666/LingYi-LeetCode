---
title: "1307. 口算难题"
aliases: ["yiduobo的每日leetcode 1307.口算难题"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/391920275"
zhihu_id: "391920275"
zhihu_title: "yiduobo的每日leetcode 1307.口算难题"
question_id: "1307"
question: "口算难题"
problem_url: "https://leetcode.cn/problems/verbal-arithmetic-puzzle/"
created: "2021-07-21T22:22:54+08:00"
updated: "2021-07-21T22:22:54+08:00"
upvotes: 1
comments: 0
---

# 1307. 口算难题

> **[yiduobo的每日leetcode 1307.口算难题](https://zhuanlan.zhihu.com/p/391920275) · 知乎 · 2021-07-21 · 赞同 1**
> 力扣：[1307. 口算难题](https://leetcode.cn/problems/verbal-arithmetic-puzzle/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1307.口算难题

[力扣](https://leetcode-cn.com/problems/verbal-arithmetic-puzzle/)

看上去没有什么多项式算法可以解决这个问题，如果使用最朴素的回溯法，那么时间复杂度在最坏情况下为O(n \* n!)，其中n为数字的总数。n在这里最多为10，那么在极限情况下时间上可能有些问题。

回忆一下原来做填字竖式的一些技巧。例如样例1中的

SEND + MORE \= MONEY

两个四位数相加得到一个5位数，那么这里的M只能是1。

不过题目中可能出现多个竖式连加的情况，那么这里的技巧就不那么好用的。因此，不妨从这个技巧的深层原因出发进行分析。

如果我们把整数拆开，那么就可以得到

SEND \= S \* 1000 + E \* 100 + N \* 10 + D

MORE \= M \* 1000 + O \* 100 + R \* 10 + E

MONEY \= M \* 10000 + O \* 1000 + N \* 100 + E \* 10 + Y

化简之后可得

S \* 1000 + E \* 91 - N \* 90 + D - M \* 9000 - O \* 900 + R \* 10 - E \* 9 - Y \= 0

可以发现，其中-M \* 9000这一项的系数的绝对值相比其他项大得多，这就决定了M的取值不能太大。更具体的，有

M \* 9000 \= S \* 1000 + E \* 91 - N \* 90 + D - O \* 900 + R \* 10 - Y

对于等式右侧，我们可以简略得到一个上下限，从而推断出M的上下界。对于式子右侧，为了求得其上下限，一个自然的想法是对各项按系数的绝对值进行排序，那么就有

M \* 9000 \= S \* 1000 - O \* 900 + E \* 91 - N \* 90 + R \* 10 + D - Y

而这里的上限就是从左向右扫描，对于正系数则从9开始往下填充，而对于负系数则从0开始向上填充。另外，需要注意的是0不能填充在首字符，也就是S和M不能为0。于是有

M \* 9000 \<\= 9 \* 1000 - 0 \* 900 + 8 \* 91 - 1 \* 90 + 7 \* 10 + 6 - 2 \= 9712

从而可知M \<\= 1

同样的，对于下限就是从左向右扫描，对于正系数则从0开始向上填充，而对于负系数则从9开始向下填充。同样的，0也不能填充在S和M上。于是有

M \* 9000 >\= 1 \* 1000 - 9 \* 900 + 0 \* 91 - 8 \* 90 + 2 \* 10 + 3 - 7 \= -7804

从而可知M >\= 0

由于M是首字符，不能为0，因此M必然为1。

接下来考察系数绝对值第二大的S。由于此时我们在搜索回溯法的过程中已经确定了M的取值，那么只需要对于S后续的项按同样的方法求得上下限。方便起见，我们在求解上下限的时候先不考虑之前使用过哪些数字，这样一来可能稍微放大上限，缩小下限，但是若考虑之前已经使用的数值，那么这里的上下限是动态变化的，难以维护。

在这里，对于后续的式子

O \* 900 - E \* 91 + N \* 90 - R \* 10 - D + Y

上限为9 \* 900 - 0 \* 91 + 8 \* 90 - 1 \* 10 - 2 + 8 \= 8816

下限为0 \* 900 - 9 \* 91 + 1 \* 90 - 8 \* 10 - 7 + 3 \= -813

于是此时有

S \* 1000 \= M \* 9000 + O \* 900 - E \* 91 + N \* 90 - R \* 10 - D + Y

这里已经确定了M为1，因此有

S \* 1000 \<\= 9000 + 8816 \= 17816

S \* 1000 >\= 9000 - 813 \= 8187

因此可知S的上限为9，下限也是9，于是这一步就确定S为9。

接下来对于后续的字符，都按同样的做法求出上下限，然后逐个进行搜索回溯，直到某一时刻找出答案，或者无法继续向后。

需要注意的，这里M和S的取值只因是上下限相同，因此可以唯一确定，但是一般情况应当逐个尝试上下限之间的所有未使用数字来进行搜索回溯。

最后附上python代码：

```python
class Solution(object):
    def isSolvable(self, words, result):
        """
        :type words: List[str]
        :type result: str
        :rtype: bool
        """

        param_dict = {}
        first_set = set()
        for word in words:
            p = 1
            for index in range(len(word) - 1, -1, -1):
                char = word[index]
                param_dict[char] = param_dict.get(char, 0) + p
                p *= 10
            if len(word) > 1:
                first_set.add(word[0])

        p = 1
        for index in range(len(result) - 1, -1, -1):
            char = result[index]
            param_dict[char] = param_dict.get(char, 0) - p
            p *= 10
        
        if len(result) > 1:
            first_set.add(result[0])

        param_list = sorted(param_dict.items(), key=lambda d:-abs(d[1]))
        n = len(param_list)
        max_list = []
        min_list = []
        for p in range(1, n):
            max_used = [False] * 10
            min_used = [False] * 10
            ma = mi = 0
            for index in range(p, n):
                if param_list[index] == 0:
                    continue
                
                char, param = param_list[index]
                if param > 0:
                    for num in range(9, -1, -1):
                        if not max_used[num] and (num != 0 or char not in first_set):
                            max_used[num] = True
                            ma += param * num
                            break
                    for num in range(10):
                        if not min_used[num] and (num != 0 or char not in first_set):
                            min_used[num] = True
                            mi += param * num
                            break
                else:
                    for num in range(10):
                        if not max_used[num] and (num != 0 or char not in first_set):
                            max_used[num] = True
                            ma += param * num
                            break
                    for num in range(9, -1, -1):
                        if not min_used[num] and (num != 0 or char not in first_set):
                            min_used[num] = True
                            mi += param * num
                            break

            max_list.append(ma)
            min_list.append(mi)

        used = [False] * 10
        return self.dfs(0, n, 0, param_list, used, first_set, max_list, min_list, [])
     
    def dfs(self, level, n, now, param_list, used, first_set, max_list, min_list, res):
        char, param = param_list[level]
        if level == n - 1:
            if param < 0:
                if now < 0:
                    return False
                param = -param
                if now % param == 0:
                    tmp = now / param
                    if not used[tmp] and (tmp != 0 or char not in first_set):
                        return True
                    else:
                        return False
                else:
                   return False

            elif param > 0:
                if now > 0:
                    return False
                now = -now
                if now % param == 0:
                    tmp = now / param
                    if not used[tmp] and (tmp != 0 or char not in first_set):
                        return True
                    else:
                        return False
                else:
                    return False

            elif now != 0 or (n == 10 and not used[0] and char in first_set):
                return False
            else:
                return True
        
        char, param = param_list[level]
        if param == 0:
            if char not in first_set:
                return True
            for num in range(1, 10):
                if not used[num]:
                    used[num] = True
                    if self.dfs(level + 1, n, now, param_list, used, first_set, max_list, min_list):
                        return True
                    used[num] = False
            return False
        
        '''
        now + p * c + k = 0
        now + p * c + mi <= 0 <= now + p * c + ma
        p * c <= -now - mi
        p * c >= -now - ma
        '''

        if param > 0:
            upper = -now - min_list[level]
            if upper < 0:
                return False
            ma = min(upper / param, 9)
            
            bounder = -now - max_list[level]
            if param * 9 < bounder:
                return False
            elif bounder < 0:
                mi = 0
            else:
                mi = bounder / param
                if bounder % param != 0:
                    mi += 1
        else:
            upper = now + max_list[level]
            if upper < 0:
                return False
            ma = min(upper / -param, 9)

            bounder = now + min_list[level]
            if -param * 9 < bounder:
                return False
            elif bounder < 0:
                mi = 0
            else:
                mi = bounder / -param
                if bounder % -param != 0:
                    mi += 1

        for num in range(mi, ma + 1):
            if not used[num] and (num != 0 or char not in first_set):
                used[num] = True
                now += param * num
                res.append(num)
                if self.dfs(level + 1, n, now, param_list, used, first_set, max_list, min_list, res):
                    return True
                res.pop()
                now -= param * num
                used[num] = False
            
        return False
```
