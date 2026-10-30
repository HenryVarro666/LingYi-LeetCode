def _idx(S):
    L, s = S.get('L'), S.get('s')
    if L is None or 'c' not in S or 'LCT' not in S:
        return None
    ln = S['_line']
    if 'T' not in S:                       # 第一趟：从左往右
        i = len(L) - 1 - (1 if ln in (9, 15) else 0)
    else:                                  # 第二趟：从右往左
        if ln < 21:
            return None
        i = len(L) if ln == 28 else len(L) - 1
    return i if 0 <= i < len(s) else None


def _pass2(S):
    return 'T' in S and S.get('_line', 0) >= 21


def _color(S, i, v):
    cur = _idx(S)
    return 'blue' if cur is not None and i == cur else None


def _dim(S, i, v):
    cur = _idx(S)
    if cur is None:
        return False
    return i > cur if _pass2(S) else i < cur


def _info(S):
    if 'LCT' not in S:
        return ''
    if 'T' in S:
        return f"第二趟（从右往左）：右边 `T` = {S['T']}，`CT` = {S['CT']}，插 C 的最佳增量 `best` = =={S['best']}=="
    return f"第一趟（从左往右）：`LC` = {S['LC']}，`LCT` = =={S['LCT']}==；`L` 列表记下每个位置左边 L 的个数"


CONFIG = dict(
    num=3628, title='插入一个字母的最大子序列数', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='前后缀 DP · 分三种插入',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1754'],
    code='''
class Solution(object):
    def numOfSubsequences(self, s):
        
        L = [0]
        LC = 0
        LCT = 0
        for c in s:
            if c == 'L':
                L.append(L[-1] + 1)
            else:
                if c == 'C':
                    LC += L[-1]
                elif c == 'T':
                    LCT += LC
                L.append(L[-1])
        
        L.pop()
        T = 0
        CT = 0
        best = 0
        for c in s[::-1]:
            if c == 'T':
                T += 1
            elif c == 'C':
                CT += T
            
            best = max(best, L[-1] * T)
            L.pop()
        
        return max(best, LC, CT) + LCT
''',
    call="Solution().numOfSubsequences('LCLLTT')",
    expect=8,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字符，灰 = 这一趟已处理）', h=180, cell=90, color=_color, dim=_dim),
        dict(type='text', fn=_info, size=24, h=70),
        dict(type='array', var='L', label='L 列表：每个位置左边 L 的个数', h=180, cell=70),
    ],
    watch=[('LC', 'LC', 'yellow'), ('LCT', 'LCT', 'green'), ('T', 'T', 'pink'), ('CT', 'CT', 'yellow'), ('best', 'best', 'orange')],
    captions={
        4: '`L[i]`：`s[:i]` 里 L 的个数，先放 `0`',
        5: '`LC`：已扫过部分的 LC 子序列数',
        6: '`LCT`：已扫过部分的 LCT 子序列数',
        7: lambda S, B, r: (f"取第 `{_idx(S) + 1}` 个字符 `c = '{S.c}'`" if _idx(S) is not None else '第一趟扫完'),
        8: lambda S, B, r: f"`c = '{S.c}'`：是 L 吗？" + ('是' if S.c == 'L' else '否'),
        9: '遇到 L：左边 L 的个数 +1 → `{L[-1]}`，记进 `L`',
        11: lambda S, B, r: f"`c = '{S.c}'`：是 C 吗？" + ('是' if S.c == 'C' else '否'),
        12: '遇到 C：左边 `{L[-1]}` 个 L 都能配它 → `LC` += {L[-1]} → =={LC}==',
        13: lambda S, B, r: f"`c = '{S.c}'`：是 T 吗？" + ('是' if S.c == 'T' else '否，不影响 LC/LCT'),
        14: '遇到 T：此前每个 LC 都能补上它 → `LCT` += {B.LC} → =={LCT}==',
        15: '不是 L：左边 L 的个数不变，也记进 `L` → `{L[-1]}`',
        17: '`L` 最后一项是整串的 L 总数，用不上；弹掉后 `L[i]` = `s[:i]` 里 L 的个数',
        18: '第二趟从右往左：`T` = 当前位置右边（含自己）T 的个数',
        19: '`CT` = 后缀里的 CT 子序列数（插 L 时的增量）',
        20: '`best` = 插 C 的最大增量',
        21: lambda S, B, r: (f"从右取字符 `c = '{S.c}'`（原下标 `{_idx(S)}`）" if _idx(S) is not None else '第二趟扫完'),
        22: lambda S, B, r: f"`c = '{S.c}'`：是 T 吗？" + ('是' if S.c == 'T' else '否'),
        23: '遇到 T：右边 T 的个数 → `T` = =={T}==',
        24: lambda S, B, r: f"`c = '{S.c}'`：是 C 吗？" + ('是' if S.c == 'C' else '否'),
        25: '遇到 C：它右边有 `{T}` 个 T → `CT` += {T} → =={CT}==',
        27: '在这个位置前插 C：左边 `{L[-1]}` 个 L × 右边 `{T}` 个 T = {L[-1] * T}，`best` → =={best}==',
        28: '这个位置处理完，弹掉 `L` 末项，对齐下一个位置',
        30: '`max(best, LC, CT) + LCT` = `max({best}, {LC}, {CT}) + {LCT}` = =={ret}==',
    },
    cards=dict(
        one_liner='插 L 放最前、插 T 放最后、插 C 放中间，再加原有 LCT',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['大写字母串 `s`，==最多插入一个==大写字母，使 `"LCT"` 子序列个数最大',
                 '示例：`s = "LCCT"` → `4`',
                 '本视频：`s = "LCLLTT"` → `8`'],
        quote='如果插入的是L，那么插入到头部是最优的，新增的LCT序列的数目就是原始字符串中CT序列的数目；……对于C，则应该插入到中间某处。',
        quote_src='—— yiduobo 题解原文',
        idea=['`L` 数组记每个位置左边 L 的个数，用变量迭代算 `LC`、`LCT`',
              '从后往前再扫一趟：算右边 `T` 的个数和 `CT`',
              '每个位置顺手算「插 C」的增量 `L × T`，取最大 `best`',
              '答案 = `max(best, LC, CT) + LCT`'],
        summary=['时间 `O(n)`，空间 `O(n)`（保留了 `L` 数组，灵神写法可压到 `O(1)`）',
                 '易错：第二趟里 `best` 先算、`L.pop()` 后做，位置才对得上',
                 '易错：插 L 增量是 `CT`，插 T 增量是 `LC`，别搞反',
                 '原文为 Python 2 风格，本题代码无需改动即可在 Python 3 运行'],
    ),
)
