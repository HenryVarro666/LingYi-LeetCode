def _prev(S):
    return S['index'] - 1 if 'index' in S and S.get('_line') in (9, 10) else None


def _formula(S):
    f = S['f']
    m = len(f)
    if 'index' in S and S.get('_line') in (9, 10):
        i = S['index']
        return (f'`f[{i}]` 对应 ==看到 {m - i} 根==：新棍 1 插在 {S["l"]} 个非最前位置（`f[{i}] × {S["l"]}`），'
                f'或插最前面（`f[{i-1}]`，多看到 1 根）')
    return f'数组 `f[j]` = 当前 `{m}` 根棍里「恰好看到 `{m} − j` 根」的排列数（高位在前）'


CONFIG = dict(
    num=1866, title='恰有 K 根木棍可以看到的排列数目', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='插入最短棍 · 递推（第一类斯特林数）',
    tags=['数学算法', '难度分 2333'],
    code='''
class Solution(object):
    def rearrangeSticks(self, n, k):

        f = [1]
        mod = 10 ** 9 + 7
        for l in range(1, n):
            f.append(0)
            for index in range(l, 0, -1):
                f[index] += f[index - 1] * l
                f[index] %= mod

        return f[n - k]
''',
    call='Solution().rearrangeSticks(5, 3)',
    expect=35,
    skip=['f[index] %= mod', 'mod = '],
    views=[
        dict(type='text', fn=_formula, size=24, h=80),
        dict(type='array', var='f', label='f[j]（粉 = 正在更新，蓝 = 它加上的 f[j-1]）', cell=100, h=230,
             pointers={'index': 'pink', _prev: 'blue'}, pointer_labels={_prev: 'index-1'},
             color=lambda S, i, v: ('pink' if i == S.get('index') else 'blue' if i == _prev(S) else None) if S.get('_line') in (9, 10) else None),
        dict(type='text', fn=lambda S: f"当前已有 `{len(S['f'])}` 根棍；`l = {S['l']}` 是即将被插入的新棍之前的根数" if 'l' in S else '', size=22, h=50),
    ],
    watch=[('l', 'l', 'blue'), ('index', 'index', 'pink'), ('n', 'n'), ('k', 'k')],
    captions={
        'f = [1]': '只有 1 根棍：看到 1 根的排列 1 种。`f = [1]`（高位在前，下标 `j` 表示看到 `根数 − j` 根）',
        'for l in range': lambda S, B, r: ('`l` 已到 `n - 1`，所有棍都加完了' if B.get('l') == S.get('l') and 'l' in B
                                           else f'现有 `{S.l}` 根棍，再加入一根==最短==的棍（长度 1）：它能插在 `{S.l + 1}` 个位置'),
        'f.append(0)': '末尾补 0：相当于把旧答案整体「向前移一位」——新棍放最前面时多看到 1 根',
        'f[index] += f[index - 1] * l': lambda S, B, r: (f'`f[{S.index}] = {B.f[S.index]} + f[{S.index-1}] × {S.l}` = =={S.f[S.index]}=='
                                                       f'（旧值 × {S.l}：新棍藏在后面不被看到；`f[{S.index-1}]` 对应放最前）'),
        'return f[n - k]': '倒着存，看到 `k` 根对应下标 `n − k = {n - k}` → =={ret}==',
    },
    cards=dict(
        one_liner='从最短的棍入手：放最前面多看到一根，放别处看不到',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['`1..n` 的 `n` 根棍排成一排，从左边看，左侧没有更长棍的才「看得到」',
                 '求恰好看到 `k` 根的排列数（对 `10^9+7` 取模）',
                 '示例：`n = 3, k = 2` → `3`；本视频演示 `n = 5, k = 3` → `35`'],
        quote='我在这里考虑是最短的木棍，相比考虑最长的木棍要简单明了得多。……当这个木棍插入到排列的最前方时，就相当于在之前三根木棍排列的基础上可以额外多看到一根木棍。',
        quote_src='—— yiduobo 题解',
        idea=['`f[i]` 记「`i` 根棍的排列，看到 1..i 根」的分布；再加一根长度 1 的新棍',
              '插最前面：新棍一定被看到，分布向看到更多一格移动',
              '插其他 `i` 个位置：新棍被挡住，分布不变，复制 `i` 份',
              '为了不用移动数组，倒着存（高位在前），末尾补 0 就是「移位」'],
        summary=['时间 `O(n^2)`，空间 `O(n)`；就是第一类斯特林数',
                 '易错：倒序遍历 `index`，否则会用到刚更新过的 `f[index-1]`',
                 '易错：倒着存，答案在 `f[n-k]` 而不是 `f[k]`',
                 '代码为 Python 3 可直接运行，未做修改'],
    ),
)
