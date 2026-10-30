---
title: "3614. 用特殊操作处理字符串II"
aliases: ["yiduobo的每日leetcode 3614.用特殊操作处理字符串II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/链表-二叉树与回溯", "题单/贪心算法", "题单/链表-二叉树与回溯/五-其他递归/分治", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1943467680335111446"
zhihu_id: "1943467680335111446"
zhihu_title: "yiduobo的每日leetcode 3614.用特殊操作处理字符串II"
question_id: "3614"
question: "用特殊操作处理字符串 II"
problem_url: "https://leetcode.cn/problems/process-string-with-special-operations-ii/"
difficulty: "Hard"
created: "2025-08-26T00:41:28+08:00"
updated: "2025-08-26T00:41:28+08:00"
upvotes: 1
comments: 0
---

# 3614. 用特殊操作处理字符串II

> **[yiduobo的每日leetcode 3614.用特殊操作处理字符串II](https://zhuanlan.zhihu.com/p/1943467680335111446) · 知乎 · 2025-08-26 · 赞同 1**
> 力扣：[3614. 用特殊操作处理字符串 II](https://leetcode.cn/problems/process-string-with-special-operations-ii/) · Hard · 灵茶山艾府：[逆向思维（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3614.用特殊操作处理字符串II

[3614. 用特殊操作处理字符串 II - 力扣（LeetCode）](https://leetcode.cn/problems/process-string-with-special-operations-ii/description/)

题目给出一个字符串s，由小写英文字母和特殊字符'\*'、'\#'以及'%'组成，其长度可达10^5。

现在要求按一下规则从左到右处理s中的字符，构造一个新的字符串result：

1、若当前字符是小写英文字母，则将其添加到result中

2、若当前字符是'\*'，则需要删除result中的最后一个字符(若存在)

3、若当前字符是'\#'，则复制当前的result，并追加到其自身后面

4、若当前字符是'%'，则反转当前的result

现在给出一个k，k的规模可达10^15，要求返回result中的第k个字符是什么，若k超出了result的下标索引返回，则返回'.'。题目保证最终result的长度不超过10^15。

之前3612题的加强版，由于本题的数据规模较大，直接暴力模拟显然是不行的，不过如果不完整模拟出整个字符，而是计算其最终的长度，则只需对s进行一趟遍历，因此在一开始可以先计算result的长度。计算方法也很简单，就是根据当前遍历到的字符决定长度应该如何变化。记当前长度为length，那么：

1、若遇到了'\*'，且length大于0，则将length减去1

2、若遇到了'\#'，则将length乘以2

3、若遇到了'%'，length不变

4、若遇到了小写字母，则将length加上1

得到length后，可以先检测k是否超出了下标索引，即k大于等于length时，直接返回'.'。若k合法，则可以想办法倒推，具体来说，就是先通过s的最后一个字符，推测出最终result中的第k个字符，在倒数第二步完成时是result中的第几个字符，然后再通过s的倒数第二个字符，推测出该字符应该是倒数第三步完成时result中的第几个字符，以此类推，直到当前的k刚好是result的最后一个字符，且当前s中对应的字符为小写字母为止，即当前添加的这个字符就是最终result中的第k个字符，也就是最终答案。具体倒推的规则如下：

1、若遇到了'\*'，说明result刚进行过一次删除操作，此时应该将length加上1。值得一提的是，在这里是不需要考虑result为空时执行的删除操作的，因为对于这种情况，可以将s到这一步为止的前缀全部去除掉，并不会影响到最终result的生成，换言之，其中的第k个字符与前缀中的操作无关，在执行到这一步操作之前就已经可以找出最终答案了。

2、若遇到了'\#'，说明在上一轮中result被复制了一份，那么当k在result的前半段，也就是k在0到length // 2 - 1之间时，可以直接剔除掉后面这复制出来的一份，此时就可以将length除以2；反之，说明当前字符串中的第k个字符是从上一轮的第k - length // 2个字符处复制得来的，那么问题就可以转换为求上一轮字符串中的第k - length // 2个字符是什么，此时就可以将k减去length // 2，然后将length除以2。

3、若遇到了'%'，说明在上一轮中result被反转了，因此当前字符串的第k个字符，应该是上一轮字符串中的第length - k - 1个字符，此时将k更新为length - k - 1即可。

4、若遇到了小写字符，那么就可以先检测k是否刚好等于length - 1，若等于，那么当前字符即为最终答案，否则说明上一轮操作中往当前字符串中添加了最后一个字符，但是这个字符并不是要求的第k个字符，因此可以将其从中删去还原到上一轮的字符串，此时应该将length减去1。

按照上面描述的算法，就可以在正反两趟遍历间找出最终答案了，时间复杂度为O(n)。

最后附上python代码：

```python
class Solution(object):
    def processStr(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: str
        """
        
        length = 0
        for c in s:
            if c == '*':
                if length > 0:
                    length -= 1
            elif c == '#':
                length += length
            elif c == '%':
                continue
            else:
                length += 1
        
        if k >= length:
            return '.'
        
        for c in s[::-1]:
            if c == '*':
                length += 1
            elif c == '#':
                if k >= length // 2:
                    k -= length // 2
                length //= 2
            elif c == '%':
                k = length - k - 1
            elif k == length - 1:
                return c
            else:
                length -= 1
```
