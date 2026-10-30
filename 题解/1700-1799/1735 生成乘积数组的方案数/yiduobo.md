---
title: "1735. 生成乘积数组的方案数"
aliases: ["yiduobo的每日leetcode 1735.生成乘积数组的方案数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/graph", "leetcode/math", "leetcode/combinatorics", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/452873960"
zhihu_id: "452873960"
zhihu_title: "yiduobo的每日leetcode 1735.生成乘积数组的方案数"
question_id: "1735"
question: "生成乘积数组的方案数"
problem_url: "https://leetcode.cn/problems/count-ways-to-make-array-with-product/"
difficulty: "Hard"
rating: 2500
created: "2022-01-03T18:48:17+08:00"
updated: "2022-01-03T18:48:17+08:00"
upvotes: 1
comments: 0
---

# 1735. 生成乘积数组的方案数

> **[yiduobo的每日leetcode 1735.生成乘积数组的方案数](https://zhuanlan.zhihu.com/p/452873960) · 知乎 · 2022-01-03 · 赞同 1**
> 力扣：[1735. 生成乘积数组的方案数](https://leetcode.cn/problems/count-ways-to-make-array-with-product/) · Hard · 灵茶山艾府：[【图解】质因数分解+放球问题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1735.生成乘积数组的方案数

[力扣](https://leetcode-cn.com/problems/count-ways-to-make-array-with-product/)

这类通过若干个数的乘积得到某个数的问题，常规的做法就是分解质因数，相当于从乘积的本源上来解决问题。

对于本题中的一组(n, k)，首先将k分解质因数，得到k \= (p[0]^m[0]) \* (p[1]^m[1]) \* ... \* (p[l] \* m[l])，其中p是k的各个质因子，m为对应的次数。由于各个质因子之间是相互独立的，那么可以对这些质因子分别讨论。

不妨假设现在考察的是p[i]和m[i]，那么现在就需要通过n个数的乘积得到p[i]^m[i]。换言之，就是需要将这m[i]个p[i]分配给这n个数，在这里可以给一个数分配多个p[i]，也可以一个都不分配，问一共有多少种分配方法。

转换一下描述，问题就变成了m个小球，放入n个盒子当中，每个盒子里面可以放多个小球，也可以一个小球都不放，问有多少种放法。

对于这个问题，可以使用隔板法解决。由于盒子里面一个小球都不放这种情况是比较难描述的，那么不妨新增n个假球，加上这m个真球一共m + n个球，这些球并排放到一起，那么一共会产生m + n - 1个空隙。从这些空隙当中挑选m - 1个空隙放入隔板，那么最终这些球会被隔成m份，每一份就相当于原问题的一个盒子。很明显，这里插板子的方法一共有C(m + n - 1, m - 1)种，还原到上面的问题，将m[i]个p[i]分配给n个数，一共就有C(n + m[i] - 1, n - 1)种分配方法。

注意到这里的n是非常大的，那么直接求解C(n + m[i] - 1, n - 1)是不太可行的。注意到有2^14 \= 16384 > 10000，也就是说这里的m[i]最大也就是13，因此在这里利用C(m, n) \= C(m, m - n)，将C(n + m[i] - 1, n - 1)转化为C(n + m[i] - 1, m[i])来进行求解。

有了上面的结论，原题中n个数的乘积等于k的方法总数就是

C(n + m[0] - 1, m[0]) \* C(n + m[1] - 1, m[1]) \* ... \* C(n + m[l] - 1, m[l])

另外，一开始的分解质因数则可以对筛法做一点变形来处理。令f[i]表示i最大的质因子是什么，接下来从2开始到sqrt(k)执行一趟筛法。对于当前处理到的质数p，将后续的f[p \* 2]、f[p \* 3]等都更新为p即可。

得到f数组之后，对于需要分解的k，若k > 1，那么就从中取出其最大的质因数f[k]，此时k就变成了k / f[k]。重复此过程直到k等于1为止，在这个过程中就取出了k所有的质因子。

于是现在就有了一种做法：

1、首先遍历每个query，找出其中最大的n和k，分别记为maxn以及maxk。

2、接下来初始话f为range(maxk)，然后从2到sqrt(maxk)执行一趟筛法，在这个过程中同步更新f。

3、对于每个query中的k[index]，配合f对k[index]分解质因数，使用哈希表cnt_dict[index]记录每个质因子出现的次数。记其中出现次数最多的质因子出现次数为m。

4、此时已经得到了maxn以及m，也就是说所有查询的C都不会超过C(maxn + m - 1, m)，那么只需要预处理出这个范围内的所有C就行了。在这类可以利用C(i, j) \= C(i - 1, j - 1) + C(i - 1, j)来进行递推计算。

5、最后只需要遍历cnt_dict，对于当前的cnt_dict[index]，通过其中记录的每个质因子出现的次数以及n[index]和C来计算当前的query对应的答案。

最后附上python代码：

```python
class Solution(object):
    def waysToFillArray(self, queries):
        """
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        maxn = maxk = 0
        len_q = len(queries)
        res = [1] * len_q
        for n, k in queries:
            maxn = max(maxn, n)
            maxk = max(maxk, k)
        
        f = range(maxk + 1)
        now = 2
        while now * now <= maxk:
            if f[now] == now:
                tmp = now + now
                while tmp <= maxk:
                    f[tmp] = now
                    tmp += now
            
            now += 1
        
        cnt_dict = [{} for _ in range(len_q)]
        m = 0
        for index in range(len_q):
            k = queries[index][1]
            while k > 1:
                cnt_dict[index][f[k]] = cnt_dict[index].get(f[k], 0) + 1
                k /= f[k]

            if cnt_dict[index]:
                m = max(m, max(cnt_dict[index].values()))

        if m == 0:
            return res

        c = [[0] * (m + 1) for _ in range(m + maxn)]
        mod = 10 ** 9 + 7
        for i in range(1, m + maxn):
            for j in range(min(i, m) + 1):
                if i == 1 or j == 0:
                    c[i][j] = 1
                else:
                    c[i][j] = c[i - 1][j - 1] + c[i - 1][j]
                    if c[i][j] >= mod:
                        c[i][j] -= mod

        for index in range(len_q):
            n = queries[index][0]
            for m in cnt_dict[index].values():
                res[index] = (res[index] * c[n + m - 1][m]) % mod
        
        return res
```
