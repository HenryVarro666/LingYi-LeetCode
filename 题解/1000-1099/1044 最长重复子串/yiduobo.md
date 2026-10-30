---
title: "1044. 最长重复子串"
aliases: ["yiduobo的每日leetcode 1044.最长重复子串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/string", "leetcode/suffix-array", "题单/字符串", "题单/字符串/四-字符串哈希", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/370936689"
zhihu_id: "370936689"
zhihu_title: "yiduobo的每日leetcode 1044.最长重复子串"
question_id: "1044"
question: "最长重复子串"
problem_url: "https://leetcode.cn/problems/longest-duplicate-substring/"
difficulty: "Hard"
rating: 2429
created: "2021-05-09T21:00:51+08:00"
updated: "2021-05-09T21:00:51+08:00"
upvotes: 4
comments: 0
---

# 1044. 最长重复子串

> **[yiduobo的每日leetcode 1044.最长重复子串](https://zhuanlan.zhihu.com/p/370936689) · 知乎 · 2021-05-09 · 赞同 4**
> 力扣：[1044. 最长重复子串](https://leetcode.cn/problems/longest-duplicate-substring/) · Hard · 灵茶山艾府：[O(N) 后缀数组做法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1044.最长重复子串

[力扣](https://leetcode-cn.com/problems/longest-duplicate-substring/)

继上次trie图之后，这里又出现了需要使用高级字符串数据结构的题目。这题可以使用后缀数组或者后缀树来解决，我在这里使用的后缀数组。

对于一个字符串而言，其所有子串都是其某个后缀的前缀，例如样例中的banana，其长度为6，那么一共就有6个后缀，分别为

banana

anana

nana

ana

na

a

而最终答案ana是anana以及ana这两个后缀的最长公共前缀

换言之，本题实际上求得就是字符串所有后缀的最长公共前缀，那么可以使用后缀数组解决。

首先可以明确的是，最长公共前缀必然是出现在按字典序排序之后的两个相邻后缀之间，例如上面的这6个后缀排序后就是

a

ana

anana

banana

na

nana

而答案则出现在ana与相邻的anana之间

回到原始的字符串s中。若后缀s[k:]与其字典序相邻的后缀s[p:]的最长公共前缀长度为l，那么对于后缀s[k + 1:]而言，必然存在某个q，满足s[k + 1:]与s[q:]的最长公共前缀长度大于等于l - 1。证明也很简单，对于s[k:]而言，其可以看做

s[k]单个字符与s[k + 1:]这个后缀拼接而成

那么若存在s[p:]的前l个字符与s[k:]的前l个字符一致，就可以得到

s[p] \= s[k]且s[p + 1:]的前l - 1个字符与s[k + 1:]的前l - 1个字符一致，于是至少存在一个q \= p + 1满足s[k + 1:]与s[q:]的最长公共前缀长度大于等于l - 1。

当然，这里的l - 1只是一个下限，上限则需要通过对比s[k + 1:]与其字典序相邻的后缀s[last:]才能知道，但是此时无需从头开始进行对比，而是可以利用其l - 1，从s[k + 1+ l - 1]以及s[last + l - 1]开始进行对比，从而在O(n)的时间复杂度内求出所有后缀的最长公共前缀。

有了上面的性质，我们现在问题就变成了如何对这些后缀进行排序。常规的排序做法时间复杂度为O(nlogn \* n)，其中n为s的长度，这个时间复杂度显然是不行的。不过注意到这里是字符串后缀之间的排序，那么我们可以采用一种倍增加桶排序的算法，在O(nlogn)的时间复杂度之内完成排序。

对于字符串而言，只有当两个字符的前缀完全一致时，才有必要对比后面的部分，那么我们可以按照前缀长度为1、2、4、8...这样的顺序对比这些后缀。还是上面的例子banana，首先长度为1时，这些后缀的前缀分别为：

banana：b

anana：a

nana：n

ana：a

na：n

a：a

那么此时就是b、a、n、a、n、a这六个字符进行排序，那么这里可以采用桶排序，在O(n)的时间复杂度内将这些字母的顺序排好：

banana：b，顺序为1

anana：a，顺序为0

nana：n，顺序为2

ana：a，顺序为0

na：n，顺序为2

a：a，顺序为0

接下来我们考察长度为2的前缀，分别为

banana：ba

anana：an

nana：na

ana：an

na：na

a：a加上一个空字符

值得注意的是，对于每一个长度为2的前缀而言，后面的这个字符要么是空字符，要么是上一轮排序中已经拍过序的字符，例如ba中的a是anana在第一轮中排序的前缀a，而an中的n是nana在第一轮中排序的前缀n，依次类推。那么在这里，我们就可以利用上一轮排序的结果，那么这一轮待排序的字符串就是如下的情况：

bababa：ba，其中b在第一轮中顺序为1，a顺序为0，那么就是[1, 0]

anana：an，其中a在第一轮中顺序为0，n顺序为2，那么就是[0, 2]

nana：na，其中n在第一轮中顺序为2，a顺序为0，那么就是[2, 0]

ana：an，其中a在第一轮中顺序为0，n顺序为2，那么就是[0, 2]

na：na，其中n在第一轮中顺序为2，a顺序为0，那么就是[2, 0]

a：a加上一个空字符，其中a在第一轮中顺序为0，而按照字典序的定义，若两个字符串前面的字符可以完全匹配，那么较短的字符串较小，因此我们在这里可以将后半部分出现的空字符的顺序规定为-1，那么这里就是[0, -1]

接下来就是对这些二元组进行排序，由于前面的部分更重要，因此需要先排后面的部分再排前面的部分。同样地，也是使用桶排序来进行排序，在执行两次桶排序之后可以得到新的顺序：

bababa：ba，对应[1, 0]，这一轮的顺序为2

anana：an，对应[0, 2]，这一轮的顺序为1

nana：na，对应[2, 0]，这一轮的顺序为3

ana：an，对应[0, 2]，这一轮的顺序为1

na：na，对应[2, 0]，这一轮的顺序为3

a：a加上一个空字符，对应[0, -1]，这一轮的顺序为0

接下里在考虑长度为4的前缀，同样是利用上一轮长度为2的前缀的排序结果：

banana：ba与na，其中ba在上一轮的顺序为2，na在上一轮的顺序为3，那么就是[2, 3]

anana：an与an，其中an在上一轮的顺序为1，那么就是[1, 1]

nana：na与na，其中na在上一轮的顺序为3，那么就是[3, 3]

ana：an与a加上一个空字符，其中an在上一轮的顺序为1，空字符认为是-1，那么就是[1, -1]

na：na与两个空字符，其中na在上一轮的顺序为3，空字符认为是-1，那么就是[3, -1]

a：a加上一个空字符，与两个空字符，其中a加上一个空字符在上一轮的顺序为0，空字符认为是-1，那么就是[0, -1]

依然是两趟桶排序，那么可以得到

banana：对应[2, 3]，这一轮的顺序为3

anana：对应[1, 1]，这一轮的顺序为2

nana：对应[3, 3]，这一轮的顺序为5

ana：对应[1, -1]，这一轮的顺序为1

na：对应[3, -1]，这一轮的顺序为4

a：对应[0, -1]，这一轮的顺序为0

下一轮要考虑的前缀长度为8，超过了n\=6，那么排序到此停止，从而得到最终的排序结果

a

ana

anana

banana

na

nana

接下里，只要使用上面说到的利用最长公共前缀长度l - 1的性质就可以在O(n)的时间复杂度内找到答案。到这里问题就解决了。

在排序实现的过程中，我们一般会使用两个数组sa与rank来辅助进行桶排序，其中sa[index]表示所有后缀中第index小的后缀是s[sa[index]:]，而rank则与sa相反，rank[index]表示的是以s[index:]是所有后缀中第rank[index]小的。

总结一下，这里算法主要有两个比较巧妙的地方。

第一个是利用后缀字符串大小比较的性质，按2的幂次比较各个后缀的前缀，这样一来每一轮都可以利用上一轮的排序结果。同时由于是对上一轮的排序结果重新排序，那么待排序数最大不会超过字符串的长度n，因此可以使用桶排序在O(n)时间复杂度内完成一轮排序。由于排序前缀长度是倍增的，因此最多只会执行log(n)轮，从而在O(nlogn)的时间复杂度内完成了对所有后缀的排序。除此之外，据我所知也存在O(n)时间复杂度为算法，名称为DC3算法，使用的3分法与字符串后缀的某些性质，但是具体细节我就不太了解了。

第二个则是在获取到有序的后缀之后，利用下标相邻的后缀只多出一个首字符这个性质，确保了下一个下标相邻后缀最长公共前缀的长度下限，从而优化了后缀之间对比求解最长公共前缀长度的时间，得以在O(n)的时间复杂度之内求出所有后缀与其排序顺序相邻的后缀之间的最长公共前缀长度，从而得到全局的最长公共前缀的长度。

最后附上python代码，其中sort和getRank的作用分别为桶排序以及桶排序之后获取新的顺序，而while k \< self.n循环中则是倍增的过程，最后的for循环则是利用公共前缀长度下限性质寻找答案的过程：

```python
class Solution(object):
    def longestDupSubstring(self, s):
        """
        :type s: str
        :rtype: str
        """

        self.n = len(s)
        a = [ord(char) - 96 for char in s]

        self.sa = range(self.n)
        self.max_rank = 26
        self.sort(a)
        b = [0] * self.n
        self.rank = [0] * self.n
        self.getRank(a, b)

        k = 1
        while k < self.n:
            b = [self.rank[index + k] if index + k < self.n else -1 for index in range(self.n)]
            self.sort(b)
            a = self.rank[:]
            self.sort(a)
            self.getRank(a, b)
            k += k

        l = 0
        res = 0
        p = None
        for index in range(self.n):
            if self.rank[index] == 0:
                continue
            last_pos = self.sa[self.rank[index] - 1]
            while index + l < self.n and last_pos + l < self.n and s[index + l] == s[last_pos + l]:
                l += 1
            if l > res:
                res = l
                p = index
            
            if l > 0:
                l -= 1

        if res == 0:
            return ""
        
        return s[p:p + res]

    def sort(self, s):
        cnt = [0] * (self.max_rank + 2)
        for index in range(self.n):
            cnt[s[index] + 1] += 1
        for index in range(1, self.max_rank + 2):
            cnt[index] += cnt[index - 1]

        order = [0] * self.n
        for index in range(self.n - 1, -1, -1):
            cnt[s[self.sa[index]] + 1] -= 1
            order[cnt[s[self.sa[index]] + 1]] = self.sa[index]
            
        
        self.sa = order[:]

    def getRank(self, a, b):
        self.max_rank = 0
        for index in range(self.n):
            if index > 0:
                now = self.sa[index]
                last = self.sa[index - 1]
                if a[now] != a[last] or b[now] != b[last]:
                    self.max_rank += 1
            self.rank[self.sa[index]] = self.max_rank
```
