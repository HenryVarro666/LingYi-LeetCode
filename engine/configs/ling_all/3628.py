def _idx(S):
    if 'b' not in S or 'lct' not in S:
        return None
    s = S['s']
    p = S['l'] + S['c'] + s.count('T') - S['t']
    i = p - 1 if S['_line'] in (7, 10, 14, 15) else p
    return i if 0 <= i < len(s) else None


def _color(S, i, v):
    cur = _idx(S)
    if cur is None:
        return None
    return 'blue' if i == cur else None


def _dim(S, i, v):
    cur = _idx(S)
    return cur is not None and i < cur


def _formula(S):
    if 'lct' not in S:
        return '三个计数：`l`=L 的个数，`lc`=LC 子序列数，`lct`=LCT 子序列数'
    return (f"原有 `LCT` = =={S['lct']}==；插入后最多再多：插 L → `ct`={S['ct']}，"
            f"插 T → `lc`={S['lc']}，插 C → `lt`={S['lt']}")


CONFIG = dict(
    num=3628, title='插入一个字母的最大子序列数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 前后缀分解',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1754'],
    code='''
class Solution:
    def numOfSubsequences(self, s: str) -> int:
        t = s.count('T')
        l = lc = lct = c = ct = lt = 0
        for b in s:
            if b == 'L':
                l += 1
            elif b == 'C':
                lc += l
                c += 1
            elif b == 'T':
                lct += lc
                ct += c
                t -= 1
            lt = max(lt, l * t)
        return lct + max(ct, lc, lt)
''',
    call="Solution().numOfSubsequences('LCLLTT')",
    expect=8,
    skip=['l = lc = lct'],
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符，灰 = 已遍历）', h=190, cell=96, color=_color, dim=_dim),
        dict(type='text', fn=_formula, size=26, h=80),
        dict(type='text', fn=lambda S: (f"插 C 的位置在当前字符之后：左边 `{S['l']}` 个 L × 右边 `{S['t']}` 个 T = =={S['l'] * S['t']}==" if 'lt' in S and 'b' in S else ''), size=26, h=60),
    ],
    watch=[('l', 'l', 'blue'), ('c', 'c', 'cyan'), ('t（右边剩余 T）', 't', 'pink'), ('lc', 'lc', 'yellow'),
           ('ct', 'ct', 'yellow'), ('lct', 'lct', 'green'), ('lt', 'lt', 'orange')],
    captions={
        't = s.count': '`t` = s 中 T 的个数 = =={t}==；每遇到一个 T 减 1，所以 `t` 始终是「当前字符右边还剩几个 T」',
        'for b in s': lambda S, B, r: (f"取第 `{_idx(S) + 1}` 个字符：`b = '{S.b}'`" if _idx(S) is not None else '字符都遍历完了'),
        "if b == 'L'": lambda S, B, r: f"`b = '{S.b}'`：是 L 吗？" + ('是' if S.b == 'L' else '否，看下一个分支'),
        "elif b == 'C'": lambda S, B, r: f"`b = '{S.b}'`：是 C 吗？" + ('是' if S.b == 'C' else '否，看下一个分支'),
        "elif b == 'T'": lambda S, B, r: f"`b = '{S.b}'`：是 T 吗？" + ('是' if S.b == 'T' else '否，这个字符不影响计数'),
        'l += 1': '遇到 L：`l` → =={l}==，后面的 C 都能和它组成 LC',
        'lc += l': '遇到 C：前面每个 L 都能和它组成 LC → `lc += l`：`{B.lc} + {l}` = =={lc}==',
        'c += 1': '`c` → {c}：统计 C 的个数，用来算 `CT`（插 L 时用）',
        'lct += lc': '遇到 T：前面每个 LC 都能补上它 → `lct += lc`：`{B.lct} + {lc}` = =={lct}==',
        'ct += c': '同理 `ct += c`（CT 子序列数）：`{B.ct} + {c}` = {ct}',
        't -= 1': '这个 T 已经遍历到，右边少一个：`t` → =={t}==',
        'lt = max': '插 C 到当前字符后：左边 `{l}` 个 L × 右边 `{t}` 个 T = {l * t}，`lt` 取最大 → =={lt}==',
        'return': '`lct + max(ct, lc, lt)` = `{lct} + max({ct}, {lc}, {lt})` = =={ret}==：插 L / 插 T / 插 C 取最优',
    },
    cards=dict(
        one_liner='原有 LCT 个数 + 插入一个字母的最大增量',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['大写字母串 `s`，==最多插入一个==大写字母，使 `"LCT"` 子序列个数最大',
                 '示例：`s = "LCCT"` → `4`（开头插 `L`）',
                 '本视频：`s = "LCLLTT"` → `8`'],
        quote='先计算不插入字母时的 LCT 子序列个数，然后加上插入字母额外产生的 LCT 子序列个数。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['插 `L`：插最左边最优，增量 = `s` 里的 `CT` 个数 `ct`',
              '插 `T`：插最右边最优，增量 = `s` 里的 `LC` 个数 `lc`',
              '插 `C`：枚举位置，增量 = 左边 `L` 个数 × 右边 `T` 个数',
              '方法二：把三个子序列计数合并到一次循环（状态机 DP），`t` 递减表示右边剩余 T'],
        summary=['时间 `O(n)`，空间 `O(1)`；一遍循环同时维护 `l, lc, lct, c, ct` 和 `lt`',
                 '易错：`t` 是==右边==剩余的 T，所以遇到 T 要先减 1 再算 `lt`',
                 '易错：答案是 `lct + max(...)`，别忘了原有的 LCT',
                 '方法一：先套 115 题「不同的子序列」算 LCT/CT/LC，再单独算插 C；方法二是它的合并写法',
                 '同类题：2222. 选择建筑的方案数'],
    ),
)
