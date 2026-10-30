NUMS = [2, 2, 1, 1, 1, 2, 2]

TRACK = '''
class KList(list):  # 快照用的普通 list（带上下标 k）
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _sim(m):
    """模拟前 m 个元素的擂台赛，返回 (ans, hp, 每个元素所在的段号)"""
    ans = hp = 0
    seg, cur = [], -1
    for x in NUMS[:m]:
        if hp == 0:
            ans, hp = x, 1
            cur += 1
        else:
            hp += 1 if x == ans else -1
        seg.append(cur)
    return ans, hp, seg


def _done(S):
    """已经比完的人数（只用于画图）"""
    k = getattr(S.get('nums'), 'k', -1)
    if k is None:
        return len(NUMS)
    if k < 0 or 'hp' not in S:
        return 0
    a, h, _ = _sim(k + 1)
    return k + 1 if (a, h) == (S['ans'], S['hp']) and _sim(k)[:2] != (a, h) else k


def _color(S, i, v):
    m = _done(S)
    if i >= m:
        return None
    return ['blue', 'purple', 'cyan', 'orange'][_sim(m)[2][i] % 4]


def _cuts(S):
    """已经“切下”的段：每段里众数 2 的个数 x ≤ 其余个数 y（只用于画图）"""
    m = _done(S)
    if m == 0:
        return ''
    _, hp, seg = _sim(m)
    nseg = seg[-1] + 1 if hp > 0 else seg[-1] + 2
    parts = []
    for g in range(nseg - 1):
        arr = [NUMS[i] for i in range(m) if seg[i] == g]
        x = arr.count(2)
        parts.append(f'`{arr}`：众数 2 有 {x} 个 ≤ 其余 {len(arr) - x} 个')
    if not parts:
        return '还没有切下任何一段'
    return '已切下：' + '；'.join(parts)


def _ring(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '擂台', 24, T['muted'], bold=True)
    hp, ans = S.get('hp'), S.get('ans')
    if hp is None:
        return
    X, Y = x0 + 60, y0 + 46
    if hp == 0:
        cv.rect((X, Y, X + 200, Y + 80), outline=T['border'], width=2, r=14)
        cv.text((X + 100, Y + 40), '擂台空着', 28, T['dim'], anchor='mm', bold=True)
    else:
        cv.rect((X, Y, X + 200, Y + 80), fill=T['yellow'], r=14)
        cv.text((X + 100, Y + 40), f'擂主 {ans}', 34, T['bg'], anchor='mm', bold=True)
    cv.text((X + 240, Y + 40), '生命值', 26, T['muted'], anchor='lm')
    for j in range(max(hp, 0)):
        cv.rect((X + 340 + j * 52, Y + 18, X + 384 + j * 52, Y + 62), fill=T['red'], r=8)
    if hp == 0:
        cv.text((X + 340, Y + 40), '0', 30, T['dim'], anchor='lm', bold=True)


CONFIG = dict(
    num=169, title='多数元素', difficulty='Easy', category='技巧',
    author='灵茶山艾府', technique='擂台赛（摩尔投票）',
    code='''
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        ans = hp = 0
        for x in nums:
            if hp == 0:  # x 是初始擂主，生命值为 1
                ans, hp = x, 1
            else:  # 比武，同门加血，否则扣血
                hp += 1 if x == ans else -1
        return ans
''',
    setup=TRACK,
    call=f'Solution().majorityElement(TList({NUMS}))',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums（同一种颜色 = 同一场擂台赛，即证明里切出的一段）', h=210,
             pointers={_k: 'yellow'}, pointer_labels={_k: 'x'}, color=_color),
        dict(type='custom', draw=_ring, h=160),
        dict(type='text', fn=lambda S: '同门（值相同）→ 擂主 ==加血==；不同门 → ==扣血==；血量为 0 → 下一个挑战者上台', size=26, h=80),
        dict(type='text', fn=_cuts, size=26, h=120, lines=3),
    ],
    watch=[('x', 'x', 'yellow'), ('ans', 'ans', 'green'), ('hp', 'hp', 'red')],
    captions={
        'ans = hp = 0': '擂台空着：`hp = 0`，第一个人上来就是擂主',
        'for x in nums': lambda S, B, ret: (f'挑战者 `x = {S.x}` 登场' if _k(S) is not None else '所有人都比完了'),
        'if hp == 0': lambda S, B, ret: ('`hp == 0`：擂台空着 → `x` ==直接当擂主==' if S.hp == 0
                                         else f'擂主 `{S.ans}` 还有 `{S.hp}` 滴血 → 比武'),
        'ans, hp = x, 1': '`{x}` 成为擂主，生命值 `1`（==新开一场擂台赛==）',
        'hp += 1 if x == ans': lambda S, B, ret: (
            f'`{S.x}` 与擂主同门 → 加血，`hp = {S.hp}`' if S.x == S.ans
            else f'`{S.x}` 不同门 → 扣血，`hp = {S.hp}`' + ('，==同归于尽==！下一个挑战者上台' if S.hp == 0 else '')),
        'return ans': '最后站在擂台上的 `{ret}` 就是==武林盟主==（绝对众数）',
    },
    cards=dict(
        one_liner='武林大会打擂台：同门加血、异门扣血，最后站着的就是众数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['返回数组中出现次数 ==大于 n/2== 的多数元素（保证存在）',
                 '进阶：`O(n)` 时间、`O(1)` 空间',
                 '示例：`[2,2,1,1,1,2,2]` → `2`'],
        quote='想象一众武林高手比武……如果挑战者与擂主属于同一门派（值相同），那么擂主生命值加 1，否则擂主生命值减 1……最后在擂台上的那人，便是武林盟主。',
        quote_src='—— 灵茶山艾府题解',
        idea=['设众数出现 `a` 次，其余共 `b` 次，`a > b`',
              '每次血量归 0 就“切一刀”：被切掉的段里，众数个数 `x ≤ y`（否则它不会被打倒）',
              '切掉后仍有 `a−x > b−y`；最后一段众数血多，==站到最后的必是众数=='],
        result='最后的擂主 `2` 就是多数元素 ✓',
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '前提：题目==保证存在==绝对众数；否则最后的擂主还需再数一遍',
                 '中途的擂主不一定是众数（如 `[1,1,2,9]` 那段），只有最后一段才保证',
                 '思考题：如何判断是否存在绝对众数？再遍历一次计数即可'],
    ),
)
