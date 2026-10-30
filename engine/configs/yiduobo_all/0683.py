BULBS = [2, 1, 5, 3, 4]


def _lamps(S):
    return list(range(1, len(BULBS) + 1))


def _cell(S, i, v):
    il = S.get('illuminated')
    if il is None:
        return None
    b = S.get('b')
    k = S.get('k')
    if b is not None and v == b:
        return 'yellow'
    if v in il:
        return 'green'
    return None


def _dim(S, i, v):
    il = S.get('illuminated')
    return il is not None and v not in il


def _fn(S):
    b = S.get('b')
    if b is None:
        return '每天亮一盏灯；要找：两盏亮灯之间恰好隔 `k` 盏灭灯'
    k = S['k']
    return f"今天点亮第 `{b}` 号；左候选 `{b - 1 - k}`，右候选 `{b + 1 + k}`"


CONFIG = dict(
    num=683, title='K个关闭的灯泡', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='集合 + 树状数组（区间灭灯判定）',
    tags=['灵神题单·贪心与思维'],
    code='''
class Solution(object):
    def kEmptySlots(self, bulbs, k):

        illuminated = set()
        n = len(bulbs)
        f = [0] * (n + 1)

        def add(now):
            while now <= n:
                f[now] += 1
                now += now & -now
        
        def get(now):
            s = 0
            while now > 0:
                s += f[now]
                now -= now & -now
            return s

        for index, b in enumerate(bulbs):
            illuminated.add(b)
            left = b - 1 - k
            if left in illuminated and get(left) == get(b - 1):
                return index + 1
            
            right = b + 1 + k
            if right in illuminated and get(right - 1) == get(b):
                return index + 1

            add(b)

        
        return -1
''',
    call=f'Solution().kEmptySlots({BULBS}, 1)',
    expect=4,
    skip=['n = len(bulbs)', 'f = [0]', 'now & -now', 's = 0', 'illuminated = set()', 'def add', 'def get'],
    max_steps=90,
    views=[
        dict(type='array', var=_lamps, label='灯泡位置 1..n（黄 = 今天点亮，绿 = 已亮，灰 = 灭）', h=190, cell=90, index=False,
             color=_cell, dim=_dim),
        dict(type='text', fn=_fn, size=24, h=60),
        dict(type='array', var='f', label='树状数组 f（f[i] 管着以 i 结尾的一段亮灯数）', h=190, cell=80),
        dict(type='set', var='illuminated', label='illuminated：已亮的灯', h=110),
    ],
    watch=[('index', 'index', 'blue'), 'b', 'left', 'right', 'k'],
    captions={
        'illuminated = set()': '`illuminated` 记哪些灯已经亮了，用来 `O(1)` 判断单盏灯亮灭',
        'f = [0]': '树状数组 `f`：动态维护「前缀里有多少盏亮灯」',
        'illuminated.add(b)': '第 `{index + 1}` 天点亮 `{b}` 号灯',
        'left = b - 1 - k': '答案一定出现在某盏灯刚亮时：左边的另一端应在 `b-1-k` = `{left}`',
        'if left in illuminated': lambda S, B, r: (f'左端 `{S.left}` ' + ('已亮 → 比较 `get(left)` 与 `get(b-1)`：前缀亮灯数相等 ⇔ 中间全灭' if S.left in S.illuminated else '未亮或越界 → 这边不成立')),
        'right = b + 1 + k': '右边的另一端应在 `b+1+k` = `{right}`',
        'if right in illuminated': lambda S, B, r: (f'右端 `{S.right}` ' + ('已亮 → 比较 `get(right-1)` 与 `get(b)`' if S.right in S.illuminated else '未亮或越界 → 这边不成立')),
        'while now > 0': '查前缀：沿 `now -= now & -now` 往前累加 `f`',
        's += f[now]': '`s += f[{now}]` → s = {s}',
        'return s': '前缀亮灯数 `get` = =={ret}==',
        'return index + 1': '第 `{ret}` 天首次出现符合条件的灯对 → ==返回 {ret}==',
        'add(b)': '两边都不成立：把 `{b}` 加进树状数组（亮灯数 +1）',
        'f[now] += 1': '树状数组第 `{now}` 格 + 1',
        'return -1': '遍历完都没有 → 返回 -1',
    },
    cards=dict(
        one_liner='灯刚亮时才可能成立：只查它左右 k+1 处的灯',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`n` 个灯泡一开始都灭，第 `i` 天点亮位置 `bulbs[i]` 的灯（位置从 1 开始）',
                 '求最早哪一天，存在两盏亮灯，它们之间恰有 `k` 盏灯是灭的',
                 '不存在返回 `-1`；本视频：`bulbs=[2,1,5,3,4]`，`k=1` → `4`'],
        quote='题目要求的情况必然出现在某盏灯被打开的这一刻……区间(l, r)的灯都灭，等价于区间[0, r - 1]中亮的灯的数量等于区间[0, l]中亮的灯的数量。',
        quote_src='—— yiduobo 题解原文',
        idea=['新点亮 `b` 的那一刻才可能凑成灯对：只查左边 `b-1-k` 和右边 `b+1+k`',
              '单盏灯亮灭用集合；「中间 k 盏全灭」转成两个前缀亮灯数相等',
              '动态前缀和 → 树状数组 `add` / `get`'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：树状数组下标从 1 开始，所以 `bulbs` 的位置正好直接用',
                 '左右两边都要查；两边都不成立才 `add(b)`',
                 '返回天数是 `index + 1`（下标从 0 开始）',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
