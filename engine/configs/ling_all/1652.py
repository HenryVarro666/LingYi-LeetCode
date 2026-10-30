def _win(S):
    """当前 s 对应的窗口下标（取模后），按顺序"""
    if 's' not in S or 'r' not in S:
        return []
    r, k, n = S['r'], S['k'], S['n']
    if S.get('_line') == 11:   # s 已更新、r 还没加一
        return [(j) % n for j in range(r - k + 1, r + 1)]
    return [j % n for j in range(r - k, r)]


def _ccol(S, i, v):
    return 'cyan' if i in _win(S) else None


def _txt(S):
    w = _win(S)
    if not w:
        return '无论 k 正负，==窗口都向右滑==，只是起点不同'
    parts = ' + '.join(str(S['code'][j]) for j in w)
    return f"窗口（循环）下标 `{w}`：`{parts}` = =={S['s']}=="


def _rinit(S, B, ret):
    if S.r == S.k + 1:
        return f'`k = {S.k} > 0`：第一个窗口是 `[1, k+1)`，右开端点 `r = {S.r}`'
    return f'`k = {S.k} < 0`：第一个窗口是 `[n − |k|, n)`，右开端点 `r = {S.r}`'


CONFIG = dict(
    num=1652, title='拆炸弹', difficulty='Easy', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='循环数组 · 定长滑动窗口',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution:
    def decrypt(self, code: List[int], k: int) -> List[int]:
        n = len(code)
        r = k + 1 if k > 0 else n  # 第一个窗口的右开端点
        k = abs(k)
        s = sum(code[r - k: r])  # 第一个窗口的元素和

        ans = [0] * n
        for i in range(n):
            ans[i] = s
            s += code[r % n] - code[(r - k) % n]
            r += 1
        return ans
''',
    call='Solution().decrypt([3,1,4,1,5,9], 3)',
    expect=[6, 10, 15, 17, 13, 8],
    views=[
        dict(type='array', var='code', label='code（循环数组，青 = 当前窗口）', h=230, cell=100,
             pointers={'i': 'blue'}, color=_ccol),
        dict(type='array', var='ans', label='ans', h=200, cell=100, pointers={'i': 'blue'},
             color=lambda S, i, v: 'green' if 'i' in S and i <= S['i'] and S.get('_line') != 9 or ('i' in S and i < S['i']) else None),
        dict(type='text', h=90, size=28, fn=_txt),
    ],
    watch=['n', ('k', 'k'), ('r', 'r', 'pink'), ('s', 's', 'orange'), ('i', 'i', 'blue')],
    captions={
        'n = len': '`n = {n}`',
        'r = k + 1 if': _rinit,
        'k = abs(k)': '窗口大小都是 `|k| = {k}`',
        's = sum(code': '第一个窗口 `code[{r - k}:{r}]` 的和 `s = {s}`',
        'ans = [0] * n': '`ans` 先全填 0（`k = 0` 时窗口为空，s 一直是 0，不用特判）',
        'for i in range': lambda S, B, ret: (f'计算 `ans[{S.i}]`' if 'i' not in B or S.i != B.i else '每个位置都算完了'),
        'ans[i] = s': '`ans[{i}]` = 当前窗口和 =={s}==',
        's += code[r % n]': '窗口右移：加上 `code[{B.r % n}] = {code[B.r % n]}`，减去 `code[{(B.r - k) % n}] = {code[(B.r - k) % n]}` → `s = {s}`（==下标取模==实现循环）',
        'r += 1': '右开端点 `r` → {r}',
        'return ans': '解密结果 `{ans}`',
    },
    cards=dict(
        one_liner='无论 k 正负，窗口都在向右移动，只有起点不同',
        complexity='时间 `O(n)`，空间 `O(1)`（返回值不计）',
        problem=['循环数组 `code` 和密钥 `k`：`k > 0` 把每个数换成==后面== k 个数之和',
                 '`k < 0` 换成==前面== |k| 个数之和，`k = 0` 换成 0；所有数同时替换',
                 '示例：`[5,7,1,4], k = 3` → `[12,10,16,13]`；本视频 `[3,1,4,1,5,9], k = 3`'],
        quote='注意到，无论 k>0 还是 k<0，==窗口都在向右移动==，只有初始位置不同。所以找到第一个窗口的下标范围，就可以开滑了！',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k > 0`：第一个窗口 `[1, k+1)`；`k < 0`：第一个窗口 `[n−|k|, n)`',
              '窗口大小都是 `|k|`，移入下标 `r mod n`，移出下标 `(r−|k|) mod n`',
              '先记 `ans[i] = s`，再滑动一格'],
        summary=['时间 `O(n)`，空间 `O(1)`（返回值不计）',
                 '`k = 0` 不用特判：窗口为空，s 恒为 0',
                 '易错：移入、移出下标都要 `% n`',
                 '第一个窗口 `code[r-k:r]` 不会越界（r ≤ n）'],
    ),
)
