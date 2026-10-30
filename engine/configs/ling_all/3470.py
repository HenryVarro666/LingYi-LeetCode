def _cand(S):
    if 'cand' not in S:
        return '`f[n]` = 偶数全排 × 奇数全排：`1,1,1,2,2,6,6,24,…`'
    c = S['cand']
    return f'剩余偶数 `cand[0] = {c[0]}`　剩余奇数 `cand[1] = {c[1]}`'


def _state(S):
    if 'ans' not in S:
        return ''
    k = S.get('k')
    s = f'`k = {k}`（从 0 开始计数）'
    if 'parity' in S:
        s += f'；这一位要填==' + ('奇数' if S['parity'] == 1 else '偶数') + '=='
    return s


CONFIG = dict(
    num=3470, title='全排列 IV', difficulty='Hard', category='数学算法',
    author='灵茶山艾府', technique='按组定位 · 逐位确定',
    tags=['组合数学', '难度分 2474'],
    code='''
# 预处理交替排列的方案数
f = [1]
i = 1
while f[-1] < 10 ** 15:
    f.append(f[-1] * i)
    f.append(f[-1] * i)
    i += 1

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # k 改成从 0 开始，方便计算
        k -= 1
        if n < len(f) and k >= f[n] * (2 - n % 2):  # n 是偶数的时候，方案数乘以 2
            return []

        # cand 表示剩余未填入 ans 的数字
        # cand[0] 保存偶数，cand[1] 保存奇数
        cand = [list(range(2, n + 1, 2)), list(range(1, n + 1, 2))]

        ans = [0] * n
        parity = 1  # 当前要填入 ans 的数字的奇偶性
        for i in range(n):
            if n - 1 - i < len(f):
                # 比如示例 1，按照第一个数分组，每一组的大小都是 size=f[n-1-i]=f[3]=2
                # 知道 k 和 size 就知道我们要去哪一组（第 j 组）
                j, k = divmod(k, f[n - 1 - i])
                # n 是偶数的情况，第一个数既可以填奇数又可以填偶数，要特殊处理
                if n % 2 == 0 and i == 0:
                    parity = 1 - j % 2
                    j //= 2
            else:
                j = 0  # n 很大的情况下，只能按照 1,2,3,... 的顺序填
            ans[i] = cand[parity].pop(j)
            parity ^= 1  # 下一个数的奇偶性
        return ans
''',
    call='Solution().permute(4, 6)',
    expect=[3, 4, 1, 2],
    skip=['f.append', 'i += 1', 'while f[-1]', 'else:', 'j = 0'],
    max_steps=60,
    views=[
        dict(type='text', fn=_cand, size=26, h=70),
        dict(type='text', fn=lambda S: '预处理 `f[n] = floor(n/2)! × ceil(n/2)!`（奇偶位置互相独立）：`f = [1, 1, 1, 2, 2, 6, 6, 24, 24, …]`', size=24, h=90),
        dict(type='array', var='ans', label='ans（逐位填）', h=210, cell=90, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_state, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'yellow'), ('parity', 'parity', 'green')],
    captions={
        'k -= 1': '`k` 改成从 0 开始：`k = {k}`',
        'if n < len(f) and k >=': '总方案数 `f[n]`（偶数长度乘 2）比 `k = {k}` 大 → 有解；否则返回空列表',
        'return []': '不足 `k` 个交替排列 → 返回空列表',
        'cand = [': '偶数、奇数各放一个有序列表，填一个就删一个',
        'ans = [0] * n': '`ans` 先占好 `n` 个位置',
        'parity = 1  #': '先假定第一位填奇数（偶数长度时稍后再修正）',
        'for i in range': lambda S, B, r: (f'开始填第 `{S.i}` 位' if S.i != B.get('i') or 'i' not in B else '四位都填完了'),
        'j, k = divmod': '每组大小 = 后面 `{n - 1 - i}` 位的方案数；`k = {B.k}` 落在第 `j = {j}` 组，组内排名 `k = {k}`',
        'parity = 1 - j % 2': '第一位按 1,2,3,4 排，`j = {j}`：j 偶数 → 奇数开头，j 奇数 → 偶数开头；这里填=={"奇" if parity else "偶"}数==',
        'j //= 2': '同奇偶的候选里，真正的组号是 `j // 2` = {j}',
        'ans[i] = cand[parity].pop(j)': '从{"奇" if parity else "偶"}数候选里取出第 `{j}` 小的：`ans[{i}]` = =={ans[i]}==',
        'parity ^= 1': '下一位奇偶翻转 → {"奇" if parity else "偶"}数',
        'return ans': '第 6 个交替排列 = =={ret}==',
    },
    cards=dict(
        one_liner='按第一个数分组，用 k 除以组大小，一位位确定',
        complexity='时间 `O(n^2)`，空间 `O(n)`',
        problem=['交替排列：前 `n` 个正整数的排列，相邻两数奇偶性不同',
                 '按字典序返回第 `k` 个，不足 `k` 个返回 `[]`',
                 '示例：`n = 4, k = 6` → `[3,4,1,2]`'],
        quote='所以根据 ⌊k/f[n-1]⌋ 的值，我们可以知道第一个数在第几组，从而确定第一个数填什么。再次强调，k 是从 0 开始的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一个数的奇偶定了，后面奇偶交替就定了；奇偶位置互相独立：`f[n] = floor(n/2)! × ceil(n/2)!`',
              '每组大小 `f[n-1-i]`，`divmod(k, size)` 得到组号 `j`（填第 j 小）和组内排名',
              'n 为偶数时第一位既可奇也可偶，多一步 `parity = 1 - j % 2; j //= 2`'],
        summary=['时间 `O(n^2)`（`pop` 删除），空间 `O(n)`',
                 '易错：`k` 先减 1，从 0 开始才能用 `divmod`',
                 '易错：n 为偶数时方案数要乘 2，第一位要特殊处理',
                 'n 很大时 `f` 数组不够长，说明 `k ≤ 10^15` 只会影响前面一小段，后面按 1,2,3 顺序填（`j = 0`）'],
    ),
)
