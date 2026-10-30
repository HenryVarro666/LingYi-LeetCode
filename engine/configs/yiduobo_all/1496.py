def _dec(k):
    y = (k + 500) % 1001 - 500
    return (k - y) // 1001, y


def _pos(S):
    if 'nowx' not in S:
        return ''
    return f"当前位置 `({S['nowx']}, {S['nowy']})`　编码 `x*1001+y` = =={S['nowx'] * 1001 + S['nowy']}=="


def _path_color(S, i, v):
    return None


CONFIG = dict(
    num=1496, title='判断路径是否相交', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='模拟 + 哈希集合', tags=[],
    code='''
class Solution(object):
    def isPathCrossing(self, path):

        dx = {'N': 0, 'S': 0, 'E': 1, 'W': -1}
        dy = {'N': 1, 'S': -1, 'E': 0, 'W': 0}

        nowx, nowy = 0, 0
        used = set([0])
        for char in path:
            nowx += dx[char]
            nowy += dy[char]
            if nowx * 1001 + nowy in used:
                return True

            used.add(nowx * 1001 + nowy)
        
        return False
''',
    call="Solution().isPathCrossing('NESWW')",
    expect=True,
    views=[
        dict(type='text', fn=_pos, size=30, h=70),
        dict(type='string', var='path', h=150, label='path（N 北 / S 南 / E 东 / W 西）'),
        dict(type='set', var='used', fmt=lambda k: '(%d,%d)' % _dec(k), h=330, label='used：走过的点（已编码）'),
    ],
    watch=['char', 'nowx', 'nowy', ('used', 'sorted(used)', 'green')],
    captions={
        'dx = {': '`dx`：每个方向让横坐标变多少，东 +1、西 −1',
        'dy = {': '`dy`：每个方向让纵坐标变多少，北 +1、南 −1',
        'nowx, nowy = 0, 0': '从原点 `(0, 0)` 出发',
        'used = set': '`used` 先放入原点（编码 `0*1001+0 = 0`）：==起点也算走过==',
        'for char in path': '取下一步方向 `{char}`',
        'nowx += dx': '横坐标 `+= dx[{char}]` → `nowx = {nowx}`',
        'nowy += dy': '纵坐标 `+= dy[{char}]` → `nowy = {nowy}`',
        'in used': lambda S, B, r: (f"点 `({S.nowx}, {S.nowy})` 编码 `{S.nowx*1001+S.nowy}`："
                                    + ('==已在 used 里== → 路径相交，返回 True' if S.nowx*1001+S.nowy in S.used
                                       else '没来过，继续走')),
        'return True': '回到走过的点，路径相交 → `True`',
        'used.add': '记下新点 `({nowx}, {nowy})`，把编码 `{nowx*1001+nowy}` 加进 `used`',
        'return False': '走完都没重复 → `False`',
    },
    cards=dict(
        one_liner='模拟行走，用哈希集合记点，回到旧点就相交',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`path` 由 `N S E W` 组成，从原点出发依次向北、南、东、西走一步',
                 '如果路径经过了之前到过的点（含原点），返回 `True`，否则 `False`',
                 '示例：`"NES"` → `False`，`"NESWW"` → `True`'],
        quote='由于这里操作数最多是有一万，那么可以直接模拟整个行走过程，然后使用哈希表来判断是否产生相交。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作数只有一万，直接一步步走，不用想别的办法',
              '把点 `(x, y)` 编成一个整数 `x*1001+y` 放进集合，查重是 `O(1)`',
              '本视频：`NESWW` 走到第 4 步回到原点，正好撞上起点'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：==原点要先放进集合==，否则绕一圈回原点会漏判',
                 '编码乘 1001：`|y| <= 1000`，不同点编码不会撞',
                 '原文为 Python 2 写法，在 Python 3 下无需改动'],
    ),
)
