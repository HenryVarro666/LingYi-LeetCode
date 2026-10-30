def _keys(S):
    lv = S['level']
    if lv < len(S['digits']):
        d = S['digits'][lv]
        letters = ''.join(S['char_list'][int(d)])
        return f"第 `{lv}` 位按键 `{d}` → `char_list[{d}]` = `{letters}`" + (f"，当前 `char = '{S['char']}'`" if 'char' in S else '')
    return f"`level == len(digits)`：`now = '{S['now']}'` 已经是一种答案"


def _for(S, B, ret):
    d = S.digits[S.level]
    letters = ''.join(S.char_list[int(d)])
    if 'char' in S and S.char != B.get('char'):
        return f"第 `{S.level}` 位先选一种可能：`char = '{S.char}'`（候选 `{letters}`）"
    return f"按键 `{d}` 的 `{letters}` 都试过了 → 这一层做完，回到上一位重新选择"


CONFIG = dict(
    num=17, title='电话号码的字母组合', difficulty='Medium', category='回溯',
    author='yiduobo', technique='搜索回溯（字符串 now + 位数 level）',
    code='''
class Solution(object):
    def letterCombinations(self, digits):
        char_list = [[],
                     [],
                     ['a', 'b', 'c'],
                     ['d', 'e', 'f'],
                     ['g', 'h', 'i'],
                     ['j', 'k', 'l'],
                     ['m', 'n', 'o'],
                     ['p', 'q', 'r', 's'],
                     ['t', 'u', 'v'],
                     ['w', 'x', 'y', 'z']]

        res = []
        self.search(digits, '', 0, char_list, res)
        return res

    def search(self, digits, now, level, char_list, res):
        if level == len(digits):
            if now:
                res.append(now)
            return

        for char in char_list[int(digits[level])]:
            self.search(digits, now + char, level + 1, char_list, res)
''',
    call="Solution().letterCombinations('23')",
    expect=['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'],
    views=[
        dict(type='string', var='digits', label='digits（蓝 = 第 level 位）', cell=64, h=130,
             color=lambda S, i, v: 'blue' if i == S['level'] else None),
        dict(type='text', fn=lambda S: _keys(S) if 'level' in S else '', h=50, size=26),
        dict(type='string', var='now', label='now（这一层收到的字符串）', cell=64, h=130, min_slots=2),
        dict(type='calls', h=180),
        dict(type='stack', var='res', label='res', h=100),
    ],
    watch=[('level', 'level', 'blue'), ('now', 'now', 'yellow'), ('char', 'char', 'pink')],
    skip=['            return', '                     ['],
    captions={
        'char_list = [[]': lambda S, B, ret: (
            '字母表建好了：`char_list[2] = [a,b,c]`，`char_list[3] = [d,e,f]`，…' if 'char_list' in S else
            '`char_list[d]` 是数字 `d` 对应的字母表（`0`、`1` 没有字母）'),
        'res = []': '`res = []`：收集答案',
        "self.search(digits, '', 0": "从 `now = ''`、`level = 0` 开始搜索",
        'if level == len(digits)': lambda S, B, ret: (
            f'`level == len(digits)`（{S.level} == {len(S.digits)}）→ 位数到了，生成了一种答案'
            if S.level == len(S.digits) else
            f'`level = {S.level}`：还没到 `{len(S.digits)}` 位，继续做第 `{S.level}` 位'),
        'if now:': lambda S, B, ret: (
            (f"`if now:` 防止 digits 为空串时记录 `''`；这里 `now = '{S.now}'` 非空" if not S.res else f"`now = '{S.now}'` 非空")
            if S.now else '`now` 为空（digits 为空串）→ 不记录'),
        'res.append(now)': "记录答案 `'{now}'`，然后回去尝试其他情况",
        'for char in char_list': _for,
        'self.search(digits, now + char': lambda S, B, ret: (
            f"继续做下一位：传入 `now + char = '{S.now}'`" + ('，原来的 `now` ==不会被改动==' if len(S.res) < 2 else '')),
        'return res': '搜索结束，共 `{len(ret)}` 种组合',
    },
    max_steps=52,
    cards=dict(
        one_liner='每一位先选一种字母，做完后面再回来换一种',
        complexity='时间 `O(n·4^n)`，空间 `O(n)`（不计返回值）',
        problem=['给一个只含数字 `2-9` 的字符串，返回它在电话按键上能表示的所有字母组合',
                 '`2→abc  3→def  4→ghi  5→jkl  6→mno  7→pqrs  8→tuv  9→wxyz`',
                 "示例：`\"23\"` → `[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]`"],
        quote='对于每一位，==先选择一种可能的情况，然后继续做下一位==。当后面位的情况都做完之后，再反过来重新选择一种可能的情况，接着再做后面的位。',
        quote_src='—— yiduobo 题解',
        idea=['用字符串 `now` 记录中间情况，`level` 记录当前做到第几位',
              '`level == len(digits)` 说明生成了一种答案，记录下来',
              '传 `now + char` 生成==新字符串==，回来时 now 还是原样，不用手动撤销'],
        result='9 种组合全部生成 ✓（中间分支已快进）',
        after=[dict(heading='yiduobo 的另一种写法：生成式', lines=[
            '按位枚举 digits，从上一位的解生成这一位的解：',
            '`res = [\'\']`',
            '`for k in digits: res = [i + j for i in res for j in char_list[int(k)]]`',
            '和回溯本质一样，只是一层一层地（BFS 式）扩展'])],
        summary=['最多 `4^n` 个答案，每个字符串长 `n` → `O(n·4^n)`',
                 '`if now:` 保证 digits 为空时返回 `[]` 而不是 `[\'\']`',
                 '字符串不可变：传 `now + char` 天然完成「恢复现场」',
                 '原文为 Python 2 风格，仅删去 docstring，其余代码未改'],
    ),
)
