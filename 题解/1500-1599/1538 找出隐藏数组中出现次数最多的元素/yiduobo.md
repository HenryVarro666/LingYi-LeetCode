---
title: "1538. 找出隐藏数组中出现次数最多的元素"
aliases: ["yiduobo的每日leetcode 1538.找出隐藏数组中出现次数最多的元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/617520069"
zhihu_id: "617520069"
zhihu_title: "yiduobo的每日leetcode 1538.找出隐藏数组中出现次数最多的元素"
question_id: "1538"
question: "找出隐藏数组中出现次数最多的元素"
problem_url: "https://leetcode.cn/problems/guess-the-majority-in-a-hidden-array/"
created: "2023-03-28T02:13:52+08:00"
updated: "2023-03-28T02:13:52+08:00"
upvotes: 0
comments: 0
---

# 1538. 找出隐藏数组中出现次数最多的元素

> **[yiduobo的每日leetcode 1538.找出隐藏数组中出现次数最多的元素](https://zhuanlan.zhihu.com/p/617520069) · 知乎 · 2023-03-28 · 赞同 0**
> 力扣：[1538. 找出隐藏数组中出现次数最多的元素](https://leetcode.cn/problems/guess-the-majority-in-a-hidden-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1538.找出隐藏数组中出现次数最多的元素

[力扣](https://leetcode.cn/problems/guess-the-majority-in-a-hidden-array/)

题目中每次需要使用四个不同的数，那么只有在这四个数中至少有两个数的01组合已经确定的前提下，才能确定剩下未知数的01组合。

根据题目给出的数据规模，在这里就需要先通过前五个数的查询组合来确定前五个数中0和1的多寡情况，同时确定这五个数中较多的哪一种数的其中两个的下标p1和p2，接下来就可以从第六个数开始两个一组，配合p1和p2确定这两个数的01分布了。另外，还需要两个变量cnt1和cnt2记录当前较多那种数以及较少那种数的数量。

由于题目中无法确定每个数具体是0还是1，为了方便起见，在这里不妨称前五个数中较多的那一种为a，较少的那一种为b，接下来对前五个数的组合进行一些分类。

首先令**v1 \= query(0, 1, 2, 3)**。v1的取值可能是4、2、0，也就是代表着前四个数中有4、3、2个a，对这三种情况分别进行讨论：

1）v1 \= 4：

此时说明前4个数全都是4，但无法确定第5个数是什么。此时需要进行第二次询问，也就是**v2 \= query(0, 1, 2, 4)**。若v2 \= 4，说明第5个数也是a，此时应该记cnt1为5，cnt2为0；否则第5个数为b，此时应该记cnt1为4，cnt2为1

对于这两种情况，都应该置p1为0，p2为1

2）v1 \= 2：

这种情况下前4个数一共有4种分布情况，分别为

aaab，此时前5个数可能是aaaba或aaabb

aaba，此时前5个数可能是aabaa或aabab

abaa，此时前5个数可能是abaaa或abaab

baaa，此时前5个数可能是baaaa或baaab

接下来，根据v2进行分类。

2-1）v2 \= 4：

此时只能唯一对应到aaaba这种情况，此时应该置cnt1 \= 4，cnt2 \= 1，p1 \= 0，p2 \= 1

2-2）v2 \= 2：

此时可以对应到aaabb、aabaa、abaaa、baaaa

对于这四种情况，实际上只需要想办法区分出最后两位到底是a还是b，因为对于后面三种情况，都可以置cnt1 \= 4，cnt2 \= 1，p1 \= 3，p2 \= 4，无需区分前三个数的具体分布。

于是在这里只需要设置查询**v3 \= query(0, 1, 3, 4)**，接下来对于v3：

2-2-1）v3 \= 0：

此时的分布必然是aaabb，此时应该置cnt1 \= 3，cnt2 \= 2，p1 \= 0，p2 \= 1

2-2-2）v3 !\= 0：

此时就应该按上面所说的后三种情况的方法初始化cnt1、cnt2、p1和p2

2-3）v2 \= 0：

此时可以对应到aabab、abaab、baaab

对于这三种情况，都有cnt1 \= 3，cnt2 \= 2，需要弄清楚的就是p1和p2应该如何选择。更进一步的，只需要定位到前三个数中b的位置，就可以指定另外两个位置为p1和p2。

2-3-1）v3 \= 2：

说明0、1、3、4这些位置中有3a1b，且3和4包含了1a1b，因此0和1必然都是a，于是可以置p1 \= 0，p2 \= 1

反之，若v3 \= 0，则无法区分是abaab还是baaab，此时需要将2、3、4这三个位置都纳入到询问中，于是可以设置**v4 \= query(0, 2, 3, 4)**。

2-3-2）v3 \= 0且v4 \= 2：

说明0和2都是a，应该置p1 \= 0，p2 \= 2

2-3-3）v3 \= 0且v4 \= 0：

说明1和2都是a，应该置p1 \= 1，p2 \= 2

3）v1 \= 0：

这种情况下前4个数一共有6种分布情况，分别为

aabb

abab

abba

baab

baba

bbaa

无论是哪种情况，前5个数中最后一个都必然是a，因此cnt分布只能是cnt1 \= 3，cnt2 \= 2，此时需要先办法区分的是p1和p2的分布

此时可以先通过v2进行分类。

3-1）v2 \= 2：

此时可能是aabba、ababa、baaba，与上面的2-3类似，此时也需要通过v3和v4来确定b的位置，然后确定p1和p2的值。具体来说，就是

3-1-1）v3 \= 2：

有p1 \= 0，p2 \= 1

3-1-2）v3 \= 0且v4 \= 2：

有p1 \= 0，p2 \= 2

3-1-3）v3 \= 0且v4 \= 0：

有p1 \= 1，p2 \= 2

3-2）v2 \= 0：

此时可能是abbaa、babaa、bbaaa。

无论是哪种情况，都可以直接选择p1 \= 3，p2 \= 4

---

到了这里，就确定了前五个数中值为a的两个位置p1和p2，以及a的数量cnt1以及b的数量cnt2。接下来，只需要从下标6开始向后，两个数一组，配合p1以及p2，就可以确定这两个数是2a、1a1b、2b中的哪一种，分别对应到query的结果为4、2、0，同时更新cnt1和cnt2。

需要特别注意的是，这种处理方法在n为偶数时将会遗留下最后这个数，那么此时就需要确定除了p1和p2之外的第三个数other，与最后这个数组合起来进行最后一次查询并更新cnt。

对于这个other的选择，如果在从下标6开始向后的遍历过程中出现了0，那么自然就可以选择其中一个位置作为other，另一方面，如果这个过程中从未出现过0，那么最终的cnt1和cnt2只有在初始cnt1 \= 3，cnt2 \= 2时才可能出现最终cnt1 \= cnt2的情况，其他情况下必然有cnt1 > cnt2，也就是答案为p1。

而对于所有cnt1 \= 3，cnt2 \= 2的情况，可能对应到上面的

2-2-1：other \= 3

2-3-1：other \= 2

2-3-2：other \= 1

2-3-3：other \= 0

3-1-1：other \= 2

3-1-2：other \= 1

3-1-3：other \= 3

3-2：此时比较特殊，需要额外检测v3。当v3 \= 0时，说明此时的分布为bbaaa，此时应该置other \= 0，否则说明此时属于abbaa或babaa中的一种，无论是哪种总是有other \= 2为b。

得到other后，就可以联合p1、p2、other以及数组中最后落单的数确定这个数是a还是b，从而完成cnt1和cnt2最后的更新并确定最终答案。

最后附上python代码：

```python
# """
# This is the ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
#class ArrayReader(object):
#	 # Compares 4 different elements in the array
#	 # return 4 if the values of the 4 elements are the same (0 or 1).
#	 # return 2 if three elements have a value equal to 0 and one element has value equal to 1 or vice versa.
#	 # return 0 : if two element have a value equal to 0 and two elements have a value equal to 1.
#    def query(self, a, b, c, d):
#        """
#        :type a, b, c, d: int
#        :rtype int
#        """
#
#	 # Returns the length of the array
#    def length(self):
#        """
#        :rtype int
#     

class Solution(object):
    def guessMajority(self, reader):
        """
        :type reader: ArrayReader
        :rtype: integer
        """

        n = reader.length()

        v1 = reader.query(0, 1, 2, 3)
        v2 = reader.query(0, 1, 2, 4)
        v3 = reader.query(0, 1, 3, 4)
        v4 = reader.query(0, 2, 3, 4)

        other = None
        if v1 == 4:
            #1)
            p1 = 0
            p2 = 1
            if v2 == 4:
                #1-1)
                cnt1 = 5
                cnt2 = 0
            else:
                #1-2)
                cnt1 = 4
                cnt2 = 1
        
        elif v1 == 2:
            #2)
            if v2 == 4:
                #2-1)
                p1 = 0
                p2 = 1
                cnt1 = 4
                cnt2 = 1
            elif v2 == 2:
                #2-2)
                if v3 == 0:
                    #2-2-1)
                    p1 = 0
                    p2 = 1
                    other = 4
                    cnt1 = 3
                    cnt2 = 2
                else:
                    #2-2-2)
                    p1 = 3
                    p2 = 4
                    cnt1 = 4
                    cnt2 = 1
            elif v2 == 0:
                #2-3)
                cnt1 = 3
                cnt2 = 2
                if v3 == 2:
                    #2-3-1)
                    p1 = 0
                    p2 = 1
                    other = 2
                elif v4 == 2:
                    #2-3-2)
                    p1 = 0
                    p2 = 2
                    other = 1
                else:
                    #2-3-3)
                    p1 = 1
                    p2 = 2
                    other = 0

        elif v1 == 0:
            #3)
            if v2 == 2:
                #3-1)
                cnt1 = 3
                cnt2 = 2
                if v3 == 2:
                    #3-1-1)
                    p1 = 0
                    p2 = 1
                    other = 2
                elif v4 == 2:
                    #3-1-2)
                    p1 = 0
                    p2 = 2
                    other = 1
                else:
                    #3-1-3)
                    p1 = 1
                    p2 = 2
                    other = 0
            elif v2 == 0:
                #3-2)
                p1 = 3
                p2 = 4
                cnt1 = 3
                cnt2 = 2
                if v3 == 0:
                    other = 0
                else:
                    other = 2

        i = 5
        while i + 1 < n:
            v = reader.query(p1, p2, i, i + 1)
            if v == 4:
                cnt1 += 2
            elif v == 2:
                cnt1 += 1
                cnt2 += 1
            else:
                cnt2 += 2
                other = i
            i += 2

        if other is None:
            return p1

        if i < n:
            if other < p1:
                v = reader.query(other, p1, p2, i)
            elif p1 < other < p2:
                v = reader.query(p1, other, p2, i)
            else:
                v = reader.query(p1, p2, other, i)

            if v == 2:
                cnt1 += 1
            else:
                cnt2 += 1
        
        if cnt1 > cnt2:
            return p1
        elif cnt1 == cnt2:
            return -1
        else:
            return other
```
