S0 = 'aAbB'


def _cnts(S):
    cl = S.get('cnt_list')
    if not isinstance(cl, list) or len(cl) != 26:
        return {}
    return {chr(97 + i): v for i, v in enumerate(cl) if v[0] or v[1]}


def _top(S):
    if 'target_cnt' not in S:
        return '把 `A/a` 都映射到编号 0，`mapping_pos`：大写 → 0，小写 → 1'
    l, r, t = S['l'], S['r'], S['target_cnt']
    return (f"字符种数上限 =={t}==：窗口 `[{l}, {r}] = {S0[l:r + 1]!r}`，"
            f"char_cnt = `{S['char_cnt']}`，full_cnt = `{S['full_cnt']}`")


def _color(S, i, v):
    if 'target_cnt' not in S:
        return None
    if S.get('res_l') is not None and S['res_l'] <= i <= S['res_r'] and not (S['l'] <= i <= S['r']):
        return 'green'
    return None


def _shrink(S, B, ret):
    if S.l < S.r and S.char_cnt > S.target_cnt:
        return f'`char_cnt = {S.char_cnt} > {S.target_cnt}`：种数超了 → 左边界 l 右移'
    return f'`char_cnt = {S.char_cnt} ≤ {S.target_cnt}`：窗口种数合法'


def _in0(S, B, ret):
    c = S.s[S.r]
    if S.cnt_list[S.num][S.pos] == 0:
        return f"`{c!r}` 这种写法==第一次==进窗口"
    return f"`{c!r}` 已在窗口里，只加次数"


def _in1(S, B, ret):
    c = S.s[S.r]
    if S.cnt_list[S.num][1 - S.pos] == 0:
        return f"另一种大小写也没有 → `{c!r}` 是==新字符种类=="
    return f"另一种大小写已在窗口 → 这个字母==大小写凑齐了=="


def _out0(S, B, ret):
    c = S.s[S.l]
    if S.cnt_list[S.num][S.pos] == 1:
        return f"移出 `{c!r}` 后这种写法就没了"
    return f"窗口里还有别的 `{c!r}`，只减次数"


def _out1(S, B, ret):
    if S.cnt_list[S.num][1 - S.pos] == 0:
        return '另一种大小写也没有 → 少了一种字符'
    return '另一种大小写还在 → 不再是大小写齐全'


def _full(S, B, ret):
    if S.full_cnt == S.target_cnt:
        return f'`full_cnt == {S.target_cnt}`：窗口里每种字母都大小写齐全 → ==美好子串=='
    return f'`full_cnt = {S.full_cnt} ≠ {S.target_cnt}`：还有字母只有一种写法'


