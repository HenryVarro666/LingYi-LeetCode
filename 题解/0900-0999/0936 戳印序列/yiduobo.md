---
title: "936. 戳印序列"
aliases: ["yiduobo的每日leetcode 936.戳印序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/357913412"
zhihu_id: "357913412"
zhihu_title: "yiduobo的每日leetcode 936.戳印序列"
question_id: "936"
question: "戳印序列"
problem_url: "https://leetcode.cn/problems/stamping-the-sequence/"
created: "2021-03-17T22:41:59+08:00"
updated: "2021-03-17T22:41:59+08:00"
upvotes: 0
comments: 0
---

# 936. 戳印序列

> **[yiduobo的每日leetcode 936.戳印序列](https://zhuanlan.zhihu.com/p/357913412) · 知乎 · 2021-03-17 · 赞同 0**
> 力扣：[936. 戳印序列](https://leetcode.cn/problems/stamping-the-sequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

936.戳印序列

[力扣](https://leetcode-cn.com/problems/stamping-the-sequence/)

首先，对于某一次戳印来说，其如果被其他戳印完全覆盖住，那么这一次戳印就没有进行的必要了，因此对于可能存在的戳印，会有以下几种情况：

1、完全没有被覆盖

2、被覆盖住头部的某些字符

3、被覆盖住尾部的某些字符

4、被同时覆盖住头部和尾部的某些字符

这里需要注意可能出现情况4，我一开始想利用正反两趟kmp获取从每个字符开始的最长可匹配的正反戳印序列来适配情况2和情况3，然后使用贪心法来处理，但是这个做法由于无法处理情况4导致出错。

回到题目，由于题目是要求出一个戳印序列，因此对于这个序列的最后一次操作，其必然在最终的target上留下来一个完整的stamp，那么我们可以先找到这个stamp的位置，而这个stamp会将当前的target分为两个部分，那么我们可以递归处理这两个部分，而对于最后这个stamp所处的位置，我们可以视为长度为len(stamp)的通配字符，那么在每次递归时头尾都可能出现通配字符，然后我们再继续寻找当前处理的target最后一次戳印的位置即可。

例如样例2中的abca以及aabcaca，首先我们可以找到中间出现的完整的abca，那么此时问题就可以转化成使用stamp获取a\*\*\*\*以及\*\*\*\*ca。当然这里的\*不需要全部用完。

不过上面这个做法有一个问题就是由于首尾通配符的长度在变化，因此每次都需要从stamp的各个位置开始进行对比匹配，时间复杂度达到了O(len(target) \* (len(stamp) ^ 2))。而如果想进行预处理的话，上面情况4的存在导致不能简单使用首尾匹配，可能会遇到stamp中多处匹配的问题，例如当前处理的target为\*\*...\*\*ab\*\*...\*\*，而stamp为abcabcabc，那么在target中的ab可能匹配上stamp中的某个ab，例如当target为ab\*\*\*\*\*\*\*时ab匹配的就是stamp中头部的ab，而\*\*\*\*\*\*\*ab则是匹配stamp中尾部的ab，如果要在预处理时考虑所有可能的情况那与不进行预处理并没有时间复杂度上的差别。

以上做法是从串的角度出来，我们不妨换个思路，从字母的角度出发。依然是采用倒推法，不过这次是遍历最后一个stamp中的所有字符，然后对于某个字符target[now]，设stamp的长度为n，那么该字符将会影响到[now - n + 1 \~ now]，[now - n + 2 \~ now + 1]，...，[now \~ now + n - 1]这些可能存在的候选stamp，那么我们对于这些候选stamp更新target[now]为通配符。若此时某个候选stamp由于target[now]变为通配符从而能够匹配上stamp，那么就将这个候选stamp中的每个字符进行与target[now]同样的处理。这里需要注意的是，这里每个字符只需要处理一次即可，而对于这些候选stamp，则可能先通过一趟预处理获取到哪些字符是需要通配符来进行匹配的。

这样一来，整体时间复杂度就降到了O(len(target) \* len(stamp))。

最后附上python代码：

```python
class Solution(object):
    def movesToStamp(self, stamp, target):
        """
        :type stamp: str
        :type target: str
        :rtype: List[int]
        """

        m = len(target)
        n = len(stamp)

        f = []
        res = []
        used = [False] * m
        q = []
        for i in range(m - n + 1):
            f.append([set(), set()])
            for j in range(n):
                if target[i + j] == stamp[j]:
                    f[-1][0].add(i + j)
                else:
                    f[-1][1].add(i + j)

            if len(f[-1][1]) == 0:
                res.append(i)
                for j in range(i, i + n):
                    if not used[j]:
                        used[j] = True
                        q.append(j)

        head = 0
        tail = len(q)
        while head < tail:
            now = q[head]
            head += 1
            l = max(0, now - n + 1)
            r = min(m - n, now)
            for index in range(l, r + 1):
                if now in f[index][1]:
                    f[index][1].remove(now)
                    if len(f[index][1]) == 0:
                        res.append(index)
                        for pos in f[index][0]:
                            if not used[pos]:
                                used[pos] = True
                                q.append(pos)
                                tail += 1
        
        flag = True
        for index in range(m):
            if not used[index]:
                flag = False
                break

        if flag:
            return res[::-1]

        return []
```
