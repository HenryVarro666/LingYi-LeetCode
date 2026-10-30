ARR, K = [3, -7, 1, 2], 3   # 元素互不相同：可以由 num 反推下标

CODE = '''
class Solution(object):
    def kConcatenationMaxSum(self, arr, k):
        mod = 10 ** 9 + 7

        now = 0
        head_max = 0
        for num in arr:
            now += num
            head_max = max(head_max, now)

        now = 0
        tail_max = 0
        for index in range(len(arr) - 1, -1, -1):
            now += arr[index]
            tail_max = max(tail_max, now)

        now = 0
        res = 0
        s = 0
        for num in arr:
            s += num
            now += num
            if now < 0:
                now = 0
            res = max(res, now)

        if k >= 2:
            if s > 0:
                res = max(res, s * (k - 2) + head_max + tail_max) % mod
            else:
                res = max(res, head_max + tail_max) % mod

        return res
'''
_LINES = CODE.strip('\n').split('\n')


def _ln(s, k=0):
    return [i + 1 for i, t in enumerate(_LINES) if s in t][k]


L1, L2, L3, LK = _ln('for num in arr', 0), _ln('for index in range'), _ln('for num in arr', 1), _ln('if k >= 2')
N = len(ARR)


def _phase(S):
    line = S.get('_line', 0)
    if line >= LK:
        return 4
    if line >= L3 - 3:
        return 3
    if line >= L2 - 2:
        return 2
    if line >= L1 - 2:
        return 1
    return 0


def _idx(S):
    ph = _phase(S)
    try:
        if ph in (1, 3):
            return S['arr'].index(S['num'])
        if ph == 2:
            return S['index']
    except Exception:
        return None
    return None


def _starts():
    """第三段（最大子段和）里，每个位置当前子段的起点"""
    out, st, now = [], 0, 0
    for i, x in enumerate(ARR):
        if now == 0:
            st = i
        now += x
        if now < 0:
            now = 0
        out.append(st)
    return out


ST3 = _starts()


def _w(k):
    def f(S):
        ph, i = _phase(S), _idx(S)
        if i is None or S.get('_line') in (L1, L2, L3):
            return None
        if ph == 1:
            return 0 if k == 0 else i
        if ph == 2:
            return i if k == 0 else N - 1
        if ph == 3:
            if S.get('now', 0) <= 0 and S.get('_line', 0) > L3 + 2:
                return None
            return ST3[i] if k == 0 else i
    return f


def _best_pre():
    best, run, e = 0, 0, -1
    for i, x in enumerate(ARR):
        run += x
        if run > best:
            best, e = run, i
    return e


def _best_suf():
    best, run, b = 0, 0, N
    for i in range(N - 1, -1, -1):
        run += ARR[i]
        if run > best:
            best, b = run, i
    return b


PRE_E, SUF_B = _best_pre(), _best_suf()


def _cat_color(S, i, v):
    if _phase(S) != 4:
        return None
    total = sum(ARR)
    last = (K - 1) * N if total > 0 else N   # 前缀取自哪一份 arr
    if SUF_B <= i < N:
        return 'pink'
    if last <= i <= last + PRE_E:
        return 'cyan'
    if total > 0 and N <= i < last:
        return 'purple'
    return None


def _text(S):
    ph = _phase(S)
    if ph == 1:
        return '① 最大==前缀==和 `head_max`（蓝框 = 当前前缀）'
    if ph == 2:
        return '② 最大==后缀==和 `tail_max`（蓝框 = 当前后缀）'
    if ph == 3:
        return '③ 不跨数组：普通的最大子段和 `res`，顺便求总和 `s`'
    if ph == 4:
        s = sum(ARR)
        if s > 0:
            return f'④ 跨数组：`s = {s} > 0` → 后缀 + 中间 `k − 2` 份 + 前缀'
        return f'④ 跨数组：`s = {s} ≤ 0` → 中间的整份不要，只取 ==后缀 + 前缀=='
    return ''


