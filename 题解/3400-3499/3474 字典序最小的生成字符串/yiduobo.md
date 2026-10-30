---
title: "3474. 字典序最小的生成字符串"
aliases: ["yiduobo的每日leetcode 3474.字典序最小的生成字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/string", "leetcode/string-matching", "leetcode/bao-li", "题单/贪心算法", "题单/字符串", "题单/贪心算法/三-字符串贪心", "题单/贪心算法/八-其他", "题单/字符串/二-Z-函数-后缀的前缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1897039786969117945"
zhihu_id: "1897039786969117945"
zhihu_title: "yiduobo的每日leetcode 3474.字典序最小的生成字符串"
question_id: "3474"
question: "字典序最小的生成字符串"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-generated-string/"
difficulty: "Hard"
rating: 2605
created: "2025-04-19T23:46:00+08:00"
updated: "2025-04-19T23:49:40+08:00"
upvotes: 0
comments: 0
---

# 3474. 字典序最小的生成字符串

> **[yiduobo的每日leetcode 3474.字典序最小的生成字符串](https://zhuanlan.zhihu.com/p/1897039786969117945) · 知乎 · 2025-04-19 · 赞同 0**
> 力扣：[3474. 字典序最小的生成字符串](https://leetcode.cn/problems/lexicographically-smallest-generated-string/) · Hard · 灵茶山艾府：[正确性证明 + 暴力修改 / Z 函数优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3474.字典序最小的生成字符串

[3474. 字典序最小的生成字符串 - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-generated-string/description/)

题目给出两个字符串str1和str2，其中str1仅由'T'和'F'组成，其长度n不超过10000，str2则由小写字母构成，其长度m不超过500。

接下来要求生成一个长度为n + m - 1的字符串，对于其中在0到n - 1之间的所有下标index都需要满足：

1、若str1[index]为'T'，那么以index开始的长度为m的子串必须与str2相同，即word[i : i + m] \= str2

2、若str1[index]为'F'，那么以index开始的长度为m的子串必须与str2不同，即word[i: i + m] !\= str2

问可以生成出来的字典序最小的字符串是什么。若无法生成，则返回空串。

首先从题目中两个字符的规模n和m来看，时间复杂度为O(n \* m)的算法应该是可行的，那么基于这一点，就可以先根据str1中所有值为'T'的位置对答案字符串进行填充，因为这些位置可以唯一确定答案字符串的某个子串。需要注意的是，在填充完毕后，需要再次遍历这些位置，确定两个'T'之间不会出现矛盾。

接下来，答案字符串中可能还存在一些没有填充的位置，现在要求填充这些位置，使得答案字符串的字典序最小，同时还需要符合str1中所有值为'F'对应的子串不能与str2相同。在这里需要注意的是，之前经过str1中的'T'填充得到的部分是不应该变动的。

为了使得答案的字典序最小，那么比较自然的想法就是将所有剩下的位置都填上'a'，但是这样一来可能会使得某些位置上不再符合str1中的'F'的要求。以贪心的思路来说，就应该从后往前，将当前子串中最后一个不是通过'T'确定下来的位置的字符修改为字母表中的下一个字符，这样就可以保证修改后得到的字符串的字典序依然最小。

当然，这样修改的话可能有两个问题，第一个是这次修改是否会导致之前某个符合'F'的子串变为不符合'F'，第二个是这个位置上的字符是否一定可以执行修改。

---

我自己尝试了一下，发现似乎构造不出上面这两种情况对应的case，但是想要严谨的证明这种做法的正确性感觉也比较麻烦。一种直观的理解是将str2以及修改前后两个子串left以及right都划分成三段，分别为

str2 \= p1 + c1 + p2 + c2 + p3

left \= p1 + c1 + p2 + c1 + p3

right \= p1 + c1 + p2 + c2 + p3

其中p1、p2、p3为三段子串，c1和c2为两个字符。此时的场景是上面提到的，因为right不符合'F'，需要将其中的c1修改为c2。在这里不妨将两段放一起来看，对应上修改的字符之后形如

```
p1 + c1 + p2 + c1 + p3
          p1 + c1 + p2 + c2 + p3
```

在这里是因为下面子串与str2匹配上了，必须将c1修改为c2，影响到了上面这个子串，变成了

```
p1 + c1 + p2 + c2 + p3
          p1 + c2 + p2 + c2 + p3
```

使得上面子串与str2匹配上了。

这里实际上隐藏了不少信息：

1、以修改前的c1、修改后的c2为界，其左侧的部分是word中相同的一端，因此p1是p1 + c1 + p2的后缀

2、下面子串修改的是c1而不是后面的字符，说明后续字符已经被之前的'T'定死了。更进一步的，p2 + c2 + p3必然是str2的前缀。再进一步，这里p1的长度不能和p2相同，因为p1 + c1和p2 + c2都是str2的前缀，如果p1和p2长度相同，那么c1就和c2相同了，显然是有问题的。

接下来对p1和p2按照长度分情况讨论：

1、若p1的长度较小：

由于p1是p1 + c1 + p2的后缀，那么说明p1就是p2的后缀。在这里不妨设p2 \= p4 + p1，那么重新写这两个字符串，为

```
p1 + c1 + p2 + c1 + p3
          p1 + c1 + p2 + c2 + p3
变为
p1 + c1 + p4 + p1 + c2 + p3
               p1 + c1 + p4 + p1 + c2 + p3
```

另外之前p2 + c2 + p3是str2的前缀这一结论可以改写成p4 + p1 + c2 + p3是str2的前缀，更进一步的，有p4 + p1 + c2是str2的前缀。同时，p1 + c1 + p4也是str2的前缀。这两个前缀的长度相同，但是包含的字符数量却不同，很明显是有问题的。

2、若p1的长度较大：

这里的变化与上面略有不同。

首先p1是str2的前缀，而p2 + c2 + p3也是str2的前缀。若p1的长度大于p2的长度，那么p1必然可以写成p1 \= p2 + c2 + p5

```
          p1 + c1 + p2 + c1 + p3
                    p1 + c1 + p2 + c2 + p3
变为
p2 + c2 + p5 + c1 + p2 + c1 + p3
          p2 + c2 + p5 + c1 + p2 + c2 + p3
```

可以发现，原来的p1展开为p5 + c1 + p2这一段之后，其依然要是p1 + c1 + p2的后缀，那么按照长度对标上去，其需要与p5 + c1 + p2相等。然后这两个子串中包含的字符数量也不同，依然是有问题的。

综合以上的分析可以发现，按照最开始的修改方法是不会出现上面提到的第一个问题，即这次修改是否会导致之前某个符合'F'的子串变为不符合'F'。

---

接下来对于第二个问题，即是否会对某个特定的位置反复修改，最后导致无法修改，也可以使用类似的方法进行证明。分割后的子串为

str2 \= p1 + c2 + p2 + c1 + p3

left \= p1 + c2 + p2 + c1 + p3

right \= p1 + c1 + p2 + c1 + p3

其中p1、p2、p3为三段子串，c1和c2为两个字符。此时的场景是上面提到的，因为left不符合'F'，需要将其中的c1修改为c2，但是这次修改之后，使得right不符合'F'了，而right必须再次修改这个字符。如果后续很多子串都盯着这个字符薅，最后就无法修改了。在这里依然将两段放一起来看，对应上修改的字符之后形如

```
p1 + c2 + p2 + c1 + p3
          p1 + c1 + p2 + c1 + p3
```

在对第一个子串修改后将变为

```
p1 + c2 + p2 + c2 + p3
          p1 + c2 + p2 + c1 + p3
```

这样一来，使得第二个子串又命中了str2，需要再次修改。然后后续的字符无法修改，必须修改为

```
p1 + c2 + p2 + c3 + p3
          p1 + c3 + p2 + c1 + p3
```

可以发现，第二个问题与第一个问题本质实际是一样的，都是p2 + c1 + p3这个后缀被某个'T'定死了，导致不得不修改前面的字符，而这个定死意味着p2 + c1 + p3是str2的前缀，同时p1天然是p1 + c2 + p2的后缀，接下来只需如法炮制，针对p1和p2的长度展开讨论推导出矛盾就行了。

---

在不严谨的证明了上面两种情况都不会出现后，就可以放心使用最开始给出的贪心法来构造最终的字符串了。

与往常的解题逻辑不同，本题是从字典序最小的方向出发，得到一种贪心方案，然后在手动构造不出反例时才反过来强行进行证明，莫名有一种先上实验做完ab涨点了然后后强行凹一个解释上去的既视感。

最后附上python代码：

```python
class Solution(object):
    def generateString(self, str1, str2):
        """
        :type str1: str
        :type str2: str
        :rtype: str
        """
        
        n = len(str1)
        m = len(str2)
        list2 = list(str2)
        res = [None] * (n + m - 1)
        for index, s1 in enumerate(str1):
            if s1 == 'T':
                for offset, s2 in enumerate(str2):
                    res[index + offset] = s2
        
        for index, s1 in enumerate(str1):
            if s1 == 'T' and res[index: index + m] != list2:
                return ""
        
        change_index = set()
        for index in range(n + m - 1):
            if res[index] is None:
                change_index.add(index)
                res[index] = 'a'
        
        for index, s1 in enumerate(str1):
            if s1 == 'F' and res[index: index + m] == list2:
                p = index + m - 1
                while p >= index and p not in change_index:
                    p -= 1
                
                if p >= index:
                    res[p] = chr(ord(res[p]) + 1)
                else:
                    return ''
        
        return ''.join(res)
```
