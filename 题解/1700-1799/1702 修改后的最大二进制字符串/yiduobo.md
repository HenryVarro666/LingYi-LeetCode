---
title: "1702. 修改后的最大二进制字符串"
aliases: ["yiduobo的每日leetcode 1702.修改后的最大二进制字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/448281507"
zhihu_id: "448281507"
zhihu_title: "yiduobo的每日leetcode 1702.修改后的最大二进制字符串"
question_id: "1702"
question: "修改后的最大二进制字符串"
problem_url: "https://leetcode.cn/problems/maximum-binary-string-after-change/"
difficulty: "Medium"
rating: 1825
created: "2021-12-21T23:07:07+08:00"
updated: "2021-12-21T23:07:07+08:00"
upvotes: 0
comments: 0
---

# 1702. 修改后的最大二进制字符串

> **[yiduobo的每日leetcode 1702.修改后的最大二进制字符串](https://zhuanlan.zhihu.com/p/448281507) · 知乎 · 2021-12-21 · 赞同 0**
> 力扣：[1702. 修改后的最大二进制字符串](https://leetcode.cn/problems/maximum-binary-string-after-change/) · Medium · 灵茶山艾府：[贪心，简洁写法（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1702.修改后的最大二进制字符串

[力扣](https://leetcode-cn.com/problems/maximum-binary-string-after-change/)

首先可以考察两种特殊情况：

1、全都是1。此时原封不动输出就好了

2、字符串的形式为11...11100...000。即在0第一次出现的位置后面没有再出现过1。此时高位上的1显然是不应该去动的，因此只需考虑如何操作后面的00...000。

对于00...000这种由连续的0构成的字符串，根据00 -> 10这个规则，可以从高位开始两位两位操作，每操作一次就相当于将最高位变成了1，那么最后一定会变成11...1110这种形式。

因此对于11...11100...000这种字符串，最终答案就是11...1110，字符串的总位数是没有变化的

3、接下来考虑01XXXX这种情况。

为了替换掉最高位上的0，需要用到00 -> 10这个规则，那么就需要将第二位上的1给替换成0。

如果此时字符串是010XXX这种形式的，那么就可以将其变成001XXX这种形式，最后再将其变成101XXX的形式

如果此时字符串是011XXX这种形式的，此时的目标就变成了将第三位上的1给替换成0，那么此时需要继续向后寻找，直到找到第一个0。

更一般的，对于011...10这种形式的字符串，需要从低位开始两位两位执行10 -> 01的操作，最后将会得到0011...111。可以发现，实际上就相当于是将连续1后面的那个0移动到了高位。

根据这个结论，就可以就将第一个0后面的字符串按这个方法进行操作，最终将会得到00...00011...111这种形式的字符串，其中1的个数就是第一个0后面1出现的次数。接下来再将这个字符串高位上的连续0按照情况2的做法转化为11...1110，那么最终这个字符串就会变成11...111011...111

于是可以一趟扫描，统计第一个0后面1出现的次数，记为cnt。设原始字符串的长度为n，那么就有：

1、若cnt \= 0，且字符串中没有0，那么对应的是情况1，此时直接原封不动返回

2、若cnt \= 0，且字符串中有0，那么对应的是情况2，此时应该返回11...1110，这里一共有n - 1个1

3、若cnt > 0，那么对应的是情况3，此时应该返回11...111011...111，这里后缀中一个有cnt个1，那么前缀中1的数目就是n - 1 - cnt

最后附上python代码：

```python
class Solution(object):
    def maximumBinaryString(self, binary):
        """
        :type binary: str
        :rtype: str
        """

        cnt = 0
        flag = False
        for char in binary:
            if char == '0':
                flag = True
            elif flag:
                cnt += 1
        
        n = len(binary)

        if cnt == 0:
            if flag:
                return '1' * (n - 1) + '0'
            else:
                return binary
        else:
            return '1' * (n - cnt - 1) + '0' + '1' * cnt
```