CONFIG = dict(
    num=1191, title='K 次串联后最大子数组之和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='分类讨论：最大前缀 + 最大后缀 + 最大子段和',
    tags=['字节30天'],
    code=CODE,
    call=f'Solution().kConcatenationMaxSum({ARR}, {K})',
    expect=6,
    skip=['mod = 10', 'now += ', 'head_max = 0', 'tail_max = 0', 'res = 0', 's = 0'],
    views=[
        dict(type='text', fn=_text, h=60),
        dict(type='array', var='arr', label='arr', cell=96, pointers={_idx: 'blue'}, pointer_labels={_idx: 'i'},
             window=(_w(0), _w(1)), h=210),
        dict(type='array', var=lambda S: ARR * K if _phase(S) == 4 else None,
             label=f'arr 重复 k = {K} 次（粉 = 第 0 份的最大后缀，青 = 下一份的最大前缀）', cell=60, h=140, color=_cat_color),
    ],
    watch=[('head_max', 'head_max', 'cyan'), ('tail_max', 'tail_max', 'pink'), ('now', 'now'), ('s', 's'), ('res', 'res', 'green')],
    captions={
        5: '① 先求==最大前缀和==：`now` 是当前前缀和，`head_max` 初始为 0（可以一个都不取）',
        11: '② 再求==最大后缀和==：从右往左累加，`tail_max` 初始为 0',
        17: '③ 最后在原数组上做一次==最大子段和==，同时求总和 `s`',
        24: '`now` 清零：从下一个数重新开始',
        'for num in arr': lambda S, B, r: (f'`num = {S.num}`' if S.get('num') != B.get('num') or 'num' not in B else '这一遍扫完了'),
        'head_max = max(': '前缀和 `now = {now}`：`head_max = max({B.head_max}, {now}) = {head_max}`',
        'for index in range': lambda S, B, r: (f'从右往左：`index = {S.index}`' if S.get('index') != B.get('index') or 'index' not in B
                                               else '后缀扫完了'),
        'tail_max = max(': '后缀和 `now = {now}`：`tail_max = max({B.tail_max}, {now}) = {tail_max}`',
        's += num': '`s` 累加总和 → {s}',
        'if now < 0': lambda S, B, r: (f'`now = {B.now} < 0`：前面这段拖后腿 → 清零重来' if B.now < 0
                                       else f'`now = {B.now} ≥ 0`，继续往后接'),
        'res = max(res, now)': '`res = max({B.res}, {now}) = {res}`',
        'if k >= 2': '`k = {k} ≥ 2`：答案还可能跨越多个 arr',
        'if s > 0': lambda S, B, r: (f'`s = {B.s} > 0`：中间的整份 arr 都要保留' if B.s > 0
                                     else f'`s = {B.s} ≤ 0`：中间的整份 arr 只会拖后腿，==直接拼后缀 + 前缀=='),
        'res = max(res, s * (k - 2)': '`max({B.res}, {s}×{k - 2} + {head_max} + {tail_max})` = =={res}==',
        'res = max(res, head_max + tail_max)': '`max({B.res}, {tail_max} + {head_max})` = =={res}==：跨数组更优',
        'return res': '返回 =={ret}==',
    },
    cards=dict(
        one_liner='答案要么不跨数组，要么是「最大后缀 + 中间整份 + 最大前缀」',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['把整数数组 `arr` 重复 `k` 次，求修改后数组的==最大子数组和==',
                 '子数组可以为空（和为 0）；结果对 `10^9 + 7` 取模',
                 '示例：`[1,2], k = 3` → `9`；`[1,-2,1], k = 5` → `2`',
                 '本视频：`arr = [3,-7,1,2]`，`k = 3` → `6`（`sum(arr) < 0`）'],
        quote='第0个原始数组的某个后缀加上第1到第p - 1个原始数组的全体加上第p个原始数组的前缀。……==当arr所有元素之和大于0时，才有必要保留第1到第p - 1个原始数组==',
        quote_src='—— yiduobo 题解原文',
        idea=['情况 1：不跨数组 → 原数组上求一次最大子段和',
              '情况 2：跨数组 → 第 0 份的最大后缀 + 中间若干整份 + 最后一份的最大前缀',
              '`sum > 0` 时中间 `k − 2` 份全要；否则只拼后缀 + 前缀'],
        summary=['时间 `O(n)`：三趟扫描，分别求最大前缀、最大后缀、最大子段和',
                 '易错：`k = 1` 时不能跨数组，所以要判 `k >= 2`',
                 '对比灵神：灵神直接对 arr+arr 跑 53 题，结论相同、代码更短',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
