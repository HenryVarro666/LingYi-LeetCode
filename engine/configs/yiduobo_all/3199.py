A = [1, 2]
B = [3, 1]
C = [2, 3]


def _par(v):
    return bin(v).count('1') & 1


def _col(S, i, v):
    return 'orange' if _par(v) else 'green'


def _txt(S):
    if 'odd' not in S:
        return '统计每个数二进制里 1 的个数：奇数个（橙）/ 偶数个（绿）'
    return f"当前统计：奇数个 1 的有 `{S['odd']}` 个，偶数个的有 `{S['even']}` 个"


CONFIG = dict(
    num=3199, title='用偶数异或设置位计数三元组 I', difficulty='Easy', category='位运算',
    author='yiduobo', technique='按 1 的个数奇偶性分组计数',
    tags=[],
    code='''
class Solution(object):
    def tripletCount(self, a, b, c):

        def cnt(arr):
            odd = even = 0
            for v in arr:
                one = 0
                while v:
                    if v & 1:
                        one += 1
                    v >>= 1
            
                if one & 1:
                    odd += 1
                else:
                    even += 1
            
            return odd, even

        odd_a, even_a = cnt(a)
        odd_b, even_b = cnt(b)
        odd_c, even_c = cnt(c)

        return odd_a * odd_b * even_c + odd_a * even_b * odd_c + even_a * odd_b * odd_c + even_a * even_b * even_c
''',
    call='Solution().tripletCount([1,2], [3,1], [2,3])',
    expect=sum(1 for x in A for y in B for z in C if bin(x ^ y ^ z).count('1') % 2 == 0),
    views=[
        dict(type='array', var='a', h=150, label='a', color=_col),
        dict(type='array', var='b', h=150, label='b', color=_col),
        dict(type='array', var='c', h=150, label='c', color=_col),
        dict(type='text', fn=_txt, size=26, h=90),
    ],
    max_steps=90,
    watch=['v', 'one', ('odd', 'odd', 'orange'), ('even', 'even', 'green'), 'odd_a', 'even_a', 'odd_b', 'even_b', 'odd_c', 'even_c'],
    captions={
        'odd = even = 0': '`odd`、`even` 分别统计「1 的个数为奇数 / 偶数」的数',
        'for v in arr': lambda S, B, r: ('数组看完了，退出循环' if S.v == 0 and B.v == 0 else f'取下一个数 `v = {S.v}`'),
        'one = 0': '`one` 清零，准备数这个数二进制里有几个 1',
        'while v': lambda S, B, r: (f'`v = {S.v}` 不为 0，还有位没看' if S.v else '`v` 移空了，所有位都看完'),
        'if v & 1': lambda S, B, r: (f'最低位是 1 → `one` +1' if S.v & 1 else '最低位是 0 → 不计'),
        'one += 1': '`one` → {one}',
        'v >>= 1': '右移一位，看下一位',
        'if one & 1': lambda S, B, r: (f'`one = {S.one}` 是奇数 → 归入 odd' if S.one & 1 else f'`one = {S.one}` 是偶数 → 归入 even'),
        'odd += 1': '`odd` → {odd}',
        'even += 1': '`even` → {even}',
        'return odd, even': '这个数组：奇数个 1 的有 `{odd}` 个，偶数个 1 的有 `{even}` 个',
        'odd_a, even_a': '`a` 的统计：`odd_a = {odd_a}`，`even_a = {even_a}`',
        'odd_b, even_b': '`b` 的统计：`odd_b = {odd_b}`，`even_b = {even_b}`',
        'odd_c, even_c': '`c` 的统计：`odd_c = {odd_c}`，`even_c = {even_c}`',
        'return odd_a': '四种奇偶组合（奇奇偶、奇偶奇、偶奇奇、偶偶偶）相加，共 =={ret}== 个三元组',
    },
    cards=dict(
        one_liner='异或后 1 的个数是否为偶数，只和三个数各自 1 的个数的奇偶有关',
        complexity='时间 `O(n log U)`，空间 `O(1)`',
        problem=['给三个整数数组 `a`、`b`、`c`',
                 '数有多少个三元组 `(i, j, k)`，使 `a[i] ^ b[j] ^ c[k]` 的二进制里 1 的个数是偶数',
                 '本视频：`a=[1,2]`，`b=[3,1]`，`c=[2,3]`'],
        quote='x^y的二进制表示中1的数量就是s[x] + s[y] - t[(x, y)] * 2，……与s[x] + s[y]是同奇偶的。',
        quote_src='—— yiduobo 题解原文',
        idea=['异或会把两个都是 1 的位消成 0，每次少掉偶数个 1，所以奇偶性不变',
              '于是三数异或的奇偶 = 三个数各自 1 的个数奇偶之和',
              '只要三者里「奇」的个数为 0 或 2：奇奇偶、奇偶奇、偶奇奇、偶偶偶'],
        summary=['时间 `O(n log U)`（逐位数 1），空间 `O(1)`',
                 '四个乘积项对应「奇数个 1 的个数」为 2 或 0 的情形',
                 '数据规模很小，暴力三重循环也行；奇偶分组可以推广到大数据',
                 '原文代码本身就是 Python 3 可运行，未做修改',
                 '题面库里缺失，题意据 yiduobo 文章与 LeetCode 原题整理'],
    ),
)
