---
title: "2746. 字符串连接删减字母"
aliases: ["yiduobo的每日leetcode 2746.字符串连接删减字母"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/653847994"
zhihu_id: "653847994"
zhihu_title: "yiduobo的每日leetcode 2746.字符串连接删减字母"
question_id: "2746"
question: "字符串连接删减字母"
problem_url: "https://leetcode.cn/problems/decremental-string-concatenation/"
created: "2023-09-02T03:59:26+08:00"
updated: "2023-09-02T03:59:26+08:00"
upvotes: 0
comments: 0
---

# 2746. 字符串连接删减字母

> **[yiduobo的每日leetcode 2746.字符串连接删减字母](https://zhuanlan.zhihu.com/p/653847994) · 知乎 · 2023-09-02 · 赞同 0**
> 力扣：[2746. 字符串连接删减字母](https://leetcode.cn/problems/decremental-string-concatenation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2746.字符串连接删减字母

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/decremental-string-concatenation/)

注意到字符串在连接时只有首尾两字符会影响最终连接的长度，因此可以使用状态压缩动态规划来求解。

令f[i][state]表示前i个字符串连接后，得到的字符串首尾字符编码为state时的最短长度，这里的编码规则为首字符在字符中的大小顺序与尾字符在字符中的大小顺序构成的两位26进制数，也就是说每一轮最多只有26^2 \= 676中可行的组合。

那么对于f[i][state]，首先考虑边界情况。对于words[0]，其首尾字符在字符中的大小顺序分别为ord(words[0][0]) - 97以及ord(word[0][1]) - 97，其中ord是计算字符的ascii码，而小写a的ascii码是97。得到两个大小顺序后，前者乘以26再加上后者就是words[0]首尾字符对应的编码state，那么就有f[0][state] \= len(words[0])

接下来考虑i >\= 1的情况。对于当前遍历到的words[i]，枚举上一轮的可行状态f[i - 1][pre_state]，那么在这里就有两种处理方法，即将words[i]拼在左侧或者右侧。

为了方便计算，在这里不妨先将pre_state对应的首尾字符拆解出来，得到pre_left和pre_right，同时将words[i]的首位字符对应的大小顺序记为left和right。

当words[i]拼在左侧时，若right恰好等于pre_left，那么这次拼接就可以省略一个字符，记left_delta \= -1，表示这样拼接可以省去一个字符，否则记left_delta \= 0。另一方面，此时新的状态state \= left \* 26 + pre_right，于是就有f[i][state] \= min(f[i][state], f[i - 1][pre_state] + len(words[i]) + left_delta)。

同样的，当words[i]右侧时，可以通过left是否等于pre_right计算出right_delta，以及新的状态state \= pre_left \* 26 + right，然后就有f[i][state] \= min(f[i][state], f[i - 1][pre_state] + len(words[i]) + right_delta)。

全部计算完成后，f[-1]中的最小值即为最终答案。

另外，注意到f的每一轮只与上一轮有关，因此可以通过滚动数组省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def minimizeConcatenatedLength(self, words):
        """
        :type words: List[str]
        :rtype: int
        """

        f = [None] * 676
        left = ord(words[0][0]) - 97
        right = ord(words[0][-1]) - 97
        f[left * 26 + right] = len(words[0])
        for w in words[1:]:
            g = f[:]
            f = [None] * 676
            left = ord(w[0]) - 97
            right = ord(w[-1]) - 97
            for pre_state in range(676):
                if g[pre_state] is None:
                    continue

                pre_left = pre_state / 26
                pre_right = pre_state % 26

                left_delta = right_delta = 0
                if right == pre_left:
                    left_delta = -1
                if left == pre_right:
                    right_delta = -1
                
                left_state = left * 26 + pre_right
                right_state = pre_left * 26 + right
                if f[left_state] is None or f[left_state] > g[pre_state] + len(w) + left_delta:
                    f[left_state] = g[pre_state] + len(w) + left_delta
                if f[right_state] is None or f[right_state] > g[pre_state] + len(w) + right_delta:
                    f[right_state] = g[pre_state] + len(w) + right_delta
                
        

        res = None
        for state in range(676):
            if f[state] is not None and (res is None or res > f[state]):
                res = f[state]
        
        return res
```
