def _top(S):
    if 'size' not in S:
        return ''
    r = S.get('res', '')
    t = S.get('t')
    cur = f"，当前子串 `t = '{t}'`" if t is not None and S['_line'] >= 15 else ''
    return f"枚举长度 `size = {S['size']}`{cur}，目前最优 `res = '{r}'`"


def _check(S):
    if 'sub' not in S:
        return '先枚举 arr[i] 的子串 t，再用 check 看别人家有没有'
    return f"check：`{S['sub']}` 是否出现在其它字符串里（`j != i`）"


def _ans(S):
    return f"ans = {S['ans']}" if 'ans' in S else ''


CONFIG = dict(
    num=3076, title='数组中的最短非公共子字符串', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='暴力枚举 · 按长度从小到大',
    tags=['灵神题单', '字符串'],
    code='''
class Solution:
    def shortestSubstrings(self, arr: List[str]) -> List[str]:
        def check(i: int, sub: str) -> bool:
            for j, s in enumerate(arr):
                if j != i and sub in s:
                    return False
            return True

        ans = []
        for i, s in enumerate(arr):
            m = len(s)
            res = ""
            for size in range(1, m + 1):
                for j in range(size, m + 1):
                    t = s[j - size: j]
                    if (not res or t < res) and check(i, t):
                        res = t
                if res: break
            ans.append(res)
        return ans
''',
    call='Solution().shortestSubstrings(["cab", "ad", "bad", "c"])',
    expect=['ab', '', 'ba', ''],
    views=[
        dict(type='array', var='arr', label='arr（蓝 = 正在求答案的字符串 arr[i]）', cell=150, pointers={'i': 'blue'}, h=170,
             color=lambda S, k, v: 'blue' if S.get('_inner', {}).get('i', S.get('i')) == k else None),
        dict(type='string', var='arr[i]', label='当前字符串 arr[i]', cell=84, h=150,
             color=lambda S, k, v: 'green' if S['_line'] >= 15 and 'size' in S and S['j'] - S['size'] <= k < S['j'] else None),
        dict(type='text', fn=_top, size=26),
        dict(type='text', fn=_ans, size=26),
    ],
    watch=[('i', 'i', 'blue'), ('size', 'size', 'pink'), ('t', 't', 'yellow'), ('res', 'res', 'green')],
    captions={
        'for i, s in enumerate(arr)': lambda S, B, r: ('每个 `arr[i]` 都处理完了' if B.get('i') == S.i and 's' in B and B.get('s') == S.s
                                               else f'分别计算每个 `answer[i]`：现在处理 `arr[{S.i}] = "{S.s}"`'),
        'm = len(s)': '`s` 的长度 `m = {m}`，子串长度最多枚举到 m',
        'res = ""': '`res` 先置空，表示还没找到非公共子串',
        'for size in range': '从小到大枚举长度 `size = {size}`：越短越优先',
        'for j in range(size': '枚举右端点 `j = {j}`，子串就是 `s[{j - size}:{j}]`',
        't = s[': '取出长为 {size} 的子串 `t = "{t}"`',
        'if (not res or t < res)': lambda S, B, r: (
            f'`res` 为空或 `"{S.t}" < "{S.res}"`（字典序更小）→ ==值得检查==，调用 check' if (not S.res or S.t < S.res)
            else f'`"{S.t}" >= "{S.res}"`，字典序不更小，==不用再 check=='),
        'if j != i and sub in s': lambda S, B, r: (
            f'`j == i`，是自己，跳过' if S.j == S.i
            else (f'`"{S.sub}" in "{S.s}"` → ==出现在别人那里==，不是非公共子串' if S.sub in S.s
                  else f'`"{S.sub}"` 不在 `"{S.s}"` 里，继续看下一个')),
        'return False': 'sub 出现在别的字符串里 → `check` 返回 False',
        'return True': '所有其它字符串都没有它 → `check` 返回 True，==是非公共子串==',
        'res = t': '更新 `res = "{res}"`（同长度里字典序最小）',
        'if res: break': lambda S, B, r: (f'这个长度已找到 `"{S.res}"`，更长的不用看了 → ==break==' if S.res
                                          else '这一长度没找到，`size` 加 1 再试'),
        'ans.append(res)': '`answer[{i}] = "{res}"`' ,
        'return ans': '返回 `{ans}`',
    },
    cards=dict(
        one_liner='长度从小到大枚举，同长度取字典序最小',
        complexity='时间 `O(n^2 m^4)`，空间 `O(m)`',
        problem=['给 `arr`，对每个字符串求：不是别的字符串子串的、==最短==的子串',
                 '同样短取字典序最小，没有就返回空串',
                 '示例：`["cab","ad","bad","c"]` → `["ab","","ba",""]`'],
        quote='对于 arr[i]，从小到大枚举长度 size，然后枚举 arr[i] 的长为 size 的所有子串 t，判断 t 是否在其它字符串中，如果不在，就更新 answer[i] 的最小值。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`size` 从小到大：一旦某个长度有解，更长的不可能更优 → `break`',
              '同一长度里用 `t < res` 保留字典序最小',
              '`check(i, t)` 用 `in` 判断子串，跳过自己 `j != i`'],
        summary=['时间 `O(n^2 m^4)`，`n ≤ 100`、`m ≤ 20`，暴力足够',
                 '易错：必须排除自己（`j != i`），且 `if res: break` 在 size 循环里',
                 '先判 `t < res` 再 check，能少做很多次子串查找',
                 '线性做法见后缀数组 / 后缀自动机（灵神注）'],
    ),
)
