CONFIG = dict(
    num=1055, title='形成字符串的最短路径', difficulty='Medium', category='字符串',
    author='yiduobo', technique='贪心 + 环形下一位置表',
    tags=['灵神题单', '字符串'],
    code='''
class Solution(object):
    def shortestWay(self, source, target):

        next_pos = {}
        for index in range(len(source) -1, -1, -1):
            next_pos[source[index]] = index
        
        pos_list = []
        for index in range(len(source) - 1, -1, -1):
            next_pos[source[index]] = index
            pos_list.append(next_pos.copy())
        
        pos_list.reverse()

        p = 0
        res = 1

        for char in target:
            if char not in pos_list[p]:
                return -1
            
            if pos_list[p][char] < p:
                res += 1
            p = pos_list[p][char] + 1
            if p == len(source):
                p = 0
                res += 1
        
        if p == 0:
            res -= 1

        return res
''',
    call="Solution().shortestWay('abc', 'cbac')",
    expect=3,
    views=[
        dict(type='string', var='source', label='source', pointers={'p': 'blue'}, h=170),
        dict(type='string', var='target', label='target', h=110),
        dict(type='text', h=70, size=30, fn=lambda S: f"当前字符：==`{S['char']}`==　已用 ==`{S['res']}`== 份 source" if 'char' in S and 'res' in S else ''),
        dict(type='map', var=lambda S: S['pos_list'][S['p']] if 'p' in S and 'pos_list' in S and S['p'] < len(S['pos_list']) else {},
             label='pos_list[p]：从 p 起（环形）每个字母下一次出现的下标', fmt=lambda k, v: f"'{k}': {v}", h=140, font=32),
    ],
    watch=[('p', 'p', 'blue'), ('char', 'char', 'pink'), ('res', 'res', 'green')],
    captions={
        'next_pos[source[index]] = index': '`{source[index]}` 的最早位置记为 `{index}`',
        'pos_list.append': '存下 `index = {index}` 这一位的表',
        'pos_list.reverse': '翻转后 `pos_list[i]` 对应从 i 起的表',
        15: '`p`：当前这份 source 里已匹配到的位置',
        'res = 1': '至少要用 1 份 source',
        'if char not in': lambda S, B, r: (f"`'{S.char}'` 在 `pos_list[{S.p}]` 里" if S.char in S.pos_list[S.p]
                                           else f"`'{S.char}'` 根本没在 source 出现 → 返回 ==-1=="),
        'return -1': '有字符 source 里没有，无解',
        'if pos_list[p][char] < p': lambda S, B, r: (f"下一个 `{S.char}` 在 `{S.pos_list[S.p][S.char]}` < `p={S.p}` → 本份里已经没有，==要回绕到下一份 source=="
                                                     if S.pos_list[S.p][S.char] < S.p else
                                                     f"下一个 `{S.char}` 在 `{S.pos_list[S.p][S.char]}` >= `p`，本份还能用"),
        22: '回绕：多用一份 source，`res` → {res}',
        27: '这一份刚好用完，先把下一份记上：`res` → {res}',
        'p = pos_list[p][char] + 1': '匹配 `{char}`，下一个从 `{p}` 开始',
        26: '`p` 走到了 source 末尾，回到 0，下一个字符从新的一份开始',
        'if p == len(source)': '`p = {p}`，source 长 `{len(source)}`：{"==这一份刚好用完==" if p == len(source) else "本份还没用完"}',
        'if p == 0': '`p == 0` 说明最后一份是“预先多记”的，没真正使用 → `res` 要减 1',
        'res -= 1': '多算的一份减掉：`res = {res}`',
        'return res': '至少要拼接 `{res}` 个 source 的子序列',
    },
    cards=dict(
        one_liner='target 每个字符都贪心用最靠前的，走到头就换下一份',
        complexity='时间 `O(26m + n)`，空间 `O(26m)`',
        problem=['`source` 的子序列可以拼接成 `target`，求最少需要几个子序列',
                 '无法拼出返回 `-1`',
                 '本视频：`source=abc`，`target=cbac` → `3`'],
        quote='为了最终串联的字符串数量最少，在这里就应该尽量让target中的每一个字符向前匹配……得到每个字符下一次出现的位置后……可以变成通过这里记录的下一个位置进行跳转。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `p` 记录在当前这份 source 里匹配到哪了，贪心地找下一个相同字符',
              '找不到（`p` 走到末尾）就换新的一份：`p = 0`，`res + 1`',
              '预处理成“下一次出现的位置表”，每个字符一步跳过去'],
        summary=['先把全部字母写入 `next_pos`，让每张表也含“环形”回绕的位置',
                 '`pos_list[p][char] < p` 表示要回绕，答案加 1',
                 '`p` 走到末尾时已经 `res += 1` 预先计了一份，若最后 `p == 0` 要减回去',
                 '原文为 Python 2 风格，代码无需修改'],
    ),
)
