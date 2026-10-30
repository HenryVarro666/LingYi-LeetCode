---
title: "1397. 找到所有好字符串"
aliases: ["yiduobo的每日leetcode 1397.找到所有好字符串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/404588999"
zhihu_id: "404588999"
zhihu_title: "yiduobo的每日leetcode 1397.找到所有好字符串"
question_id: "1397"
question: "找到所有好字符串"
problem_url: "https://leetcode.cn/problems/find-all-good-strings/"
created: "2021-08-28T21:30:32+08:00"
updated: "2021-08-28T21:30:32+08:00"
upvotes: 0
comments: 0
---

# 1397. 找到所有好字符串

> **[yiduobo的每日leetcode 1397.找到所有好字符串](https://zhuanlan.zhihu.com/p/404588999) · 知乎 · 2021-08-28 · 赞同 0**
> 力扣：[1397. 找到所有好字符串](https://leetcode.cn/problems/find-all-good-strings/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1397.找到所有好字符串

[力扣](https://leetcode-cn.com/problems/find-all-good-strings/)

如果题目没有evil的限制，那么就可以转化成比较简单的组合数学问题。即对于字符串s1和s2，我们可以分别计算'aa...a'到s1的字符串数目cnt1以及'aa...a'到s2的字符串数目cnt2，但是有了evil之后就麻烦了。一个自然的想法是计算从'aa...a'到s1和s2的字符串中有多少个包含子串evil的字符串数目，但是这就又涉及到容斥原理之类的东西，越搞越复杂了。

另一个思路则是使用动态规划。令f[index][pos][flag]表示前index个字符，其后缀已经匹配到了evil的pos这个位置，flag则表示当前字符与sa和sb的贴近情况。

flag一共有4中选择：

1、当flag为1时，表示当前选择的字符串与sa的前index个字符一样

2、当flag为2时，表示当前选择的字符串与sb的前index个字符一样

3、当flag为3时，表示当前选择的字符串与sa的前index个字符一样，同时与sb的前index个字符也一样

4、当flag为0时，表示当前选择的字符串不受限制

这里维护flag的目的是为了确定下一个字符的合法选择范围。例如sa为abc，sb为ade，那么我们在第一个字符选择了'a'之后，第二个字符就会同时受到sa和sb的限制，因此第二个字符的取值范围就是'b'到'e'。

当我们第二个字符选择'b'时，由于贴近下限sa，因此第三个字符选择的下限就是sa中的字符'c'，而上限则没有限制，即'abc'、'abd'、...、'abz'这些字符串

当我们第二个字符选择'c'时，并没有贴近sa和sb，因此第三个字符选择没有任何限制，这里对应的是'aca'、'acb'、...、'acz'这些字符串。

当我们第二个字符选择'd'时，由于贴近上线sb，因此第三个字符选择的上限就是sb中的字符'e'，而下限则没有限制，即'ada'、'adb'、...、'ade'这些字符

对于状态f[index][pos][flag]：

1、若index等于字符串长度n，那么说明f[index][pos][flag]得出了一种合法的答案，那么将f[index][pos][flag]置为1。

2、若index小于n，那么我们需要选择下一个字符。此时则先通过上面flag使用的规则确定下一个字符的下限和上限，接下来枚举之间的每一个字符char。

此时我们需要确认当前已经选择的字符加入了char之后与evil的匹配情况。这里则可以利用kmp算法，也就是当前选择字符串的后缀与evil前缀匹配的最大长度，也就是通过pos以及evil的next数组来更新选择了char之后的next_pos，若此时的next_pos等于n，说明当前选择的字符串的后缀与evil完全一致，是非法答案，那么当前的char则不能选择。

若char是可以选择的，那么我们通过对比char与sa以及sb中对应的字符以及当前的flag，来确定下一状态的next_flag。

确定好next_pos以及next_flag之后，就有

f[index][pos][flag] +\= f[index + 1][next_pos][next_flag]

具体实现时，我采用的是记忆化搜索的做法，这样比较简洁方便。

最后附上python代码：

```
class Solution(object):
    def findGoodStrings(self, n, s1, s2, evil):
        """
        :type n: int
        :type s1: str
        :type s2: str
        :type evil: str
        :rtype: int
        """

        next = [0]
        pos = 0
        l = len(evil)
        for index in range(1, l):
            while pos > 0 and evil[pos] != evil[index]:
                pos = next[pos - 1]
            if evil[pos] == evil[index]:
                pos += 1
            next.append(pos)
        
        f = [[[None] * 4 for _ in range(l)] for _ in range(n)]
        mod = 10 ** 9 + 7

        return self.dfs(0, 0, 3, evil, next, l, s1, s2, n, f, mod)
    
    def dfs(self, index, pos, flag, evil, next, l, s1, s2, n, f, mod):
        if f[index][pos][flag] is None:
            if index == n:
                f[index][pos][flag] = 1
            else:
                f[index][pos][flag] = 0
                if flag == 1 or flag == 3:
                    bottom = s1[index]
                else:
                    bottom = 'a'
                
                if flag == 2 or flag == 3:
                    top = s2[index]
                else:
                    top = 'z'
                
                for asc in range(ord(bottom), ord(top) + 1):
                    char = chr(asc)
                    next_pos = pos
                    while next_pos > 0 and evil[next_pos] != char:
                        next_pos = next[next_pos - 1]
                    if evil[next_pos] == char:
                        next_pos += 1
                    if next_pos == l:
                        continue
                    
                    if index == n - 1:
                        f[index][pos][flag] += 1
                    else:
                        if flag == 1:
                            if char == s1[index]:
                                next_flag = 1
                            else:
                                next_flag = 0
                        elif flag == 2:
                            if char == s2[index]:
                                next_flag = 2
                            else:
                                next_flag = 0
                        elif flag == 3:
                            if char == s1[index]:
                                if char == s2[index]:
                                    next_flag = 3
                                else:
                                    next_flag = 1
                            elif char == s2[index]:
                                next_flag = 2
                            else:
                                next_flag = 0
                        else:
                            next_flag = 0
                    
                        f[index][pos][flag] += self.dfs(index + 1, next_pos, next_flag, evil, next, l, s1, s2, n, f, mod)
                    
                    f[index][pos][flag] %= mod
        
        return f[index][pos][flag]
```
