CONFIG = dict(
    num=1087, title='花括号展开', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='回溯：逐位选字符',
    tags=['常用数据结构', '回溯'],
    code='''
class Solution(object):
    def expand(self, s):

        res = []

        def dfs(level, now):
            if level == len(s):
                res.append(''.join(now))
                return

            if s[level] == '{':
                p = level + 1
                while s[p] != '}':
                    p += 1
                
                char_list = sorted(s[level + 1 : p].split(','))
                for char in char_list:
                    now.append(char)
                    dfs(p + 1, now)
                    now.pop()
            else:
                now.append(s[level])
                dfs(level + 1, now)
                now.pop()

        dfs(0, [])
        return res
''',
    call='Solution().expand("{b,a}c{d,e}")',
    expect=['acd', 'ace', 'bcd', 'bce'],
    views=[
        dict(type='string', var='s', label='s（蓝箭头 = 当前处理的位置 level）', cell=60, h=170, pointers={'level': 'blue'},
             dim=lambda S, i, v: i < S['_inner'].get('level', 0)),
        dict(type='stack', var='now', label='now（当前这条路径已选的字符）', h=110, font=30),
        dict(type='calls', h=200),
        dict(type='stack', var='res', label='res（已展开的单词）', h=100, font=28),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'), ('p', lambda S: S['_inner'].get('p'), 'pink'),
           ('char', lambda S: S['_inner'].get('char'), 'yellow'), ('now', 'now', 'green')],
    skip=['res = []', 'p += 1', 'while s[p] != '],
    captions={
        'dfs(0, [])': '从 `level = 0` 开始，`now` 为空：逐位决定选哪个字符',
        'if level == len(s)': lambda S, B, r: ('`level` 走到末尾 → ==每一位都选好了==' if S.level == len(S.s)
                                              else f'`level = {S.level} < {len(S.s)}`：还要决定第 `{S.level}` 位'),
        "res.append(''.join(now))": '拼成单词 `{res[-1]}` 放进 `res`',
        '                return': '这条路径结束，回到上一层',
        "if s[level] == '{'": lambda S, B, r: (f'`s[{S.level}] = "{{"` → 这一位有==多个候选字符==，需要逐个尝试'
                                               if S.s[S.level] == '{' else f'`s[{S.level}] = "{S.s[S.level]}"` 不是花括号 → 这一位只能选它自己'),
        'char_list = sorted': '花括号里的候选 `{s[level+1:p]}` 按字典序排序 → ==`{char_list}`==（结果要求有序）',
        'for char in char_list': lambda S, B, r: ('候选都试完了 → 这一层结束，回到上一层' if 'char' in B['_inner'] and B['_inner']['char'] == S['_inner'].get('char')
                                                   else f'尝试第 `{S.char_list.index(S.char) + 1}` 个候选 `{S.char}`'),
        'now.append(char)': '选 `{char}` 放进路径：`now = {now}`',
        'dfs(p + 1, now)': '递归：跳过 `}`，从 `level = p + 1` 处理下一位',
        'now.pop()': '==回溯==：撤销刚才的选择 → `now = {now}`',
        'now.append(s[level])': '普通字符 `{s[level]}` 直接选上：`now = {now}`',
        'dfs(level + 1, now)': '递归处理下一位 `level = {B.level + 1}`',
        'return res': '一共展开出 `{len(ret)}` 个单词：`{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='每一位试遍所有候选字符：典型回溯',
        complexity='时间 `O(k^m · n)`，空间 `O(n)`（k 候选数，m 花括号数）',
        problem=['`s` 中 `{a,b}` 表示该位可选 `a` 或 `b`，普通字母只有一种选择',
                 '返回所有可能的单词，按字典序排列',
                 '本视频：`"{b,a}c{d,e}"` → `["acd","ace","bcd","bce"]`'],
        quote='为了能够尝试每一位上各种各样的组合，本题应该使用回溯法来进行处理。',
        quote_src='—— yiduobo 题解原文',
        idea=['`level` 指向 `s` 中当前处理的位置，`now` 是已选字符',
              '遇 `{`：找到 `}`，把里面的候选排序，逐个选、递归、再撤销',
              '遇普通字符：只能选它；`level` 到末尾就拼出一个单词'],
        result='4 个单词全部展开 ✓',
        summary=['时间 `O(k^m · n)`，空间 `O(n)`，返回值不计',
                 '先对候选字符 `sorted`，深搜的出口顺序就是字典序，不用再整体排序',
                 '易错：递归 `dfs(p + 1, now)` 要跳过 `}`；选完要 `now.pop()` 恢复',
                 '原文为 Python 2 写法，本题代码无需改动，直接可在 Python 3 运行',
                 '同类题：17 电话号码的字母组合（每位候选集合不同）'],
    ),
)
