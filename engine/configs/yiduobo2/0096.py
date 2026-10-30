from math import comb as _comb


def _cat(k):
    return _comb(2 * k, k) // (k + 1)


def _k(S):
    """当前 f 对应的节点数：循环前 f = f[1]，第 index 轮算完后 f = f[index + 1]"""
    if 'f' not in S:
        return None
    if 'index' not in S:
        return 1
    return S['index'] + 1 if S['f'] == _cat(S['index'] + 1) else S['index']


def _formula(S, B):
    if 'index' not in S or 'f' not in S:
        return '递推：`f[i+1] = f[i] × 2 × (2i+1) / (i+2)`，从 `f[1] = 1` 开始'
    i = S['index']
    if S['_line'] == 5 and 'f' in B:
        return f'`f[{i + 1}] = {B["f"]} × 2 × {2 * i + 1} // {i + 2}` = =={S["f"]}=='
    return f'下一步：`f[{i + 1}] = f[{i}] × 2 × ({i}+{i}+1) / ({i}+2)`'


def _check(S):
    k = _k(S)
    if k is None or k < 2:
        return ''
    terms = ' + '.join(f'{_cat(j)}×{_cat(k - 1 - j)}' for j in range(k))
    return f'验证 `f[{k}]`：枚举根 → `{terms}` = =={_cat(k)}=='


CONFIG = dict(
    num=96, title='不同的二叉搜索树', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='卡特兰数 · 一维递推',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def numTrees(self, n):
        f = 1
        for index in range(1, n):
            f = f * 2 * (index + index + 1) // (index + 2)
        return f
''',
    call='Solution().numTrees(6)',
    expect=132,
    views=[
        dict(type='text', fn=_formula, size=28),
        dict(type='array', var=lambda S: [_cat(k) for k in range(S['n'] + 1)] if 'n' in S else None,
             label='f[i]：i 个节点能形成多少棵不同的 BST（暗 = 还没算到）', cell=96, h=230,
             pointers={_k: 'green'}, pointer_labels={_k: 'f'},
             dim=lambda S, i, v: _k(S) is None or i > _k(S),
             color=lambda S, i, v: 'green' if i == _k(S) else None),
        dict(type='text', fn=lambda S: '对照求和式：`f[i] = f[0]·f[i-1] + f[1]·f[i-2] + … + f[i-1]·f[0]`', size=24, h=60),
        dict(type='text', fn=_check, size=24, h=100, lines=2),
    ],
    watch=['n', ('index', 'index', 'blue'), ('f', 'f', 'green')],
    captions={
        'f = 1': '`f = f[1] = 1`：1 个节点只有一种树（`f[0] = 1` 也一样）',
        'for index in range(1, n)': lambda S, B, ret: (
            f'`index = {S.index}`：由 `f[{S.index}]` 推出 `f[{S.index + 1}]`'
            if S.get('index') is not None and (B.get('index') != S.index) else f'`index` 到 `n - 1 = {S.n - 1}` 为止，已经算出 `f[{S.n}]`'),
        'f = f * 2': lambda S, B, ret: (
            f'`f[2] = {B.f} × 2 × {2 * S.index + 1} // {S.index + 2} = {S.f}`：原文 `/` 是 Python 2 整除，==这里改为 //=='
            if S.index == 1 else
            f'`f[{S.index + 1}] = {B.f} × 2 × {2 * S.index + 1} // {S.index + 2}` = =={S.f}==' + ('（从左往右==先乘后除==，结果一定是整数）' if S.index == 2 else '')),
        'return f': '返回 `f[{n}] = {ret}`：{n} 个节点共有 {ret} 种不同的 BST',
    },
    cards=dict(
        one_liner='选一个数当根，左右子树方案数相乘再求和 → 卡特兰数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给你一个整数 `n`，求恰由 `n` 个节点组成、节点值为 `1` 到 `n` 的',
                 '==二叉搜索树==有多少种？',
                 '示例：`n = 3` → `5`；`n = 1` → `1`；本视频 `n = 6` → `132`'],
        before=[dict(heading='先想清楚：f[i] 怎么来', lines=[
            '依次选 `1..i` 中的某个数 `j` 当根：左边 `j-1` 个数，右边 `i-j` 个数',
            '左右子树各自独立 → 方案数 ==相乘==：`f[j-1] × f[i-j]`',
            '所以 `f[i] = f[0]·f[i-1] + f[1]·f[i-2] + … + f[i-1]·f[0]`',
            '`f[0] = f[1] = 1`；这一串 1, 1, 2, 5, 14, 42… 就是==卡特兰数==',
        ])],
        quote='上面这个式子被称作卡特兰数，其递推公式为 ==f[i + 1] = f[i] * 2 * (2 * i + 1) / (i + 2)==。于是最后也可以直接递推计算出结果。',
        quote_src='—— yiduobo 题解',
        idea=['`O(n²)` 的求和式已经能做，但卡特兰数有更快的一阶递推',
              '只需一个变量 `f`：从 `f[1] = 1` 出发，`index` 从 1 推到 `n-1`',
              '每步 `f[index] → f[index+1]`，循环结束就是 `f[n]`'],
        result='运行结束：`f[6] = 132` ✓',
        summary=['时间 `O(n)`，空间 `O(1)`；求和式 DP 是 `O(n²)`',
                 '原文为 Python 2 写法：`/` 整除已改为 `//`，并删去 docstring',
                 '易错：必须==先乘后除==（从左到右算），先算 `(2i+1)/(i+2)` 会出现小数',
                 '`n = 1` 时循环不执行，直接返回 1',
                 '上一题 95 要求列出所有树，本题只要数量'],
    ),
)
