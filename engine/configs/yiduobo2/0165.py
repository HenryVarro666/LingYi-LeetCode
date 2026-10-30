V1, V2 = '1.0.1', '1.00'
SLOTS = max(len(V1.split('.')), len(V2.split('.')))


def _col(name):
    def f(S, i, v):
        now = S.get('now')
        if now is None:
            return None
        if i < now:
            return 'green'
        if i == now and 'v1_number' in S and S.get('_line', 0) >= 8:
            return 'yellow' if S['v1_number'] == S['v2_number'] else 'red'
        return None
    return f


def _cmp(S):
    if 'v2_number' not in S or S.get('_line') not in (9, 11, 12, 14):
        if 'now' in S:
            return f'`now = {S["now"]}`：v1 有 `{len(S["v1"])}` 段，v2 有 `{len(S["v2"])}` 段；==有一个没比完就继续=='
        return ''
    a, b = S['v1_number'], S['v2_number']
    op = '=' if a == b else ('<' if a < b else '>')
    return f'第 `{S["now"]}` 段：`v1_number = {a}` ==' + op + f'== `v2_number = {b}`'


def _cap_num(which):
    def f(S, B, ret):
        lst, num = S[which], S[f'{which}_number']
        if S.now < len(lst):
            raw = lst[S.now]
            tail = '，==前导零被 int 忽略==' if len(raw) > 1 and raw[0] == '0' else ''
            return f"`int({which}[{S.now}]) = int('{raw}') = {num}`{tail}"
        return f'`{which}` 只有 `{len(lst)}` 段，第 `{S.now}` 段==缺失，当做 0=='
    return f


CONFIG = dict(
    num=165, title='比较版本号', difficulty='Medium', category='字符串',
    author='yiduobo', technique='split 后逐段比较 · 缺失按 0',
    tags=['字节30天', '热题173'],
    code='''
class Solution(object):
    def compareVersion(self, version1, version2):
        v1 = version1.split('.')
        v2 = version2.split('.')

        now = 0
        while now < len(v1) or now < len(v2):
            v1_number = int(v1[now]) if now < len(v1) else 0
            v2_number = int(v2[now]) if now < len(v2) else 0
            if v1_number < v2_number:
                return -1
            elif v1_number > v2_number:
                return 1
            else:
                now += 1

        return 0
''',
    call=f'Solution().compareVersion({V1!r}, {V2!r})',
    expect=1,
    views=[
        dict(type='array', var='v1', label=f"v1 = '{V1}'.split('.')", min_slots=SLOTS, cell=120,
             pointers={'now': 'blue'}, color=_col('v1'), h=215),
        dict(type='array', var='v2', label=f"v2 = '{V2}'.split('.')", min_slots=SLOTS, cell=120,
             pointers={'now': 'blue'}, color=_col('v2'), h=225),
        dict(type='text', h=80, size=28, fn=_cmp),
    ],
    watch=[('now', 'now', 'blue'), 'v1_number', 'v2_number'],
    captions={
        'v1 = version1.split': "按 `.` 分割：`v1 = {v1}`",
        'v2 = version2.split': "`v2 = {v2}`（只有 `{len(v2)}` 段）",
        'now = 0': '`now`：当前比较第几段',
        'while now < len(v1) or': lambda S, B, ret: (
            f'`now = {S.now}`：至少一个版本还有第 `{S.now}` 段 → 继续' if S.now < len(S.v1) or S.now < len(S.v2)
            else f'`now = {S.now}`：两个版本都比完了'),
        'v1_number = int': _cap_num('v1'),
        'v2_number = int': _cap_num('v2'),
        'if v1_number < v2_number': lambda S, B, ret: (f'`{S.v1_number} < {S.v2_number}` → version1 更小' if S.v1_number < S.v2_number
                                                        else f'`{S.v1_number} < {S.v2_number}` 不成立'),
        'elif v1_number > v2_number': lambda S, B, ret: (f'`{S.v1_number} > {S.v2_number}`：第一个不同的段，==version1 更大=='
                                                          if S.v1_number > S.v2_number else f'`{S.v1_number} > {S.v2_number}` 也不成立 → 这一段相等'),
        'return -1': '返回 `-1`',
        'return 1': '返回 `1`',
        'now += 1': '这一段相等，比下一段：`now` → {now}',
        'return 0': '所有段都相等，返回 `0`',
    },
    cards=dict(
        one_liner='split 之后逐段转整数比较，缺的段当 0',
        complexity='时间 `O(n + m)`，空间 `O(n + m)`',
        problem=['版本号由 `.` 分隔的修订号组成，修订号按==整数==比较（忽略前导零）',
                 '从左到右比较；某个版本修订号较少时，==缺失的视为 0==',
                 '`v1 < v2` 返回 `-1`，`v1 > v2` 返回 `1`，否则返回 `0`',
                 f'本视频：`"{V1}"` vs `"{V2}"` → `1`'],
        quote='使用split分离字符串之后逐个比较即可，需要注意当某个版本号的某一位缺失时应该当做0来计算。',
        quote_src='—— yiduobo 题解',
        idea=['`split(\'.\')` 得到每一段字符串，`int()` 转整数时前导零自然消失',
              '`while now < len(v1) or now < len(v2)`：==较长的那个==比完才结束',
              '越界的一方取 0；第一处不相等就能决定答案'],
        result='第 `2` 段 `1 > 0`（v2 缺失按 0）→ 返回 `1`',
        summary=['时间 `O(n + m)`，空间 `O(n + m)`',
                 '易错：循环条件是 `or` 不是 `and`，否则 `"1.0.1"` 和 `"1"` 会被判成相等',
                 '易错：按整数比较，`"01"` 和 `"1"` 相等，`"10" > "2"`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串',
                 '对比灵神：灵神用 `zip_longest(fillvalue=0)` 一行完成“补 0”'],
    ),
)
