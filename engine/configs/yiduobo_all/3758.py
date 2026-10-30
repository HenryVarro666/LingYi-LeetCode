def _top(S):
    if 'p' not in S:
        return ''
    if 'w' in S and S['_line'] >= 17 and S['p'] < len(S['s']):
        w = S['w']
        return f"位置 `p = {S['p']}`：用单词 `{w}` 对比 `s[{S['p']}:{S['p'] + len(w)}] = \"{S['s'][S['p']:S['p'] + len(w)]}\"`"
    return f"位置 `p = {S['p']}`，已提取 `{''.join(S['res'])}`"


def _win(S):
    w = S.get('w')
    p = S.get('p', 0)
    if w is None or p >= len(S['s']):
        return None
    return p


CONFIG = dict(
    num=3758, title='将数字词转换为数字', difficulty='Medium', category='字符串',
    author='yiduobo', technique='哈希表 + 暴力匹配',
    tags=['灵神题单', '字符串', 'AC 自动机'],
    code='''
class Solution(object):
    def convertNumber(self, s):
        
        nums = {"one": "1",
                "two": "2",
                "three": "3",
                "four": "4",
                "five": "5",
                "six": "6",
                "seven": "7",
                "eight": "8",
                "nine": "9",
                "zero": "0"
        }

        res = []
        p = 0
        while p < len(s):
            for w, v in nums.items():
                if p + len(w) <= len(s) and s[p: p + len(w)] == w:
                    res.append(v)
                    p += len(w) - 1
                    break

            p += 1
        
        return ''.join(res)
''',
    call='Solution().convertNumber("twoxone")',
    expect='21',
    views=[
        dict(type='text', fn=_top, size=26, h=70),
        dict(type='string', var='s', label='s（蓝箭头 = p；黄色 = 当前单词要覆盖的范围）', pointers={'p': 'blue'},
             color=lambda S, i, v: ('yellow' if 'w' in S and S['p'] <= i < S['p'] + len(S['w']) and S['_line'] >= 19 else None),
             h=230),
        dict(type='array', var='res', label='res（已提取的数字）', h=200),
        dict(type='text', fn=lambda S: f"当前尝试：`{S['w']}` → `{S['v']}`" if 'w' in S else '', size=26, h=70),
    ],
    watch=[('p', 'p', 'blue'), ('w', 'w', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums = {': '单词 → 数字的哈希表 `nums`，共 10 个单词',
        'res = []': '`res` 存提取出的数字字符',
        'p = 0': '`p` 从 `s` 头部开始向后移动',
        'while p < len(s)': lambda S, B, r: (f'`p = {S.p} < {len(S.s)}`，还没到末尾' if S.p < len(S.s) else f'`p = {S.p}` 到达末尾 → 解析结束'),
        'for w, v in nums.items()': lambda S, B, r: ((f"试下一个单词 `{S.w}`（对应 `{S.v}`）" if S.w != B.get('w') else f'10 个单词都不匹配 → `s[{S.p}]` 不属于任何数字词') if 'w' in S else '遍历 nums'),
        'if p + len(w)': lambda S, B, r: (
            f"`s[{S.p}:{S.p+len(S.w)}] = \"{S.s[S.p:S.p+len(S.w)]}\"` == `{S.w}` → ==匹配==" if S.p + len(S.w) <= len(S.s) and S.s[S.p:S.p+len(S.w)] == S.w
            else (f"从 `{S.p}` 起放不下 `{S.w}`（越界）→ 不匹配" if S.p + len(S.w) > len(S.s)
                  else f"`\"{S.s[S.p:S.p+len(S.w)]}\"` ≠ `{S.w}` → 不匹配")),
        'res.append(v)': '找到有效单词 `{w}`，把 `{v}` 加入答案：`res = {res}`',
        'p += len(w) - 1': '跳过整个单词：先加 `len(w) - 1 = {len(w)-1}`，下面还会再 +1',
        'break': '已匹配，不用再试别的单词',
        'p += 1': '`p` 前进到 `{p}`：没匹配就只走一步，匹配过则落在单词之后',
        'return': '拼接所有数字：`"{\'\'.join(res)}"`',
    },
    skip=['"one"', '"two"', '"three"', '"four"', '"five"', '"six"', '"seven"', '"eight"', '"nine"', '"zero"'],
    max_steps=90,
    cards=dict(
        one_liner='每个位置试 10 个单词，匹配就跳过整词',
        complexity='时间 `O(10·n·5)`，即 `O(n)`；空间 `O(1)`',
        problem=['字符串 `s` 由小写字母组成，其中可能含 0~9 的英文单词（无空格）',
                 '从左到右解析：当前位置有数字词就加入答案并跳过该词；否则跳过==恰好一个字符==',
                 '本视频：`"twoxone"` → `"21"`'],
        quote='一对多的字符串匹配，通常可以使用trie图来处理，不过本题中这些多的长度都很短……因此在这里直接暴力匹配就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['单词最长只有 `three/seven/eight` 5 个字母，前缀也没多少可复用',
              '建哈希表 `nums`，对每个 `p` 遍历所有单词，比较 `s[p: p+len(w)]`',
              '匹配 → 记数字、`p` 跳过整词；全不匹配 → `p` 只走一步'],
        summary=['时间 `O(n)`（常数约 50），空间 `O(1)`',
                 '易错：先判断 `p + len(w) <= len(s)` 再切片，避免越界比较',
                 '`p += len(w) - 1` 之后外面还有 `p += 1`，合起来正好跳过整词',
                 '词数更多、更长时改用字典树或 AC 自动机',
                 '原文为 Python 2 风格，无需修改即可在 Python 3 运行'],
    ),
)
