CONFIG = dict(
    num=267, title='回文排列 II', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='配对计数 + 排列型回溯枚举前半',
    tags=['灵神题单·链表树与回溯'],
    code='''
class Solution(object):
    def generatePalindromes(self, s):

        char_dict = {}
        char_set = set()

        for char in s:
            if char in char_set:
                char_dict[char] = char_dict.get(char, 0) + 1
                char_set.remove(char)
            else:
                char_set.add(char)
        
        if len(char_set) >= 2:
            return []
        
        if len(char_set) == 1:
            mid = list(char_set)[0]
        else:
            mid = ''
        
        res = []
        
        def dfs(level, now, char_dict, res):
            if level == len(s) // 2:
                res.append('')
                for char in now:
                    res[-1] += char
                res[-1] += mid
                for char in now[::-1]:
                    res[-1] += char
                return
            
            for char in char_dict:
                if char_dict[char] > 0:
                    char_dict[char] -= 1
                    now.append(char)
                    dfs(level + 1, now, char_dict, res)
                    now.pop()
                    char_dict[char] += 1
        
        dfs(0, [], char_dict, res)
        return res
''',
    call='Solution().generatePalindromes("aabbc")',
    expect=['abcba', 'bacab'],
    views=[
        dict(type='string', var='s', label='s', cell=60, h=110),
        dict(type='map', var='char_dict', label='char_dict（每个字符可用的“对数”）', h=120, fmt=lambda k, v: f'{k}: {v} 对'),
        dict(type='array', var='now', label='now（回文的前半部分）', cell=60, h=120),
        dict(type='calls', h=170, hide=('char_dict', 'res', 'now')),
        dict(type='stack', var='res', label='res', h=100),
    ],
    watch=[('char_set', 'char_set', 'yellow'), ('mid', 'mid', 'cyan'), ('level', lambda S: S['_inner'].get('level'), 'blue')],
    skip=['res = []', 'char_dict = {}', 'char_set = set()', 'for char in now'],
    captions={
        'if char in char_set': lambda S, B, ret: (
            f"`'{S.char}'` 已在 `char_set` 里 → 凑成一对" if S.char in B.char_set else f"`'{S.char}'` 不在 `char_set` 里 → 先记为落单"),
        'char_dict[char] = char_dict.get': '凑成一对：`char_dict[{char!r}]` 加 1 → {char_dict[char]}',
        'char_set.remove': '这个字符配对成功，从落单集合 `char_set` 里移除',
        'char_set.add': '先放进 `char_set`：等下一个相同字符来配对',
        'if len(char_set) >= 2': lambda S, B, ret: (
            f'落单字符有 `{len(S.char_set)}` 个，>= 2 → ==不可能==组成回文，返回空' if len(S.char_set) >= 2
            else f'落单字符 `{len(S.char_set)}` 个（<= 1）→ 可以组成回文'),
        'mid = list': '恰好一个落单字符 `{mid!r}`：它只能放在回文的==正中间==',
        'mid = ': '没有落单字符，中心为空串',
        'if level == len(s)': lambda S, B, ret: (
            f'`level = {S.level} == len(s)//2`：前半部分填满了 → 拼成回文' if S.level == len(S.s) // 2
            else f'`level = {S.level} < {len(S.s) // 2}`：前半部分还没填满，继续枚举下一位'),
        'res.append': '先在 `res` 里开一个空串，下面往它后面拼',
        'res[-1] += char': '拼上 `{char!r}` → `{res[-1]!r}`（前半 → 中心 → 反转的前半）',
        'res[-1] += mid': '再拼中心字符 `{mid!r}` → `{res[-1]!r}`',
        '                return': '拼好一个回文，回到上一层继续枚举',
        'for char in char_dict': '枚举这一位放哪个字符',
        'if char_dict[char] > 0': lambda S, B, ret: (
            f"`char_dict['{S.char}'] = {S.char_dict[S.char]} > 0` → 还有对可用，可以放" if S.char_dict[S.char] > 0
            else f"`char_dict['{S.char}'] = 0` → 这个字符的对用完了，跳过"),
        'char_dict[char] -= 1': '用掉一对：`char_dict[{char!r}]` → {char_dict[char]}',
        'now.append': '`{char!r}` 放进前半部分 → `{now}`',
        'dfs(level + 1': '递归填下一位',
        'now.pop()': '回溯：撤销这一位 `{B.now[-1]!r}`',
        'char_dict[char] += 1': '恢复现场：把这一对还回去 → {char_dict[char]}',
        'dfs(0, [], char_dict, res)': '从第 0 位开始枚举前半部分',
        'return res': '共 `{len(ret)}` 个回文排列：`{ret}`',
    },
    max_steps=90,
    cards=dict(
        one_liner='先判能否成回文，再只排列前半，镜像拼出整串',
        complexity='时间约 `O((n/2)!·n)`，空间 `O(n)`',
        problem=['给定字符串 `s`，返回它==重新排列后==所有不重复的回文串（任意顺序）',
                 '示例：`"aabb"` → `["abba","baab"]`；`"abc"` → `[]`',
                 '本视频：`"aabbc"` → `["abcba","bacab"]`'],
        quote='如果可以形成回文排列，那么在这里就只需找出所有可行排列的前半部分，也就是找出所有成对出现字符的所有可行排列。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `char_set` 配对：遇到第二个相同字符就==凑成一对==，对数记在 `char_dict`',
              '最后 `char_set` 里剩 2 个以上落单字符 → 不可能；剩 1 个就是中心 `mid`',
              '前半部分用回溯枚举（按“对”分配，天然不重复），再拼 前半 + mid + 反转前半'],
        result='找到 2 个回文排列 ✓',
        summary=['时间约 `O((n/2)!·n)`，空间 `O(n)`（不计返回值）',
                 '枚举的是 `char_dict` 的键，每个字符的对数用完才跳过，所以结果==不会重复==',
                 '长度为奇数时别忘了中心字符 `mid`，拼接顺序：前半 + mid + 反转前半',
                 '原文为 Python 2 写法，`len(s) / 2` 已改为 `len(s) // 2`'],
    ),
)
