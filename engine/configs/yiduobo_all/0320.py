CONFIG = dict(
    num=320, title='列举单词的全部缩写', difficulty='Medium', category='二叉树与回溯',
    author='yiduobo', technique='dfs 回溯 · 缩写 / 保留',
    tags=['灵神题单', '链表树与回溯'],
    code='''
class Solution(object):
    def generateAbbreviations(self, word):

        res = []
        n = len(word)

        def dfs(level, now, len):
            if level == n:
                if len > 0:
                    tmp = str(len)
                else:
                    tmp = ''
                res.append(''.join(now) + tmp)
            
                return

            dfs(level + 1, now, len + 1)
            
            if len > 0:
                now.append(str(len))
                now.append(word[level])
                dfs(level + 1, now, 0)
                now.pop()
                now.pop()
            else:
                now.append(word[level])
                dfs(level + 1, now, 0)
                now.pop()
        
        dfs(0, [], 0)

        return res
''',
    call='Solution().generateAbbreviations("abc")',
    expect=['3', '2c', '1b1', '1bc', 'a2', 'a1c', 'ab1', 'abc'],
    views=[
        dict(type='string', var='word', label='word（蓝 = 当前处理的字符）', cell=84, h=190,
             pointers={'level': 'blue'}),
        dict(type='text', size=28, h=70,
             fn=lambda S: f"`now` = `{''.join(S['_inner'].get('now', []))}`　　待缩写长度 `len` = ==`{S['_inner'].get('len', 0)}`==" if 'now' in S['_inner'] else ''),
        dict(type='calls', h=230),
        dict(type='stack', var='res', label='res（已找到的缩写）', h=150, fmt=lambda x: x),
    ],
    watch=[('level', lambda S: S['_inner'].get('level'), 'blue'), ('len', lambda S: S['_inner'].get('len'), 'orange')],
    skip=['res = []', 'n = len(word)', 'tmp = str(len)', "tmp = ''"],
    captions={
        'dfs(0, [], 0)': '从 `dfs(0, [], 0)` 开始：第 0 个字符，还没构造任何东西',
        'if level == n': lambda S, B, ret: ('`level == n`：字符都处理完了 → ==得到一种缩写==' if S['_inner']['level'] == S.n
                                            else f"`level = {S['_inner']['level']} < n`：还要处理 `word[{S['_inner']['level']}]`"),
        'if len > 0': lambda S, B, ret: (f"`len = {S['_inner']['len']} > 0`：前面有 ==`{S['_inner']['len']}` 个字符==被缩写，保留当前字符前要先写出数字"
                                         if S['_inner']['len'] > 0 else '`len = 0`：前面没有待缩写的字符，直接保留当前字符'),
        'dfs(level + 1, now, len + 1)': '选择 1：把 `word[{level}]` ==转成缩写==，待缩写长度 +1 → 进入下一层',
        'now.append(str(len))': '先把缩写数字 `{len}` 写进 `now`：`{"".join(now)}`',
        'now.append(word[level])': '选择 2：==保留== `word[{level}]` = `{word[level]}`，`now` = `{"".join(now)}`',
        'dfs(level + 1, now, 0)': '保留了字符，待缩写长度清零 → 进入下一层',
        'res.append': lambda S, B, ret: f"记录答案 `{S.res[-1]}`（`now` 加上末尾剩余的数字）",
        '                return': '这条分支处理完 → 回到上一层',
        'now.pop()': '恢复现场：弹出刚加的内容，`now` = `{"".join(now)}`',
        'return res': '全部 `{len(ret)}` 种缩写：每个字符 ==缩写或保留== 共 `2^n` 种',
    },
    max_steps=110,
    cards=dict(
        one_liner='每个字符两种选择：并入缩写，或者原样保留',
        complexity='时间 `O(n·2^n)`，空间 `O(n)`（不计返回值）',
        problem=['单词可以把任意不相邻的若干子串替换成它们的长度，列出 `word` 的全部缩写',
                 '示例：`"word"` → `["4","3d","w3","1o2","w2d",...]`',
                 '本视频：`"abc"`，共 `2^3 = 8` 种'],
        quote='对于当前字符s[level]，有两种处理方法：1、将其转化为缩写，那么接下来就应该向后计算dfs(level + 1, now, len + 1)；2、保持该字符不变。',
        quote_src='—— yiduobo 题解原文',
        idea=['`level` 是处理到第几个字符，`now` 是已构造的字符串，`len` 是正在被缩写的字符数',
              '缩写：只让 `len + 1`，先不写数字，这样连续缩写自动合并成一个数',
              '保留：若 `len > 0` 先写 `str(len)`，再写字符，`len` 清零'],
        result='8 种缩写全部找到',
        summary=['时间 `O(n·2^n)`，空间 `O(n)`；n 很小才能暴力',
                 '易错：到 `level == n` 时 `len > 0` 还要在末尾补上数字',
                 '`now` 是共享列表，回溯后要 `pop`；保留分支在 `len > 0` 时 append 了两次，也要 pop 两次',
                 '原文为 Python 2 风格，参数名 `len` 遮住了内置函数，但函数内没再调用 `len()`，可直接在 Python 3 运行'],
    ),
)
