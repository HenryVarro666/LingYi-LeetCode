HOUSES = [1, 5, 8, 11]
HEATERS = [2, 10, 6]
SH = sorted(HEATERS)
W = 12


def _pos(S, i, v):
    cur = S.get('house') if 'res' in S else None
    if cur is not None and i == cur:
        return 'pink'
    if i in SH:
        return 'orange'
    if i in HOUSES:
        return 'blue'
    return None


def _lbl(i):
    if i in SH and i in HOUSES:
        return '房暖'
    if i in SH:
        return '暖'
    if i in HOUSES:
        return '房'
    return str(i)


def _top(S):
    if 'res' not in S:
        return '每个房子找==最近的供暖器==，这些距离的最大值就是答案'
    h = S.get('house')
    if h is None:
        return f"`res = {S['res']}`"
    if S['_line'] in (12, 13, 14, 15, 17) and 'l' in S:
        return f"房子 `{h}`：二分找第一个 `≥ {h}` 的供暖器，区间 `[{S['l']}, {S['r']}]`"
    if S['_line'] in (19, 20, 22) and 'l' in S:
        l = S['l']
        if l == 0:
            return f"房子 `{h}` 在第一个供暖器 `{SH[0]}` 之前 → 距离 `{SH[0] - h}`"
        return f"房子 `{h}` 在 `{SH[l - 1]}` 和 `{SH[l]}` 之间 → 取较近的 `min({SH[l] - h}, {h - SH[l - 1]})`"
    if S['_line'] in (7, 8) and h >= SH[-1]:
        return f"房子 `{h}` 在最后一个供暖器 `{SH[-1]}` 之后 → 距离 `{h - SH[-1]}`"
    return f"处理房子 `{h}`，当前 `res = {S['res']}`"


CONFIG = dict(
    num=475, title='供暖器', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='排序 + 二分最近供暖器',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def findRadius(self, houses, heaters):

        heaters = sorted(heaters)
        res = 0
        for house in houses:
            if house >= heaters[-1]:
                res = max(res, house - heaters[-1])
            else:
                l = 0
                r = len(heaters) - 1
                while l < r:
                    mid = (l + r) >> 1
                    if heaters[mid] >= house:
                        r = mid
                    else:
                        l = mid + 1

                if l == 0:
                    res = max(res, heaters[0] - house)
                else:
                    res = max(res, min(heaters[l] - house, house - heaters[l - 1]))
        
        return res
''',
    call=f'Solution().findRadius({HOUSES}, {HEATERS})',
    expect=2,
    views=[
        dict(type='text', fn=_top, size=26, h=80),
        dict(type='array', var=lambda S: [_lbl(i) for i in range(W + 1)],
             label='数轴 0~12（蓝 = 房子，橙 = 供暖器，粉 = 当前房子）', cell=62, color=_pos, h=200),
        dict(type='array', var=lambda S: S['heaters'] if 'res' in S else SH, label='排序后的 heaters', cell=110, h=220,
             pointers={'l': 'blue', 'mid': 'yellow', 'r': 'pink'},
             color=lambda S, i, v: ('green' if 'l' in S and S['_line'] in (19, 20, 22) and (i == S['l'] or (S['l'] > 0 and i == S['l'] - 1)) else None)),
    ],
    watch=['house', ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('mid', 'mid', 'yellow'), ('res', 'res', 'green')],
    captions={
        'heaters = sorted': '先对供暖器排序：`{heaters}`，之后才能二分',
        'res = 0': '`res`：所有房子到最近供暖器距离的最大值',
        'for house in': lambda S, B, r: ('所有房子都处理完了' if 'house' in B and B.house == S.house else f'处理房子 `house = {S.house}`'),
        'if house >= heaters[-1]': lambda S, B, r: (f'`{S.house} ≥ {S.heaters[-1]}`：在最后一个供暖器之后 → ==只能由它供暖=='
                                                     if S.house >= S.heaters[-1] else f'`{S.house} < {S.heaters[-1]}`：二分找它两侧的供暖器'),
        'res = max(res, house - heaters[-1])': '距离 `{house} − {heaters[-1]} = {house - heaters[-1]}` → `res = {res}`',
        'l = 0': '在 `heaters` 里二分：`l = 0`',
        'r = len': '`r = {r}`',
        'while l < r': lambda S, B, r: (f'`[{S.l}, {S.r}]` 还有多个位置，继续二分' if S.l < S.r
                                         else f'`l == r = {S.l}`：`heaters[{S.l}] = {S.heaters[S.l]}` 是第一个 `≥ {S.house}` 的供暖器'),
        'mid = (l + r)': '`mid = ({l} + {r}) >> 1 = {mid}`',
        'if heaters[mid] >= house': lambda S, B, r: (f'`heaters[{S.mid}] = {S.heaters[S.mid]} ≥ {S.house}`：答案在 mid 或左边'
                                                      if S.heaters[S.mid] >= S.house else f'`heaters[{S.mid}] = {S.heaters[S.mid]} < {S.house}`：答案在 mid 右边'),
        'r = mid': '`r = {r}`',
        'l = mid + 1': '`l = {l}`',
        'if l == 0': lambda S, B, r: ('`l == 0`：房子在第一个供暖器之前 → ==由第一个供暖器供暖==' if S.l == 0
                                       else f'`l = {S.l}`：房子在 `heaters[{S.l - 1}] = {S.heaters[S.l - 1]}` 和 `heaters[{S.l}] = {S.heaters[S.l]}` 之间'),
        'res = max(res, heaters[0] - house)': '距离 `{heaters[0]} − {house} = {heaters[0] - house}` → `res = {res}`',
        'res = max(res, min(': '==取较近的==：`min({heaters[l] - house}, {house - heaters[l - 1]}) = {min(heaters[l] - house, house - heaters[l - 1])}` → `res = {res}`',
        'return res': '最小加热半径 =={ret}==',
    },
    cards=dict(
        one_liner='每个房子只看离它最近的供暖器，取这些距离的最大值',
        complexity='时间 `O((n + m) log m)`，空间 `O(1)`（不计排序）',
        problem=['数轴上有房子 `houses` 和供暖器 `heaters`，所有供暖器的加热半径相同',
                 '求能让==所有房子都被覆盖==的最小加热半径',
                 '示例：`houses = [1,2,3,4], heaters = [1,4]` → `1`；本视频 `[1,5,8,11], [2,10,6]` → `2`'],
        quote='对于每个房子，我们只需要找到与该房子==距离最近的供暖器==并计算二者之间的距离，那么这些距离的最大值即为最后答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['先对供暖器排序',
              '房子在最后一个供暖器之后 → 用最后一个；在第一个之前 → 用第一个',
              '否则二分找到两侧的供暖器，==取较近的那个=='],
        summary=['时间 `O(m log m + n log m)`，空间 `O(1)`（不计排序）',
                 '二分求的是==第一个 ≥ house== 的供暖器下标 l，左邻居是 `l − 1`',
                 '`house ≥ heaters[-1]` 先特判，二分时 l 就不会越界',
                 '也可以把房子也排序后用双指针同向扫描（灵神题单把它放在双指针里）'],
    ),
)
