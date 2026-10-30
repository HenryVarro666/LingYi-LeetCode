---
title: "3735. 反转后字典序最小的字符串II"
aliases: ["yiduobo的每日leetcode 3735.反转后字典序最小的字符串II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1968778106803295475"
zhihu_id: "1968778106803295475"
zhihu_title: "yiduobo的每日leetcode 3735.反转后字典序最小的字符串II"
question_id: "3735"
question: "反转后字典序最小的字符串II"
problem_url: "https://leetcode.cn/problems/lexicographically-smallest-string-after-reverse-ii/"
created: "2025-11-04T21:22:25+08:00"
updated: "2025-11-04T21:22:25+08:00"
upvotes: 2
comments: 0
---

# 3735. 反转后字典序最小的字符串II

> **[yiduobo的每日leetcode 3735.反转后字典序最小的字符串II](https://zhuanlan.zhihu.com/p/1968778106803295475) · 知乎 · 2025-11-04 · 赞同 2**
> 力扣：[3735. 反转后字典序最小的字符串II](https://leetcode.cn/problems/lexicographically-smallest-string-after-reverse-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3735.反转后字典序最小的字符串II

[3735. 反转后字典序最小的字符串 II - 力扣（LeetCode）](https://leetcode.cn/problems/lexicographically-smallest-string-after-reverse-ii/description/)

题目给出一个由小写英文字母组成的，长度为n的字符串s。其中n的规模可达10^5。

现在要求恰好执行一次操作，选出一个1到n之间的整数k，然后反转s的前k个字符，或者反转s的后k个字符。

问执行一次操作后可以得到的字典序最小的字符串是什么。

比较直观的思路是直接暴力枚举这个k，然后想办法高效检测当前构成的字符串与答案字符串大小关系。

由于涉及到了子串间大小的比较，在这里需要用到后缀数组。而对于反转后的子串，则可以将s反转后拼接在原始的s的后面，这样一来就也可以对比原始s中的子串与反转后的子串的大小关系了。为了防止混淆，通常的做法是在期间添加一个额外字符，例如'!'或者'@'作为分隔。

---

接下来简单介绍一下后缀数组。

对于一个长度为n的字符串，其一共有n个后缀，分别为s[0:], s[1:], ...，s[n - 1:]，而字符串中的所有子串，都必然是其中某个后缀的前缀。基于这一点，只需要各个后缀间最长公共前缀的长度，就可以很方便的比较字符串中的任意两个子串的大小了。

为了计算这个最长公共前缀，首先需要计算三个数组sa、rank以及height。height的定义以及计算方法将在后面提到，在这里先说一说sa和rank。

sa\[index\]表示的是排名为index的后缀其起始位置的下标，而rank\[index\]则表示起始位置为index的后缀的排名。不难发现，这两个数组具有sa\[rank\[index\]\] \= rank\[sa\[index\]\] \= index这个关系，只要知道了其中一个数组，就可以通过一趟遍历推导出另一个数组。

在数据规模较大的情况下，直接对这些后缀字符串进行排序是不优的。在没有辅助条件的情况下，直接通过遍历对比两个字符串的大小，其时间复杂度与字符串的长度有关，换言之，在这里直接使用sort进行排序，时间复杂度高达O(n^2 \* logn)，是不成立的。

接下来介绍一种基于桶排序与倍增思想结合的计算sa以及rank的方法。

对于两个长度为m的字符串s和t，如果能预先直到s和t的前半部分s[:m// 2]与t[:m// 2]的大小关系，以及s和t的后半部分s[m//2:]以及t[m//2:]的大小关系，那么就可以通过这些半部分之间的大小关系，来判断s和t的大小关系。更进一步的，如果按照长度为1->2->4->...的顺序，来计算这些后缀间的大小关系，那么就可以在O(T \* log(n))的时间复杂度内计算出需要的rank数组，这里的T是完成一次排序所需的时间。

值得一提的是，在对比长度为m的两个字符串s和t的大小时，先对比的是s[:m // 2]以及t[:m // 2]，在这里应该对比s[:m // 2]以及t[:m // 2]在长度为m // 2的这一轮排序中的序，而不是原始的字符串。这样一来比较就是两组整数，才能达到优化性能的目的。

接下来需要考虑排序算法的选择。在这里直接选择基于比较的排序的话应该也行，不过性能可能会差一点。注意到长度为1时比较的是单个字符，一共只有26种可能，而在后续每一轮中，需要比较两次上一轮的序数组，而序数组的取值都在1到n之间，因此在这里可以选择桶排序来提高性能。

桶排的具体实现各有不同，我在这里采用的是使用一个数组cnt，记录小于每种序的元素的数目。具体来说，先一趟遍历，对于当前遍历到的序v，先将cnt[v + 1]加上1，这里的cnt[index]表示恰好等于index - 1的元素出现的数目。接下来再一趟遍历，累加cnt数组，此时cnt[index]的含义就变成了所有小于index的元素出现的次数，那么值为index的元素，就应该是cnt[index] + 1了。

需要注意的是，由于可能有相同的元素，因此在这里确定最终每个元素的顺序时，应该按照从后往前的顺序来进行确定，这样做的理由是对于值相同的元素，可以保有其原来的序，这样才能适配先排后半部分，再排前半部分的处理方法，也就是当前半部分相同时，需要依赖之前排过的后半部分的序，反之则直接通过前半部分来确定新的序。因此，在这里枚举的是sa数组，重新得到的也是sa数组。

得到sa数组后，则需要从前往后进行一趟遍历，对于当前位置sa\[index\]，与上一名的位置sa\[index - 1\]，其前半部分和后半部分对应的序是否相同，若相同，说明二者rank并列，否则当前位置的rank需要加上1，根据计算得到的序更新rank\[sa\[index\]\]即可。

这样一来，就得到了完整的处理方案。

首先，将原始字符串s转化成其ascii码对应的数值数组，这些ascii码可以视为长度为1的字符串原始的序，同时初始化sa数组为1到n。接下来，先对其进行一次桶排序，获取sa数组，并计算出对应的rank数组。

接下来，从2k开始向上迭代。对于当前长度为2k，起始位置在index的后缀，其可以参考的序就是上一轮的rank[index]，而后半部分对应的则应该是rank[index + k]。当index + k >\= n时，说明其不具备后半部分，可以将对应的值置为-1，表示空串的序小于任意字符串。

于是可以令a为rank的复制，b为rank向后偏移k位后得到的数组，然后先对b进行桶排序，更新sa数组，再对a进行桶排序，更新sa数组，最后通过sa数组获取新一轮的rank数组。

重复上面的过程，直到2k >\= n，此时就计算出了所有后缀对应的sa和rank。

---

得到了sa和rank后，还需要计算height数组，并通过其预处理出任意两个后缀的最长公共前缀。height数组的定义为，height[index]表示排名为index的后缀，即s[sa[index]:]，与排名为index - 1的后缀，即s[sa[index - 1]:]的，这两个后缀的最长公共前缀长度，另外定义height[0]为0，因为没有排名更小的后缀。

height数组有一个很好的性质，就是height\[rank\[index\]\] >\= height\[rank\[index - 1\]\] - 1，其证明如下：

首先，若height\[rank\[index - 1\]\] \<\= 1，那么这个式子必然成立，因为不等式右侧要么是0，要么是-1，而不等式左侧必然是非负的。

接下来，若height\[rank\[index - 1\]\] > 1，那么就说明s\[sa\[rank\[index - 1\]\]:\]与s\[sa\[rank\[index - 1\] - 1\]:\]的最长公共前缀长度大于等于2，不妨令这个前缀为pT，其中p为单个字符，T为这个最长公共前缀剩下的部分，其长度为height\[rank\[index - 1\]\] - 1，那么s\[sa\[rank\[index - 1\]:\]就可以写成pTX的形式，而s\[sa\[rank\[index - 1\] - 1\]:\]则可以写成pTY的形式。根据二者的排名关系，这里的X必然非空，否则前者的排名应该更小。

根据sa和rank的定义，sa\[rank\[index - 1\]\]就是index - 1，因此s\[sa\[rank\[index - 1\]:\]，也就是s\[index - 1:\]可以写成pTX的形成，那么s\[index:\]就是TX，另外也必然有一个后缀为pTY去掉p之后剩下的TY。

根据排名，s\[sa\[rank\[index\] - 1\]:\]是s\[index:\]的上一位，因此就有s\[sa\[rank\[index\] - 1\]:\] \< s\[index:\] \= TX。另一方面，由于TY \< TX，因此s\[sa\[rank\[index\] - 1:\]夹在两个以T开头的后缀之间，也就是说这个后缀必然也是以T开头的，其与s\[index:\]的最长公共前缀至少为T的长度，也就是height\[rank\[index - 1\]\] - 1，也就是最上面的性质，height\[rank\[index\]\] >\= height\[rank\[index - 1\]\] - 1。

基于这个性质，就可以从下标0开始一趟遍历，在height\[rank\[index - 1\]\] - 1的基础上暴力计算出height\[rank\[index\]\]了。由于最长公共前缀的长度不会超过n，而这个公共前缀的长度都只会在上一轮的基础上减去1，因此向外暴力扩展的次数不会超过n \* 2次，否则就减不回来了，这也保证了暴力计算height数组的时间复杂度为O(n)。

得到height数组后，就可以通过height数组计算任意两个后缀的最长公共前缀了。对于两个后缀s[p:]和s[q:]，不妨设rank[p] \< rank[q]，那么二者的最长公共前缀的长度就是

min(height\[rank\[p\] + 1\]、height\[rank\[p\] + 2\]、...、height\[rank\[q\]\])

理由是对于三个后缀s[x:]、s[y:]和s[z:]，不妨设rank[x] \< rank[y] \< rank[z]，在这里记s[x:]和s[y:]的最长公共前缀长度为a，s[y:]和s[z:]的最长公共前缀长度为b，那么s[x:]和s[z:]的最长公共前缀长度必然小于等于m \= min(a, b)。不妨记s[x:]和s[z:]的最长公共前缀长度为c，那么当c > m时，就说明s[x:]和s[z:]的第m + 1个字符也必然是相同的，而s[y:]夹在中间，说明s[y:]在这个位置上也具有相同的字符，这样一来a和b中较小的那一项，其对应的公共前缀就可以再加上第m + 1个字符就可以得到更长的公共前缀，与最开始的假设产生了矛盾。

基于上面的结论，在这里就可以不断地往这个不等式里面插入后缀，即对于rank\[p\] \< rank\[p + 1\] \< ... \< rank\[q\]，先根据rank\[p\] \< rank\[p + 1\] \< rank\[p + 2\]，得到s\[sa\[rank\[p\]\]:\]和s\[sa\[rank\[p + 2\]\]:\]的最长公共前缀的上界为min(height\[rank\[p\] + 1\], height\[rank\[p\] + 2\])，然后再根据rank\[p\] \< rank\[p + 2\] \< rank\[p + 3\]，得到s\[sa\[rank\[p\]\]:\]与s\[sa\[rank\[p + 3\]\]:\]的最长公共前缀的上界，以此类推。最终，就可以得到s\[p:\]和s\[q:\]的最长公共前缀的上界为length \= min(height\[rank\[p\] + 1\]、height\[rank\[p\] + 2\]、...、height\[rank\[q\]\])了。

以上是最长公共前缀的上界，而下界则比较显然。由于s\[sa\[rank\[p\]\]:\]和s\[sa\[rank\[p + 1\]\]:\]的前length个字符相同，而s\[sa\[rank\[p + 1\]\]:\]与s\[sa\[rank\[p + 2\]\]:\]的前length个字符相同，因此就可以得出s\[sa\[rank\[p\]\]:\]与s\[sa\[rank\[p + 2\]\]:\]的前length个字符相同。接下来依次推导到s\[sa\[rank\[q\]\]:\]，就可以得到s\[p:\]与s\[q:\]的前length个字符相同的结论。

因此，在这里就可以确定s\[p:\]和s\[q:\]的最长公共前缀就是length \= min(height\[rank\[p\] + 1\]、height\[rank\[p\] + 2\]、...、height\[rank\[q\]\])。

可以发现，这是一个静态区间的最小值问题，使用st算法，就可以在O(nlogn)的时间内完成预处理，然后在O(logn)的时间内查询任意两个后缀的最长公共前缀长度了。

---

st算法是非常经典的区间最值问题的算法。在本题中，令f[index][p]表示height数组以index开头，长度为2^p的区间中的最小值，也就是height数组在index到index + 2^p - 1这一段的最小值，那么当p\=0时，显然就有f[index][p] \= height[index]；而对于p > 0的情况，则可以将这个长度为2^p的区间拆分成两个长度为2^(p - 1)的子区间，前者对应的就是f[index][p - 1]，后者对应的则是f[index + 2^(p - 1) - 1][p - 1]，这两者的较小值即为f[index][p]。换言之，在O(1)的时间内就可以得到任意的f[index][p]，而一共有n个下标，区间长度的指数p是logn级别的，因此预处理f数组的时间复杂度为O(nlogn)。

接下来对于一组查询s[x:]和s[y:]，因为查询的是height，所以需要先将x和y转化为rank[x]和rank[y]。接下来，在这里默认x较小方便查询，若x较大，则交换二者。到了这里，问题就变成了计算height[x + 1]到height[y]这一段的最小值，于是令指数p从最大的可能指数m开始向下迭代，找出最大的，满足x + 2^p - 1 \<\= y的p。接下来，这个从x到y的区间，就被拆解成了x到x + 2^p - 1，以及x + 2^p到y这两段。其中前者就是之前预处理的f[x][p]，而对于后者，则可以继续上面的迭代，找到下一个合法的p然后拆解区间。由于每次都会拆解掉至少一半的区间，因此拆解的次数为logn，也就是说单次查询的时间复杂度为O(logn)。

---

写了上面这么大一堆，终于是把准备工作做完了。接下来需要遍历每个k，并计算这种翻转方案下得到的字符串与当前答案记录的字符串谁更优。

由于题目中有反转前缀与反转后缀这两种情况，在这里可以分别进行处理，找出各自的最优解，然后再进行对比取最优的。这样做虽然会考虑一些不可能成为最优解的情况，但是胜在简单直观。

首先是反转前缀。在这种情况下，默认答案就是反转第一个字符，也就是保持原字符串不动，可以先记录res \= 0。接下来从下标1开始向后遍历，对于当前遍历到的index，考察的是反转s[:index + 1]的情况。

以样例2为例，s为abba，那么反转s后拼接到末尾，得到的字符串t为abba!abba，按下标排布

a b b a ! a b b a

0 1 2 3 4 5 6 7 8

此时反转后的s[:index + 1]，对应的就是t[n - 1 - index:]，注意这里的n是t的长度而不是s的长度。方便期间，在这里记n - 1 - index为rev_index。

如果index \= 2，那么原始的s[:index + 1]就是abb，对应到反转后的部分，就是t[6:]，即bba。

对于当前对比的index与res，由于是按照顺序遍历的，因此index必然大于res，而对比的两个字符串就应该是

t[rev_index:] + t[index + 1:]

以及

t[n - 1 - res:] + t[res + 1:]

首先对于前面这两段，即t[rev_index:]以及t[n - 1 - res:]，即这两个后缀的最长公共前缀长度为length，那么length的最大值就是n - 1 - res，即较短的那个后缀的长度。

若length \< res + 1，那么就说明这两个反转后的前缀已经分出胜负了，只需对比这两个后缀中第length + 1个字符的大小，即t[n - 1 - res + length]以及t[rev_index + length]这两个字符的大小就行了。

若length的长度等于res + 1，那么就说明在这一段分不出大小，需要继续对比。

需要注意的是，这里不能直接对比t[index + 1:]以及t[res + 1:]，因为前面的t[rev_index:]在去除掉前length个字符后，还会剩下一部分字符，需要对比的是这些字符与t[res + 1:]。实际上，t[index + 1:]必然是t[res + 1:]的后缀，因为这部分字符是s中没有被反转过的部分，是无需比较的。

不妨记剩下部分的起点为rest_part_index，那么就有rest_part_index \= rev_index + res + 1，需要对比的两个后缀就是t[rest_part_index:]以及t[res + 1:]。同样记这个最长公共前缀长度为length，那么当length够大时，即length >\= n - rest_part_index，那么就说明分不出胜负，无需更新答案；若length \< n - rest_part_index，那么就只需要对比这两个后缀中的第length + 1个字符串的大小，即t[rest_part_index + length]以及t[res + 1 + length]这两个字符的大小就行了。

接下来是反转后缀。对于这种情况，依然是从短到长遍历反转的长度，也就是初始化答案res为n // 2 - 1，然后从n // 2 - 2开始向前遍历，对于当前遍历到的index，考察的是反转s[index:]的情况。

还是样例2，s为abba，按下标排布

a b b a ! a b b a

0 1 2 3 4 5 6 7 8

此时反转后的s[index:]，对应的就是按'!'对称的部分，即t[n // 2 + 1: n - index]。

如果index \= 1，那么原始的s[index:]就是bba，对应到反转后的部分，就是t[5: 8]，即abb。

对于当前对比的index和res，对比的两个字符串分别为

t[:index] + t[n // 2 + 1: n - index]

以及

t[:res] + t[n // 2 + 1: n - res]

可以发现，这里的前半段中t[:index]这一段是无需比较的，因为两个字符串都没有动过这一段。需要注意，这里是从后向前遍历的，所以index必然小于res，t[:index]是较短的那一段。因此，首先需要对比的就是t[n // 2 + 1 : n - index]以及t[index + 1: res]，即计算t[n // 2 + 1:]与t[index + 1:]这两个后缀的最长公共前缀，记为length。需要注意，此时的length可能超长，因为计算的是后缀的最长公共前缀，而不是子串的最长公共前缀。此时就需要对于length与res - index的大小。

若length \< res - index，说明已经分出胜负，此时只需对比t[n // 2 + 1 + length]以及t[index + 1 + length]这两个字符的大小就行了。

若length >\= res - index，则还需要对比后面的部分。对于index而言，t[n // 2 + 1: n - index]被消耗掉了前面长为res - index的部分，因此接下来需要从n // 2 + 1 + res_suffix - index开始进行比较，不妨记为rest_part_index。而对于res，需要对比的就是t[n // 2 + 1: n - res]，因此对比的两个后缀就是t[rest_part_index:]以及t[n // 2 + 1:]，同样记最长公共前缀的长度为length，那么当length够大时，即length大于等于t[n // 2 + 1: n - res]的长度n // 2 - res时，那么就说明分不出胜负，无需更新答案；若length \< n // 2 - res，那么就只需要比较t[rest_part_index + length]与t[n // 2 + 1 + length]的大小就行了。

在得到反转前缀和反转后缀的最优位置后，只需构造这两个字符串，然后取其中较小的那个作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def lexSmallest(self, s):
        """
        :type s: str
        :rtype: str
        """

        n = len(s)
        a = [ord(c) - 96 for c in s]
        a = a + [27] + a[::-1]
        n = len(a)
        sa = range(n)
        ma = 27

        def sort(f, sa):
            cnt = [0] * (ma + 2)
            for index in range(n):
                cnt[f[index] + 1] += 1
            for index in range(1, ma + 2):
                cnt[index] += cnt[index - 1]

            order = [0] * n
            for index in range(n - 1, -1, -1):
                cnt[f[sa[index]] + 1] -= 1
                order[cnt[f[sa[index]] + 1]] = sa[index]

            for index in range(n):
                sa[index] = order[index]

        sort(a, sa)
        b = [0] * n
        rank = [0] * n

        def get_rank():
            ma = 0
            for index in range(n):
                if index > 0:
                    now = sa[index]
                    pre = sa[index - 1]
                    if a[now] != a[pre] or b[now] != b[pre]:
                        ma += 1
                rank[sa[index]] = ma

            return ma
        
        ma = get_rank()

        k = 1
        while k < n:
            b = [rank[index + k] if index + k < n else -1 for index in range(n)]
            sort(b, sa)
            a = rank[:]
            sort(a, sa)
            ma = get_rank()
            k += k

        t = s + "!" + s[::-1]
        height = [0] * n
        length = 0
        for index in range(n):
            if rank[index] == 0:
                continue
            pre = sa[rank[index] - 1]
            while index + length < n and pre + length < n and t[index + length] == t[pre + length]:
                length += 1
            height[rank[index]] = length
            if length > 0:
                length -= 1

        pow2 = [1]
        while pow2[-1] + pow2[-1] <= n:
            pow2.append(pow2[-1] + pow2[-1])
        
        f = [[None] * len(pow2) for _ in range(n)]
        for p in range(len(pow2)):
            for index in range(n):
                if index + pow2[p] - 1 >= n:
                    break
                if p == 0:
                    f[index][p] = height[index]
                else:
                    f[index][p] = min(f[index][p - 1], f[index + pow2[p - 1]][p - 1])

        def get(x, y):
            x = rank[x]
            y = rank[y]
            if x > y:
                x, y = y, x

            x += 1
            max_length = n
            p = len(pow2) - 1
            while x < y:
                while x + pow2[p] - 1 > y and p > 0:
                    p -= 1
                
                max_length = min(max_length, f[x][p])
                x += pow2[p]
            
            return min(max_length, height[y])

        res_preifx = 0
        for index in range(1, n // 2):
            rev_index = n - index - 1

            max_length = get(rev_index, n - res_preifx - 1)

            if max_length == res_preifx + 1:
                rest_part_index = rev_index + res_preifx + 1
                max_length = get(rest_part_index, res_preifx + 1)
                if max_length < n - rest_part_index and t[rest_part_index + max_length] < t[res_preifx + 1 + max_length]:
                    res_preifx = index
            elif t[n - res_preifx - 1 + max_length] > t[rev_index + max_length]:
                res_preifx = index

        res_suffix = n // 2 - 1
        for index in range(n // 2 - 2, -1, -1):
            max_length = get(n // 2 + 1, index)
            if max_length >= res_suffix - index:
                rest_part_index = n // 2 + 1 + res_suffix - index
                max_length = get(rest_part_index, n // 2 + 1)
                if max_length < n // 2 - res_suffix and t[rest_part_index + max_length] < t[n // 2 + 1 + max_length]:
                    res_suffix = index
            elif t[index + max_length] > t[n // 2 + 1 + max_length]:
                res_suffix = index

        return min(s[:res_preifx + 1][::-1] + s[res_preifx + 1:], s[:res_suffix] + s[res_suffix:][::-1])
```
