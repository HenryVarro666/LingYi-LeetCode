---
title: "76. 最小覆盖子串"
aliases: ["yiduobo的每日leetcode 76.最小覆盖子串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/sliding-window", "题单/滑动窗口与双指针", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/滑动窗口与双指针/二-不定长滑动窗口", "题单/LeetCode-热题-100/子串", "题单/面试经典-150-题/滑动窗口"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/133527669"
zhihu_id: "133527669"
zhihu_title: "yiduobo的每日leetcode 76.最小覆盖子串"
question_id: "76"
question: "最小覆盖子串"
problem_url: "https://leetcode.cn/problems/minimum-window-substring/"
difficulty: "Hard"
created: "2020-04-19T23:32:11+08:00"
updated: "2020-04-19T23:32:11+08:00"
upvotes: 0
comments: 0
---

# 76. 最小覆盖子串

> **[yiduobo的每日leetcode 76.最小覆盖子串](https://zhuanlan.zhihu.com/p/133527669) · 知乎 · 2020-04-19 · 赞同 0**
> 力扣：[76. 最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/) · Hard · 灵茶山艾府：[两种方法：从 O(52m+n) 到 O(m+n)，附题单（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

76.最小覆盖子串<https://leetcode-cn.com/problems/minimum-window-substring/>

某种升级版的滑动窗口问题。

首先，我们可以统计出对于t中的每个字符，其在s中的位置分布，将其记为pos_dict。pos_dict的key为t中的每个字符，对应的value为一个list，表示key这个字符在s中出现的所有位置。

于是，我们可以很快从pos_dict得到s中最左侧的一个覆盖住t的子串。具体做法为对于t中的每个字符，统计其出现的次数，然后取pos_dict中对应的前几个的位置，计算出最左侧和最右侧的下标位置即可。由于pos_dict中的list都是单调的，因此实际上对于一个字符char，其在t中出现了k次，那么左边界一定是pos_dict[char][0]，而右边界则是pos_dict[char][k - 1]。

例如样例中的s\=ADOBECODEBANC，t\=ABC，首先计算pos_dict：

pos_dict['A'] \= [0, 10]

pos_dict['B'] \= [3, 9]

pos_dict['C'] \= [5, 12]

然后统计出t中的A、B、C分别都出现了1次，那么：

左边界l就是min(pos_dict['A'][0], pos_dict['B'][0], pos_dict['C'][0]) \= 0。

右边界r则是max(pos_dict['A'][1 - 1]， pos_dict['B'][1 - 1], pos_dict['C'][1 - 1]) \= 5。

这样一来，就找到了最左侧的一个可行解，具体为s[l : r + 1] \= ADOBEC。

当然，如果这里出现了k > len(pos_dict[char])的情况，说明s中char字符的数量少于t中char字符的数量，此时直接返回空串即可。

接下来，我们将l往右推动。若当前s\[l\]是t中的字符，那么说明需要将pos_dict\[s\[l\]\]的下一个字符补充进来，用来替代当前的s\[l\]，于是我们可以维护一个now_choose_pos字典，用来表示当前pos_dict中每个字符当前使用到了第几个。

例如上面的ADOBEC：

由于此时的A、B、C都是只是用了第一个，因此now_choose_pos['A'] \= 0, now_choose_pos['B'] \= 0，now_choose_pos['C'] \= 0。

接下来，我们将l往右推动一位，此时s\[l : r + 1\] \= DOBEC，需要补上一位A，此时将now_choose_pos\['A'\]加一，然后取出pos_dict\['A'\]\[now_choose_pos\['A'\]\]加入到候选结果中。当然，新加入的char字符所在的位置pos_dict\[char\]\[now_choose_pos\[char\]\]是可能会超出右边界r的，因此需要及时更新右边界r，样例中为

r \= max(r, pos_dict\['A'\]\[now_choose_pos\['A'\]\]) \= max(5, 10) \= 10

右边界产生了变化，此时的s[l : r + 1] \= DOBECODEBA。

接下来，继续将l往右推动一位，发现是D，不在t中，那么无事发生。同样，再往后的O也一样。此时s[l : r +1] \= BECODEBA。

再往后，s[l] \= 'B'，因此需要将now_choose_pos['B'] +\= 1，同时更新右边界r，即

r \= max(r, pos_dict['B'][now_choose_pos['B']) \= max(10, 9) \= 10

可以发现此时的右边界无需移动，因此此时的s[l : r + 1] \= ECODEBA。

接下来l移动到E，无事发生，此时s[l : r + 1] \= CODEBA。

再往后l移动到C，那么需要将now_choose_pos['C'] +\= 1，同时更新右边界r，即

r \= max(r, pos_dict['C'][now_choose_pos['C']) \= max(10, 12) \= 12

此时右边界往右移动，此时的s[l : r + 1] \= ODEBANC。

接下来，l往右移动到O、D、E均无事发生，此时的s[l : r + 1] \= BANC。

最后，l往右移动到B，发现此时的now_choose_pos['B'] + 1 \=\= len(pos_dict['B'])，说明s中再往后已经没有字符B可以使用了，那么在此处break。对于t中的每个字符char，若当前的now_choose_pos[char] + 1 \=\= len(pos_dict[char])，且当前左边界移除了char，那么s中的char就不够了，都可以直接break掉。

可以发现，上面每次移动之后，得到的s[l : r +1]都是合法的结果，因此只需要在这个过程中记录住最短的一个结果即可。一个小的优化是，当r - l + 1 \=\= len(t)时，说明此时的s[l : r + 1]刚好包含了t中的所有字符，因此此时的s[l : r + 1]一定是最优解，此时可以直接返回。

由于只需要一趟扫描，因此最后的时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def minWindow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        """

        if not s or not t:
            return ''

        pos_dict = {}
        count_dict = {}
        now_choose_pos = {}
        for char in t:
            pos_dict[char] = []
            count_dict[char] = count_dict.get(char, 0) + 1

        for index, char in enumerate(s):
            if char in pos_dict:
                pos_dict[char].append(index)

        l = len(s)
        r = 0
        for char in pos_dict:
            if len(pos_dict[char]) < count_dict[char]:
                return ''
            l = min(l, pos_dict[char][0])
            r = max(r, pos_dict[char][count_dict[char] - 1])
            now_choose_pos[char] = count_dict[char] - 1

        res = [r - l + 1, l, r]

        while l < r:
            if r - l + 1 == len(t):
                return s[l : r + 1]
            char = s[l]
            if char in pos_dict:
                if now_choose_pos[char] == len(pos_dict[char]) - 1:
                    break
                else:
                    now_choose_pos[char] += 1
                    next_pos = pos_dict[char][now_choose_pos[char]]
                    if next_pos > r:
                        r = next_pos
            l += 1
            if r - l + 1 < res[0]:
                res = [r - l + 1, l, r]

        return s[res[1] : res[2] + 1]
```
