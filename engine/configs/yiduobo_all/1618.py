def _mid_text(S):
    if 'f_size' in S['_inner']:
        c = S['_inner']
        s = c.get('s', 0)
        return (f"字号 `{c['f_size']}`：高 `{c['f_size']}` / 限高 `{S['h']}`；已累加宽度 `{s}` / 限宽 `{S['w']}`")
    if 'mid' in S:
        return f"二分 `left={S['left']}`（合法）  `right={S['right']}`  `mid={S['mid']}`"
    return ''


CONFIG = dict(
    num=1618, title='找出适应屏幕的最大字号', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分字号 + 逐字累加宽度',
    tags=['二分算法', '贪心与思维'],
    setup='''
class FontInfo(object):
    # 题目给的接口：字号越大，字符越宽、越高（此处宽 = 字号 // 2，高 = 字号）
    def getWidth(self, fontSize, ch):
        return fontSize // 2
    def getHeight(self, fontSize):
        return fontSize
''',
    code='''
#class FontInfo(object):
class Solution(object):
    def maxFont(self, text, w, h, fonts, fontInfo):
        def check(f_size):
            if fontInfo.getHeight(f_size) > h:
                return False
            s = 0
            for char in text:
                s += fontInfo.getWidth(f_size, char)
            return s <= w
        if not check(fonts[0]):
            return -1
        left, right = 0, len(fonts) - 1
        while left < right:
            mid = (left + right + 1) // 2
            if check(fonts[mid]):
                left = mid
            else:
                right = mid - 1
        return fonts[left]
''',
    call='Solution().maxFont("world", 50, 30, [6, 8, 10, 12, 14, 16, 18, 24, 32, 40], FontInfo())',
    expect=18,
    views=[
        dict(type='text', h=70, fn=_mid_text),
        dict(type='array', var='fonts', label='fonts（升序；蓝 = left，粉 = right，黄 = mid）', cell=84, h=220,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}, window=('left', 'right'),
             dim=lambda S, i, v: 'right' in S and not (S['left'] <= i <= S['right']),
             color=lambda S, i, v: 'green' if 'left' in S and i == S['left'] else None),
        dict(type='string', var='text', label='text（check 时逐个字符累加宽度）', cell=70, h=150),
    ],
    watch=[('left', 'left', 'blue'), ('right', 'right', 'pink'), ('mid', 'mid', 'yellow'),
           ('f_size', 'f_size'), ('s', 's', 'green')],
    captions={
        'if fontInfo.getHeight': lambda S, B, r: (f'字号 `{S.f_size}` 的高 `{S.fontInfo.getHeight(S.f_size)}` > 限高 `{S.h}` → 太高，不合法'
                                                   if S.fontInfo.getHeight(S.f_size) > S.h
                                                   else f'字号 `{S.f_size}` 的高 `{S.fontInfo.getHeight(S.f_size)}` ≤ 限高 `{S.h}`：高度过关，再看宽度'),
        's = 0': '宽度总和从 0 开始',
        's += fontInfo.getWidth': '加上 `{char}` 的宽度：`s = {s}`',
        'return s <= w': lambda S, B, r: f'总宽 `{S.s}` {"≤" if S.s <= S.w else ">"} 限宽 `{S.w}` → ==字号 {S.f_size} {"合法" if r else "放不下"}=='
                                          ,
        'if not check(fonts[0])': lambda S, B, r: '最小字号 `fonts[0]` 都放不下就无解，返回 -1；否则至少 `fonts[0]` 合法',
        'left, right = 0': '`left = 0` 一定合法（上面验过），`right = {right}`',
        'while left < right': lambda S, B, r: (f'`left = {S.left} < right = {S.right}`：还没夹到一个答案' if S.left < S.right
                                               else f'`left == right = {S.left}`：最大合法字号就是 `fonts[{S.left}]`'),
        'mid = (left + right + 1) // 2': '`mid = {mid}`：==+1 向上取整==，因为下面 `left = mid` 要保证区间会缩小',
        'if check(fonts[mid])': lambda S, B, r: f'试字号 `fonts[{S.mid}] = {S.fonts[S.mid]}` 能放下吗？',
        'left = mid': '能放下 → 更大的字号还有可能，`left = {left}`',
        'right = mid - 1': '放不下 → 比它大的都不行（字号越大越占地方），`right = {right}`',
        'return fonts[left]': '最大合法字号 `{fonts[left]}`',
    },
    cards=dict(
        one_liner='字号越大越占地方 → 二分找最大的合法字号',
        complexity='时间 `O(|text| log |fonts|)`，空间 `O(1)`',
        problem=['给 `text`、屏幕宽 `w` 高 `h`、升序字号 `fonts`，以及接口 `fontInfo`（取字符宽、字号高）',
                 '求能让整句话放进屏幕的==最大字号==，放不下返回 `-1`',
                 '本视频：`text = "world"`，宽 50，高 30，字宽 = 字号 // 2'],
        quote='字号越大，所需的高度和宽度也就越大，而字号大小已经排好序了，因此可以使用二分法来寻找合法的最大字号。',
        quote_src='—— yiduobo 题解原文',
        idea=['`check(f_size)`：高度不超限，且每个字符宽度之和不超过 `w`',
              '先验 `fonts[0]`：最小的都不行就返回 `-1`',
              '合法的字号构成前缀 → 二分 `left = mid` / `right = mid - 1`'],
        summary=['时间 `O(n log m)`：`n` 是文本长度，`m` 是字号个数',
                 '易错：`mid` 要向上取整 `+ 1`，否则 `left = mid` 会死循环',
                 '原文为 Python 2 写法，`/` 整数除法已改为 `//`；`FontInfo` 接口在 setup 里补了一个示例实现',
                 '本题是 LeetCode 会员题'],
    ),
)