CONFIG = dict(
    num=1763, title='最长的美好子字符串', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='枚举字符种数 + 双指针',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def longestNiceSubstring(self, s):

        n = len(s)
        mapping_num = {}
        mapping_pos = {}
        for index in range(26):
            mapping_num[chr(index + 65)] = index
            mapping_num[chr(index + 97)] = index
            mapping_pos[chr(index + 65)] = 0
            mapping_pos[chr(index + 97)] = 1

        res_l = res_r = None
        max_len = 0

        for target_cnt in range(1, 26):
            l = r = 0
            cnt_list = [[0, 0] for _ in range(26)]
            char_cnt = 1
            full_cnt = 0
            num = mapping_num[s[r]]
            pos = mapping_pos[s[r]]
            cnt_list[num][pos] += 1

            while r + 1 < n:
                r += 1
                num = mapping_num[s[r]]
                pos = mapping_pos[s[r]]
                if cnt_list[num][pos] == 0:
                    if cnt_list[num][1 - pos] == 0:
                        char_cnt += 1
                    else:
                        full_cnt += 1
                cnt_list[num][pos] += 1

                while l < r and char_cnt > target_cnt:
                    num = mapping_num[s[l]]
                    pos = mapping_pos[s[l]]
                    if cnt_list[num][pos] == 1:
                        if cnt_list[num][1 - pos] == 0:
                            char_cnt -= 1
                        else:
                            full_cnt -= 1

                    cnt_list[num][pos] -= 1
                    l += 1

                if full_cnt == target_cnt:
                    if r - l + 1 > max_len:
                        max_len = r - l + 1
                        res_l, res_r = l, r

        if max_len == 0:
            return ""
        return s[res_l : res_r + 1]
''',
    call=f'Solution().longestNiceSubstring({S0!r})',
    expect='aAbB',
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='string', var='s', label='s（框 = 窗口 [l, r]，绿 = 当前最优答案）',
             pointers={'l': 'cyan', 'r': 'orange'}, window=('l', 'r'), color=_color, cell=120, h=280),
        dict(type='map', var=_cnts, label='cnt_list（每个字母的 [大写次数, 小写次数]）',
             fmt=lambda k, v: f'{k}: [{v[0]}, {v[1]}]', h=150, font=32),
    ],
    watch=[('target_cnt', 'target_cnt', 'purple'), ('l', 'l', 'cyan'), ('r', 'r', 'orange'),
           ('char_cnt', 'char_cnt', 'blue'), ('full_cnt', 'full_cnt', 'pink'), ('max_len', 'max_len', 'green')],
    skip=['mapping_num = {}', 'mapping_pos = {}', 'for index in range(26)', 'mapping_num[chr', 'mapping_pos[chr',
          'num = mapping_num', 'pos = mapping_pos', 'char_cnt = 1', 'full_cnt = 0', 'cnt_list = [[0, 0]', 'cnt_list[num][pos] -= 1', 'cnt_list[num][pos] += 1'],
    captions={
        'n = len(s)': '`n = {n}`；先建映射：字母 → 编号 0~25，大写 → 0、小写 → 1',
        'res_l = res_r = None': '`res_l, res_r` 记录答案区间',
        'max_len = 0': '`max_len = 0`',
        'for target_cnt in range': lambda S, B, r: (f'枚举答案中==字符种数== `target_cnt = {S.target_cnt}`'
                                                    if 'target_cnt' not in B or B.target_cnt != S.target_cnt else '枚举结束'),
        'l = r = 0': '`l = r = 0`，清空计数，`char_cnt = 1`、`full_cnt = 0`',
        'while r + 1 < n': lambda S, B, r: ('`r` 还能右移' if S.r + 1 < S.n else '`r` 到末尾，这一轮结束'),
        'r += 1': '`r` → {r}，`{s[r]!r}` 进窗口',
        'if cnt_list[num][pos] == 0': _in0,
        30: _in1,
        40: _out1,
        'char_cnt += 1': '`char_cnt` → {char_cnt}',
        'full_cnt += 1': '`full_cnt` → {full_cnt}',
        'while l < r and char_cnt > target_cnt': _shrink,
        'if cnt_list[num][pos] == 1': _out0,
        'char_cnt -= 1': '`char_cnt` → {char_cnt}',
        'full_cnt -= 1': '`full_cnt` → {full_cnt}',
        'l += 1': "`{s[l - 1]!r}` 次数减一，`l` → {l}",
        'if full_cnt == target_cnt': _full,
        'if r - l + 1 > max_len': lambda S, B, r: (f'长度 `{S.r - S.l + 1}` > `max_len = {S.max_len}` → 更新'
                                                   if S.r - S.l + 1 > S.max_len else f'长度 `{S.r - S.l + 1}` 不比 `{S.max_len}` 长，不更新'),
        'max_len = r - l + 1': '`max_len` → =={max_len}==',
        'res_l, res_r = l, r': '答案区间 `[{res_l}, {res_r}]`',
        'if max_len == 0': '`max_len = {max_len}`，有美好子串',
        'return s[res_l': '答案：=={ret!r}==',
    },
    max_steps=85,
    cards=dict(
        one_liner='限定字符种数，滑窗里种数齐全且大小写齐全就是美好子串',
        complexity='时间 `O(26 · n)`，空间 `O(26)`',
        problem=['字符串里每种字母都==同时出现大写和小写==，就是美好的',
                 '求 `s` 最长的美好子串；多个时取最早出现的，没有返回空串',
                 '示例：`"YazaAay"` → `"aAa"`；本视频 `"aAbB"` → `"aAbB"`'],
        quote='枚举答案中字符种类的数量，然后利用这个数量限制使用双指针来求解。……当char_cnt合法后，判断当前的full_cnt是否==恰好等于target_cnt==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`char_cnt`：窗口里字母种数；`full_cnt`：大小写都有的种数',
              '固定种数上限 `target_cnt`，r 右扩，种数超了就移 l',
              '`full_cnt == target_cnt` 说明每种字母都大小写齐全'],
        summary=['时间 `O(26 · n)`：枚举 25 种上限，每轮双指针 `O(n)`',
                 '`cnt_list[num][pos]`：pos 0 是大写、1 是小写，`1 − pos` 取另一种写法',
                 '只在次数 0↔1 变化时才改 `char_cnt / full_cnt`',
                 '用 `>` 更新答案，保证长度相同时取最早出现的',
                 '原文为 Python 2 风格，代码无需改动；暴力枚举所有子串也能过（n ≤ 100）'],
    ),
)
