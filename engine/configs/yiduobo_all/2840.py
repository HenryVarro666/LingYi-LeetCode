CONFIG = dict(
    num=2840, title='判断通过操作能否让字符串相等 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶分组 · 计数相消',
    tags=['灵神题单', '难度分 1486'],
    code='''
class Solution(object):
    def checkStrings(self, s1, s2):

        cnt = [[0] * 26 for _ in range(2)]

        for index, char in enumerate(s1):
            cnt[index % 2][ord(char) - 97] += 1
        
        for index, char in enumerate(s2):
            cnt[index % 2][ord(char) - 97] -= 1
            if cnt[index % 2][ord(char) - 97] < 0:
                return False
        
        return True
''',
    call='Solution().checkStrings("abcdba", "cabdab")',
    expect=True,
    views=[
        dict(type='string', var='s1', label='s1（蓝 = 偶数下标，粉 = 奇数下标，黄 = 当前）', h=210,
             color=lambda S, i, v: 'yellow' if S['_line'] in (6, 7) and S.get('index') == i else ('blue' if i % 2 == 0 else 'pink')),
        dict(type='string', var='s2', label='s2', h=210,
             color=lambda S, i, v: 'yellow' if S['_line'] in (9, 10, 11) and S.get('index') == i else ('blue' if i % 2 == 0 else 'pink')),
        dict(type='map', var=lambda S: {chr(97 + j): c for j, c in enumerate(S['cnt'][0]) if c} if 'cnt' in S else {},
             label='cnt[0]：偶数下标的字符计数', h=120, fmt=lambda k, v: f'{k}:{v}'),
        dict(type='map', var=lambda S: {chr(97 + j): c for j, c in enumerate(S['cnt'][1]) if c} if 'cnt' in S else {},
             label='cnt[1]：奇数下标的字符计数', h=120, fmt=lambda k, v: f'{k}:{v}'),
    ],
    watch=[('index', 'index', 'yellow'), ('char', 'char', 'green')],
    captions={
        'cnt = [[0]': '`cnt[0]` 记偶数下标的 26 个字母次数，`cnt[1]` 记奇数下标的',
        'cnt[index % 2][ord(char) - 97] += 1': '`s1[{index}] = {char}` 在 `{"偶" if index % 2 == 0 else "奇"}` 数下标：`cnt[{index % 2}]` 的 `{char}` 加 1',
        'cnt[index % 2][ord(char) - 97] -= 1': '`s2[{index}] = {char}` 在 `{"偶" if index % 2 == 0 else "奇"}` 数下标：`cnt[{index % 2}]` 的 `{char}` 减 1，用来抵消 s1 里的字符',
        'if cnt[index % 2][ord(char) - 97] < 0': lambda S, B, r: (f'`{S.char}` 在这个奇偶组里被减成负数 → s1 里没有足够的 `{S.char}`，凑不出 s2 → ==False==' if S.cnt[S.index % 2][ord(S.char) - 97] < 0 else f'`cnt[{S.index % 2}]` 里 `{S.char}` 还有 `{S.cnt[S.index % 2][ord(S.char) - 97]}` 个，没减成负数，继续'),
        'return False': '这组字符个数对不上 → 返回 `False`',
        'return True': 's2 的每个字符都抵消掉了（两串等长）→ 每组个数相同 → ==True==',
    },
    cards=dict(
        one_liner='按奇偶下标分成两组，比较每组里每个字符的个数',
        complexity='时间 `O(n)`，空间 `O(1)`（26×2 的计数表）',
        problem=['两个等长小写字符串，可交换同一个串中下标差为偶数的两个字符，次数不限',
                 '问能否让 `s1` 与 `s2` 相等',
                 '本视频：`s1 = "abcdba"`，`s2 = "cabdab"` → `true`'],
        quote='本题中可以执行操作的下标对必须是同奇偶的，那么做法就顺势变成了按照奇偶将两个字符串都分成两个部分，然后比较这两个部分中每个字符出现的次数是否相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['同奇偶的位置可以随便换，所以只看每组里有哪些字符、各几个',
              '先扫 `s1`，把偶、奇下标的字符分别计数加 1',
              '再扫 `s2`，对应减 1；任何一个减到负数，说明 `s2` 的该字符比 `s1` 多 → `False`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：计数表要按奇偶分成两行，不能混着数',
                 '扫完 `s2` 没出现负数且两串等长，则每个计数都为 0 → `True`',
                 '对比灵神：灵神切片后用 `Counter` 比较，yiduobo 用 26 位计数表边减边判断',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
