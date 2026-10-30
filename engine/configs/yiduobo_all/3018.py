NUMS, QS = [2, 1, 3], [3, 2, 3]


def _cur(S):
    """(left, right) currently being computed, else None"""
    inner = S.get('_inner', {})
    if 'right' in inner and 'left' in inner and 'f' in inner and S.get('_line', 0) <= 24 and 'index' not in inner:
        return inner['left'], inner['right']
    return None


def _nq(S):
    inner = S.get('_inner', {})
    if 'index' in inner:
        return inner['f'][inner['index']][inner['index']]
    c = _cur(S)
    if c is None:
        return None
    return inner['f'][c[0]][c[1]]


def _win(S):
    inner = S.get('_inner', {})
    if 'index' in inner:
        return inner['index']
    c = _cur(S)
    return None if c is None else c[0]


def _winr(S):
    inner = S.get('_inner', {})
    if 'index' in inner:
        return inner['index']
    c = _cur(S)
    return None if c is None else c[1]


def _ncolor(S, i, v):
    c = _cur(S)
    line = S.get('_line')
    if c is None:
        return None
    left, right = c
    if line in (9, 10, 11, 12, 13, 14) and left > 0 and i == left - 1:
        return 'blue'
    if line in (16, 17, 18, 19, 20, 21) and i == right + 1:
        return 'blue'
    return None


def _fcolor(S, r, c, v):
    cur = _cur(S)
    inner = S.get('_inner', {})
    if 'index' in inner:
        return 'yellow' if r == c == inner['index'] else None
    if cur is None:
        return None
    left, right = cur
    if (r, c) == (left, right):
        return 'yellow'
    line = S.get('_line')
    if line in (9, 10, 11, 12, 13, 14) and (r, c) == (left - 1, right):
        return 'blue'
    if line in (16, 17, 18, 19, 20, 21) and (r, c) == (left, right + 1):
        return 'blue'
    return None


def _txt(S):
    inner = S.get('_inner', {})
    if 'index' in inner:
        i = inner['index']
        return f'最后：只剩 `nums[{i}]`，还能多匹配一个吗？`f[{i}][{i}] + delta`'
    c = _cur(S)
    if c is None:
        return '`f[left][right]` = 只剩下 `nums[left..right]` 时，最多能匹配 `queries` 的前几个'
    left, right = c
    return f'`f[{left}][{right}]`：外面的数已删光/用掉，剩 `nums[{left}..{right}]`；已匹配前 ==`{S["_inner"]["f"][left][right]}`== 个询问'


def _chk(side):
    def fn(S, B, ret):
        inner = S['_inner']
        left, right, f = inner['left'], inner['right'], inner['f']
        if side == 'L':
            p, q = left - 1, right
            idx = f[p][q]
            nm = 'left - 1'
        else:
            p, q = left, right + 1
            idx = f[p][q]
            nm = 'right + 1'
        pos = p if side == 'L' else q
        if idx >= len(QS):
            return f'`f[{p}][{q}] = {idx}` 已匹配完所有询问 → 不能再加，`delta = 0`'
        ok = NUMS[pos] >= QS[idx]
        return (f'`nums[{nm}] = {NUMS[pos]}` {"≥" if ok else "<"} `queries[{idx}] = {QS[idx]}` → '
                + ('==能匹配，多处理一个=='if ok else '不够大，只能把它删掉（不匹配）'))
    return fn


