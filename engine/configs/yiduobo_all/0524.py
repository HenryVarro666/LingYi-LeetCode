def _idx(s, t, k):
    out, p = [], 0
    for i, ch in enumerate(s):
        if p < k and ch == t[p]:
            out.append(i)
            p += 1
    return out


def _now_text(S):
    if 'now' not in S:
        return ''
    n, p = S['now'], S.get('pos', 0)
    c = S.get('char')
    head = f"当前单词 `{n}`，已匹配 =={p}== 个字母，目前最优 `{S.get('res', '')!r}`"
    if c is not None and p < len(n) and S['_line'] >= 9:
        return head + f"；扫到 `{c}`，等待 `{n[p]}`"
    return head


def _s_color(S, i, v):
    if 'now' not in S or 'pos' not in S:
        return None
    return 'green' if i in _idx(S['s'], S['now'], S['pos']) else None


def _skip(S, B, ret):
    now, res = S.now, S.res
    if len(now) < len(res):
        return f"`{now}` 比 `{res}` 短 → 不可能更优，==直接跳过=="
    if len(now) == len(res) and now > res:
        return f"等长但 `{now}` 字典序比 `{res}` 大 → ==跳过=="
    return f"`{now}` 有可能更优（更长，或等长且字典序更小）→ 才去检查它是不是 s 的子序列"


CONFIG = dict(
    num=524, title='通过删除字母匹配到字典里最长单词', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='逐词判断子序列 + 剪枝',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def findLongestWord(self, s, d):

        res = ''
        for now in d:
            if len(now) < len(res) or (len(now) == len(res) and now > res):
                continue
            pos = 0
            for char in s:
                if char == now[pos]:
                    pos += 1
                    if pos == len(now):
                        res = now
                        break

        return res
''',
    call="Solution().findLongestWord('abpcplea', ['ale', 'apple', 'monkey', 'plea'])",
    expect='apple',
    views=[
        dict(type='text', fn=_now_text, h=60),
        dict(type='string', var='s', color=_s_color, label='s（绿 = 已被当前单词贪心匹配的字母）', h=170),
        dict(type='string', var='now', pointers={'pos': 'blue'}, label='当前单词 now（箭头 = 下一个要匹配的位置 pos）', h=170),
        dict(type='string', var='res', label='res（目前最优）', h=130),
    ],
    watch=['now', 'pos', ('res', 'res', 'green')],
    captions={
        "res = ''": '`res` 保存目前最长（同长取字典序最小）的答案，初始为空',
        'for now in d': '枚举字典里的每个单词：`now = {now!r}`',
        'if len(now) < len(res)': _skip,
        'pos = 0': '`pos = 0`：从 `now` 的第一个字母开始匹配',
        'for char in s': '一趟扫描 `s`，能匹配就尽量匹配（贪心）',
        'if char == now[pos]': lambda S, B, r: (f"`{S.char}` == `now[{S.pos}] = {S.now[S.pos]}` → ==匹配上了==" if S.char == S.now[S.pos] else f"`{S.char}` ≠ `now[{S.pos}] = {S.now[S.pos]}` → 这个字母相当于被删掉"),
        'pos += 1': '匹配成功，`pos` → {pos}，去等下一个字母',
        'if pos == len(now)': lambda S, B, r: (f'`pos = {S.pos} == len(now)`：`now` 整个是 s 的子序列' if S.pos == len(S.now) else f'`pos = {S.pos} < {len(S.now)}`：还没匹配完，继续扫'),
        'res = now': '`res = {res!r}`：更长（或同长更小），==更新答案==',
        'break': '已经匹配完，不用再扫 `s`，换下一个单词',
        'return res': '返回 `{res!r}`',
    },
    cards=dict(
        one_liner='删字母凑单词，就是判断单词是不是 s 的子序列',
        complexity='时间 `O(d·n)`（d 个单词，n = len(s)），空间 `O(1)`',
        problem=['给字符串 `s` 和字典 `d`，通过==删除 s 的若干字母==得到字典里的单词',
                 '返回能得到的==最长==单词，同长取==字典序最小==，得不到返回空串',
                 '示例：`s = abpcplea`，`d = [ale, apple, monkey, plea]` → `apple`'],
        quote='题目要求删除某些字母匹配字典里的单词，实际上就是检测d里的单词是否是s的子序列。',
        quote_src='—— yiduobo 题解原文',
        idea=['数据范围只有 1000，直接==枚举 d 里每个单词==，用贪心一趟扫描判断子序列',
              '小优化：比当前答案短，或同长但字典序更大的单词，==连检查都不用==',
              '检查通过就更新 `res`；`res` 始终是最长、字典序最小的那个'],
        summary=['时间 `O(d·n)`，空间 `O(1)`',
                 '剪枝条件里：同长时 `now > res` 才跳过，保证字典序小的留下',
                 '`now[pos]` 在 `pos == len(now)` 时就 break，所以不会越界',
                 '原文为 Python 2 风格，本题无需改动，直接可在 Python 3 运行',
                 '同类题：392 判断子序列、2486、2825'],
    ),
)
