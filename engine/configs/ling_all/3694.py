S, K = 'ULURRD', 2


def _win(S_):
    i = S_.get('i')
    if i is None:
        return None
    return i - S_['k'] + 1


def _off(S_):
    if 'x' not in S_:
        return '`st` 保存的是==相对第一个窗口的偏移量==，不是最终坐标'
    return f"当前偏移量 `(x, y) = ({S_['x']}, {S_['y']})`：窗口每右移一格，进来一步、出去一步"


CONFIG = dict(
    num=3694, title='删除子字符串后不同的终点', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='定长滑窗 · 偏移量去重',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1739'],
    code='''
DIRS = {
    'L': (-1, 0),
    'R': (1, 0),
    'D': (0, -1),
    'U': (0, 1),
}

class Solution:
    def distinctPoints(self, s: str, k: int) -> int:
        st = {(0, 0)}  # 第一个窗口
        x = y = 0
        for i in range(k, len(s)):
            in_x, in_y = DIRS[s[i]]
            out_x, out_y = DIRS[s[i - k]]
            x += in_x - out_x
            y += in_y - out_y
            st.add((x, y))
        return len(st)
''',
    call=f'Solution().distinctPoints({S!r}, {K})',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（框 = 当前删掉的长为 k 的窗口）', cell=96, h=190,
             pointers={'i': 'blue'}, window=(_win, 'i')),
        dict(type='set', var='st', label='st（不同的偏移量）', fmt=lambda p: f'({p[0]},{p[1]})', h=170, font=30),
        dict(type='text', h=90, size=30, fn=_off),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'orange'), ('y', 'y', 'orange'), ('len(st)', 'len(st)', 'green')],
    captions={
        'st = {(0, 0)}': '第一个窗口相对自己的偏移量是 `(0, 0)`，先放进集合',
        'x = y = 0': '`x, y` 记录当前窗口相对第一个窗口的偏移',
        'for i in range': lambda S, B, ret: (f'窗口右端点 `i = {S.i}`，左端点 `i − k = {S.i - S.k}`' if 'i' not in B or S.i != B.i else '遍历结束'),
        'in_x, in_y = DIRS': '右边进来 `{s[i]!r}`：偏移 `({in_x}, {in_y})`',
        'out_x, out_y = DIRS': '左边出去 `{s[i - k]!r}`：偏移 `({out_x}, {out_y})`',
        'x += in_x': '`x` += `{in_x} − ({out_x})` → {x}',
        'y += in_y': '`y` += `{in_y} − ({out_y})` → {y}',
        'st.add': '偏移量不同 ⇔ 最终坐标不同，加入集合：`({x}, {y})`，现有 `{len(st)}` 个',
        'return len(st)': '集合大小就是答案：`{len(st)}`',
    },
    cards=dict(
        one_liner='站在最终坐标看，删掉子串 = 加上一个偏移量',
        complexity='时间 `O(n−k)`，空间 `O(n−k)`',
        problem=['`s` 由 `U/D/L/R` 组成，表示在网格上走路；必须删掉==恰好一个==长为 `k` 的子串',
                 '求删完后能走到的==不同终点==个数',
                 f'本视频：`s = "{S}", k = {K}`'],
        quote='横看成岭侧成峰，站在最终坐标的位置看，去掉子串后的偏移量为 (-1,-1)。……偏移量不同，最终坐标也不同。',
        quote_src='—— 灵茶山艾府题解',
        idea=['终点 = 原终点 + 被删子串的偏移的相反数，所以数不同终点 = 数不同的偏移量',
              '长为 `k` 的子串偏移量用==定长滑窗==算',
              '优化：所有窗口都从第一个窗口出发，只记相对增减量'],
        summary=['时间 `O(n−k)`，空间 `O(n−k)`',
                 '优化前直接存最终坐标，要先把整段走完；优化后集合存增减量，第一个窗口记 `(0,0)`',
                 '易错：循环从 `i = k` 开始，第一个窗口已手动放入集合',
                 '写法二把 `(x,y)` 压成一维整数 `x*(n+1)+y`，更快；本视频用二维元组写法'],
    ),
)
