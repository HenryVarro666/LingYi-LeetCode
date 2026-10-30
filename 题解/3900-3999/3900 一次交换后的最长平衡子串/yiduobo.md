---
title: "3900. 一次交换后的最长平衡子串"
aliases: ["yiduobo的每日leetcode 3900.一次交换后的最长平衡子串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2028244636565533744"
zhihu_id: "2028244636565533744"
zhihu_title: "yiduobo的每日leetcode 3900.一次交换后的最长平衡子串"
question_id: "3900"
question: "一次交换后的最长平衡子串"
problem_url: "https://leetcode.cn/problems/longest-balanced-substring-after-one-swap/"
difficulty: "Medium"
rating: 2135
created: "2026-04-16T23:10:06+08:00"
updated: "2026-04-16T23:10:09+08:00"
upvotes: 1
comments: 0
---

# 3900. 一次交换后的最长平衡子串

> **[yiduobo的每日leetcode 3900.一次交换后的最长平衡子串](https://zhuanlan.zhihu.com/p/2028244636565533744) · 知乎 · 2026-04-16 · 赞同 1**
> 力扣：[3900. 一次交换后的最长平衡子串](https://leetcode.cn/problems/longest-balanced-substring-after-one-swap/) · Medium · 灵茶山艾府：[前缀和 + 记录前两次出现位置（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3900.一次交换后的最长平衡子串

<https://leetcode.cn/problems/longest-balanced-substring-after-one-swap/description/>

题目给出一个仅由'0'和'1'组成的二进制字符串s。

若一个字符串中0和1的数量相等，那么就称这个字符串为平衡字符串。

现在可以执行至多一次操作，交换s中的任意两个字符，问在至多执行一次操作的前提下，可以得到的最长平衡子串的长度是多少。

如果不考虑执行操作的话，本题就变成了找出最长的，包含相同数量的0和1的子串。这个问题之前遇到过，但是忘记题号了，而处理方法则是先转化为区间和问题，再利用前缀和求解。具体来说，将子串中的0视为-1,而1则视为1，那么问题就变成了找出一个最长的和为0的子区间。更进一步的，这个和为0的子区间问题，则可以转化为相等前缀和相减的问题。

具体来说，只需一趟遍历，计算前缀和pre_s。对于当前位置index，不妨设当前的pre_s首次出现的下标为first[pre_s]，那么从first[pre_s] + 1到index这一段的区间和就必然为0，也就是说可以使用first[pre_s] + 1到index这一段的长度，即index - first[pre_s]来更新答案。接下来，若当前的pre_s在first中没有出现过，则将first[pre_s]置为index，然后继续向后遍历即可。

回到本题。如果选择不执行操作，那么最优解就可以通过上面的方法得到，而对于执行操作的情况，这只需做一些小小的变换就行了。具体来说，如果需要执行操作，必然是将子区间外部的某个0与区间内部的某个1进行交换，或者将子区间外部的某个1与区间内部的某个0进行交换，交换结束后，区间内部的0和1的数量相等。反过来推一步，就能知道前一种情况中，子区间内部0的数量比1多两个，而后一种情况，子区间内部1的数量比0多两个。再转化为区间和，前一种情况的区间和就是-2，而后一种情况的区间和就是2。

同样是区间和问题，依然可以利用前缀和求解，不过在这里需要寻找的是first[pre_s + 2]以及first[pre_s - 2]，这样一来子区间的区间和就是-2或者2了。不过需要特别注意的是，由于需要执行操作，那么必须保证区间外部还存在落单的1或者0，这样一来才能与区间内部多出的0或者1进行交换。在这里可以先遍历s，统计其中0和1的数量，接下来通过子区间的长度，计算出当前状态下区间内0和1的数量，就可以判断出区间外部是否还有可用的1或者0了。若存在，则可以使用index - first[pre_s + 2]或者index - first[pre_s - 2]更新答案。若不存在，则只能退而求其次，选择pre_s + 2或者pre_s - 2第二次出现的位置，对接下来的位置到index形成的子区间执行操作。因此，在first的基础上，还需要额外维护一个哈希表second，记录每种前缀和第二次出现的下标位置。

最后附上python代码：

```python
class Solution(object):
    def longestBalanced(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        zero, one = 0, 0
        for c in s:
            if c == '0':
                zero += 1
            else:
                one += 1
        
        first = {0: -1}
        second = {}
        pre_s = 0
        res = 0
        for index, c in enumerate(s):
            if c == '0':
                pre_s -= 1
            else:
                pre_s += 1
            
            if pre_s in first:
                res = max(res, index - first[pre_s])
            
            if pre_s - 2 in first and (index - first[pre_s - 2] - 2) // 2 < zero:
                res = max(res, index - first[pre_s - 2])
            if pre_s - 2 in second:
                res = max(res, index - second[pre_s - 2])
            
            if pre_s + 2 in first and (index - first[pre_s + 2] - 2) // 2 < one:
                res = max(res, index - first[pre_s + 2])
            if pre_s + 2 in second:
                res = max(res, index - second[pre_s + 2])
            
            if pre_s not in first:
                first[pre_s] = index
            elif pre_s not in second:
                second[pre_s] = index
        
        return res
```
