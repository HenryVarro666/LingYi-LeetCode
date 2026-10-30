---
title: "LCP 69. Hello LeetCode!"
aliases: ["yiduobo的每日leetcode LCP69.Hello LeetCode!"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/hash-table", "leetcode/string", "leetcode/dynamic-programming", "leetcode/backtracking", "leetcode/bitmask", "题单/常用数据结构", "题单/动态规划", "题单/常用数据结构/编程能力强化训练", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/580554557"
zhihu_id: "580554557"
zhihu_title: "yiduobo的每日leetcode LCP69.Hello LeetCode!"
question_id: "LCP 69"
question: "Hello LeetCode!"
problem_url: "https://leetcode.cn/problems/rMeRt2/"
difficulty: "Hard"
created: "2022-11-05T02:49:37+08:00"
updated: "2022-11-05T02:49:37+08:00"
upvotes: 0
comments: 0
---

# LCP 69. Hello LeetCode!

> **[yiduobo的每日leetcode LCP69.Hello LeetCode!](https://zhuanlan.zhihu.com/p/580554557) · 知乎 · 2022-11-05 · 赞同 0**
> 力扣：[LCP 69. Hello LeetCode!](https://leetcode.cn/problems/rMeRt2/) · Hard · 灵茶山艾府：[预处理+状压DP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP69.Hello LeetCode!

[力扣](https://leetcode.cn/problems/rMeRt2/)

题目给出若干单词，可以花费一定的代价从单词中选出一些字母，问选出的字母刚好凑成helloleetcode时所需的最小代价是多少。

注意到题目中单词的长度都不超过8，那么就意味着每个单词最多只有2^8\=64种选择的方案。另一方面，由于每个单词、每种字母选择的代价与单词与字母自身无关，只与字母在单词中的位置有关，那么就可以先利用动态规划预处理出对于每种长度单词的每种选择字母方案所需的代价。具体来说，令f[i][j]表示长度为i的单词，选择字母的二进制表示为j时所需的代价。

例如样例中的engineer这个单词，选择第一个e和最后一个e，那么这种选择的二进制表示就是10000010，对应到的状态就是f[8][130]。

那么对于f[i][j]：

1、若j \= 0，显然有f[i][j] \= 0

2、若j > 0，那么j的二进制表示中必然有1。枚举j中所有1的位置k，可以选择拿走第k位上的这个字母，于是就有

f[i][j] \= f[i - 1][pre_state] + k \* (i - 1 - k)

其中pre_state是j移除掉k这一位之后的二进制表示。这一步的含义是拿走对应的字母后，剩下的就是从长度为i - 1的单词中拿走pre_state表示的字母，而拿走第k位上的字母时，其低位上有0到k - 1共k个字母，高位上则是n - 1 - k个字母，因此拿走这个字母的代价就是k \* (i - 1 - k)。

另一方面，在这里关于pre_state的计算则可以利用位运算来实现。j的第k位为(1 \<\< k)，不妨设其左侧和右侧部分分别为left_part和right_part，那么在这里需要将j从{left_part}{1}{right_part}变为{left_part}{right_part}。

为了将right_part提取出来，就可以用j与111...11做按位与运算，这里1的数量与right_part的长度相等，都是k，也就是right_part \= j & ((1 \<\< k) - 1)。得到right_part后，left_part就可以通过j与(1 \<\< k)以及right_part做异或操作得到，即left_part \= j ^ (1 \<\< k) ^ right_part。最后，将left_part与right_part拼接，此时应该将left_part右移一位，然后与left_part做按位或运算，即pre_state \= (left_part >> 1) | right_part。

得到pre_state后，按照上面的转移方程，使用f[i - 1][pre_state] + k \* (i - 1 - k)来更新f[i][j]即可。

---

得到了所有的f[i][j]之后，接下来可以枚举所有单词。对于当前单词word，可以根据其长度枚举所有可能的state，接下来根据枚举的state分离出word中对应位置上的字母。由于最终目标的helloleetcode中一共出现了7种字母，分别为h、e、l、o、t、c、d，出现次数分别为1、4、3、2、1、1、1，那么在这里枚举的state中出现的字母就必须属于这7种字母，且出现次数不能超过上面统计的次数。

在这里可以使用一个数组candidate统计所有可行的取字母方案，其中candidate[i]中记录的是word[i]所有可行的取字母方案，需要记录取出每种字母的数量，以及当前方案的代价。

---

得到candidate后，接下来的问题就是经典的背包问题了。不过在这里使用常规的高位背包状态表示在实现起来非常不优雅，那么在这里可以再进行一次编码，即给出一个7位的数字串，其中每一位对应的是h、e、l、o、t、c、d这7种字母当前出现的次数，接下来按照常规的背包算法计算填满这些字母的最小代价即可。

最后附上python代码：

```python
class Solution(object):
    def Leetcode(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        f = [[None] * 256 for _ in range(9)]
        f[0][0] = 0
        for i in range(1, 9):
            max_state = (1 << i) - 1
            f[i][0] = 0
            for j in range(1, max_state + 1):
                for k in range(i):
                    if j & (1 << k) == (1 << k):
                        right_part = j & ((1 << k) - 1)
                        left_part = (j ^ right_part ^ (1 << k)) >> 1
                        pre_state = left_part | right_part
                        if f[i - 1][pre_state] is not None and (f[i][j] is None or f[i][j] > f[i - 1][pre_state] + k * (i - 1 - k)):
                            f[i][j] = f[i - 1][pre_state] + k * (i - 1 - k)

        max_cnt = [1, 4, 3, 2, 1, 1, 1]
        candidate_list = []
        order = {'h' : 0, 'e' : 1, 'l' : 2, 'o': 3, 't': 4, 'c': 5, 'd': 6}

        for word in words:
            candidate_list.append([])
            max_state = (1 << len(word))
            for j in range(max_state):
                pos_list = []
                for k in range(len(word)):
                    if j & (1 << k) == (1 << k):
                        pos_list.append(k)

                flag = True
                cnt_list = [0] * 7
                for pos in pos_list:
                    if word[pos] not in order:
                        flag = False
                        break
                    cnt_list[order[word[pos]]] += 1

                if flag:
                    for index in range(7):
                        if cnt_list[index] > max_cnt[index]:
                            flag = False
                            break
                
                if flag:
                    candidate_list[-1].append([cnt_list[:], f[len(word)][j]])

        g = [-1] * 960
        g[0] = 0
        base = [2, 5, 4, 3, 2, 2, 2]
        multi_base = [1, 2, 10, 40, 120, 240, 480]
        for i in range(len(words)):
            for j in range(959, 0, -1):
                cnt_list = []
                tmp = j
                for index in range(7):
                    cnt_list.append(tmp % base[index])
                    tmp /= base[index]
                
                for candidate in candidate_list[i]:
                    flag = True
                    for index in range(7):
                        if cnt_list[index] < candidate[0][index]:
                            flag = False
                            break
                    
                    if flag:
                        pre_state = 0
                        for index in range(7):
                            pre_state += multi_base[index] * (cnt_list[index] - candidate[0][index])
                        
                        if g[pre_state] != -1 and (g[j] == -1 or g[j] > g[pre_state] + candidate[1]):
                            g[j] = g[pre_state] + candidate[1]
        
        return g[-1]
```