CONFIG = dict(
    num=3018, title='可处理的最大删除操作数 I', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='区间 DP · 由外向内，状态里存已匹配的前缀长度',
    tags=['灵神题单', '动态规划'],
    code='''
class Solution(object):
    def maximumProcessableQueries(self, nums, queries):

        n = len(nums)
        f = [[0] * n for _ in range(n)]
        for l in range(n - 1, 0, -1):
            for left in range(n):
                right = left + l - 1
                if right >= n:
                    break
                
                if left > 0:
                    if f[left - 1][right] < len(queries) and nums[left - 1] >= queries[f[left - 1][right]]:
                        delta = 1
                    else:
                        delta = 0
                    
                    f[left][right] = f[left - 1][right] + delta

                if right < n - 1:
                    if f[left][right + 1] < len(queries) and nums[right + 1] >= queries[f[left][right + 1]]:
                        delta = 1
                    else:
                        delta = 0
                    
                    f[left][right] = max(f[left][right], f[left][right + 1] + delta)
                
                if f[left][right] == len(queries):
                    return f[left][right]

        res = 0
        for index in range(n):
            if nums[index] >= queries[f[index][index]]:
                delta = 1
            else:
                delta = 0
            res = max(res, f[index][index] + delta)
        
        return res
''',
    call=f'Solution().maximumProcessableQueries({NUMS}, {QS})',
    expect=2,
    max_steps=110,
    skip=['n = len(nums)', 'f = [[0]', 'right = left + l - 1', 'if right >= n', 'break', 'for left in range',
          'delta = 0', 'res = 0'],
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='array', var=lambda S: NUMS, label='nums（框 = 剩下的 [left, right]，蓝 = 正在考察的数）', cell=80, h=150,
             window=(_win, _winr), color=_ncolor),
        dict(type='array', var=lambda S: QS, label='queries（箭头 = 下一个要匹配的 = f[left][right]）', cell=80, h=200,
             pointers={_nq: 'pink'}, pointer_labels={_nq: '下一个'}),
        dict(type='table', var='f', label='f[left][right]（黄 = 正在算，蓝 = 来源）', h=280, cell=64,
             rows=lambda S: [f'L{k}' for k in range(len(NUMS))], cols=lambda S: [f'R{k}' for k in range(len(NUMS))],
             color=_fcolor),
    ],
    watch=[('l', lambda S: S['_inner'].get('l'), 'yellow'), ('left', lambda S: S['_inner'].get('left'), 'blue'),
           ('right', lambda S: S['_inner'].get('right'), 'pink'), ('res', lambda S: S['_inner'].get('res'), 'green')],
    captions={
        'for l in range': lambda S, B, r: (f'剩下的区间长度 `l = {S.l}`：==从长到短==，先算外层（删得少）再算内层'
                                           if S.get('l') != B.get('l') else '区间长度枚举完了'),
        'if left > 0': lambda S, B, r: (f'`left = {S.left}`：区间左边还有 `nums[{S.left - 1}]` → 看看从 `f[{S.left - 1}][{S.right}]` 转移过来'
                                        if S.left > 0 else '`left = 0`：左边没有数，不用从左边转移'),
        'if f[left - 1][right] <': _chk('L'),
        'delta = 1': '`delta = 1`：这个数留下来匹配下一个询问',
        'f[left][right] = f[left - 1][right] + delta': '`f[{left}][{right}] = f[{left - 1}][{right}] + {delta}` = =={f[left][right]}==',
        'if right < n - 1': lambda S, B, r: (f'`right = {S.right}`：右边还有 `nums[{S.right + 1}]` → 对称地从 `f[{S.left}][{S.right + 1}]` 转移'
                                             if S.right < len(NUMS) - 1 else '`right` 已是末尾，右边没有数'),
        'if f[left][right + 1] <': _chk('R'),
        'f[left][right] = max(': '`f[{left}][{right}] = max(左边来的, {f[left][right + 1]} + {delta})` = =={f[left][right]}==',
        'if f[left][right] == len': lambda S, B, r: (f'`f[{S.left}][{S.right}] = {S.f[S.left][S.right]}` 等于询问总数 → ==全部处理完，直接返回==' if S.f[S.left][S.right] == len(QS)
                                                    else f'`f[{S.left}][{S.right}] = {S.f[S.left][S.right]}` < 询问总数 `{len(QS)}`，继续'),
        'for index in range': lambda S, B, r: (f'最后一轮：状态里没法表示“全部用完”，所以单独看每个 `nums[{S.index}]`'
                                               if S.get('index') != B.get('index') or B.get('index') is None else '每个 `nums[index]` 都看过了'),
        'if nums[index] >=': lambda S, B, r: (f'`nums[{S.index}] = {NUMS[S.index]}` vs `queries[{S.f[S.index][S.index]}] = {QS[S.f[S.index][S.index]]}` → '
                                              + ('==还能多匹配一个==' if NUMS[S.index] >= QS[S.f[S.index][S.index]] else '匹配不了')),
        'res = max': '`res = max(.., f[{index}][{index}] + {delta})` = =={res}==',
        'return res': '最多能处理 `{ret}` 个询问',
    },
    cards=dict(
        one_liner='由外向内删数，状态里直接存“已匹配的前缀长度”',
        complexity='时间 `O(n^2)`，空间 `O(n^2)`',
        problem=['给 `nums` 和 `queries`。可先任意删数（取子序列），再依次处理询问',
                 '处理 `queries[i]`：取 `nums` 两端中 `≥ queries[i]` 的一个删掉；两端都更小就停',
                 '求最多能处理几个询问。本视频：`[2,1,3]`、`[3,2,3]` → `2`'],
        quote='题目看上去像是很常规的区间动态规划问题，但是在这里是外侧匹配数组的前缀，那么状态的设计和更新的方向就需要反过来。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[left][right]`：整个数组删到只剩 `left..right` 时，能匹配 `queries` 的最长前缀',
              '外层 `l` 从大到小：从 `f[left-1][right]` 或 `f[left][right+1]` 转移，多删一个数',
              '被删的数 `≥ queries[f[..]]` 就多匹配一个（`+1`），否则当作白删（`+0`）'],
        summary=['时间 `O(n^2)`，空间 `O(n^2)`',
                 '“下一个要匹配的位置”存在 `f` 的值里，所以必须由外向内转移，而不是常规的由内向外',
                 '区间长度 `l` 从 `n-1` 开始：长度 `n` 的状态全是 0，不用算',
                 '最后要单独遍历每个 `nums[index]`：状态无法表示“数全用完”',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；本题无整数除法'],
    ),
)
