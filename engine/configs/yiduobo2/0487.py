NUMS = [1, 1, 0, 1, 1, 1, 0, 1]

SETUP = '''
class _Nums(list):
    """普通 list，只是在迭代时记下当前下标 pos，供动画画指针（不影响算法）"""
    pos = -1
    frozen = False  # 追踪器拍下的快照不再记录

    def __iter__(self):
        for k in range(len(self)):
            if not self.frozen:
                self.pos = k
            yield self[k]

    def __deepcopy__(self, memo):
        c = _Nums(self[:])
        c.pos, c.frozen = self.pos, True
        return c
'''


def _pos(S):
    nums = S.get('nums')
    return getattr(nums, 'pos', -1) if nums is not None else -1


def _upto(S):
    """elements [0, upto] are already reflected in last/now"""
    p, ln = _pos(S), S.get('_line')
    if ln in (6, 7):
        return p - 1
    return p


def _seg_color(S, i, v):
    nums = S.get('nums')
    if nums is None or 'now' not in S:
        return None
    u = _upto(S)
    if i > u or u < 0:
        return 'blue' if i == _pos(S) and S.get('_line') in (6, 7) else None
    zs = [k for k in range(u + 1) if nums[k] == 0]
    z = zs[-1] if zs else -1
    z2 = zs[-2] if len(zs) > 1 else -1
    if z < i <= u:
        return 'green'
    if i == z:
        return 'yellow'
    if z2 < i < z:
        return 'purple'
    return None


def _note(S, B):
    ln = S.get('_line')
    last, now = S.get('last'), S.get('now')
    if ln == 10:
        return f"情况 4：`last + 1 + now` = `{last} + 1 + {now}` = =={last + now + 1}==（紫 + 黄 + 绿）"
    if ln == 12:
        return f"情况 1：左边没有 0，只有一整段 1：`now` = =={now}=="
    if ln == 16:
        return f"情况 3：新的 `last` 配上这个 0：`last + 1` = =={last + 1}=="
    return '绿 = now 这一段，黄 = 要翻的 0，紫 = last 那一段'


def _cases(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    ln = S.get('_line')
    cur = {12: 0, 10: 3, 16: 2}.get(ln)
    cv.text((x0 + 18, y0 + 4), '最终答案的 4 种可能（黄框 = 这一步用来更新 res 的情况）', 22, T['muted'], bold=True)
    items = [('① 一整段 1', '左边没有 0：`now`'),
             ('② 1 段左侧翻一个 0', '被 ④ 覆盖，不用单独算'),
             ('③ 1 段右侧翻一个 0', '遇到 0 时：`last + 1`'),
             ('④ 翻中间的 0 合并两段', '遇到 1 且 last 非空：`last + 1 + now`')]
    w = (x1 - x0 - 60) / 2
    for k, (a, b) in enumerate(items):
        X = x0 + 20 + (k % 2) * (w + 20)
        Y = y0 + 44 + (k // 2) * 110
        on = k == cur
        cv.rect((X, Y, X + w, Y + 96), fill=T['panel2'], r=12, outline=T['yellow'] if on else T['border'], width=4 if on else 1)
        cv.text((X + 18, Y + 14), a, 26, T['yellow'] if on else (T['dim'] if k == 1 else T['text']), bold=True)
        cv.rich(X + 18, Y + 52, b, w - 36, size=22, color=T['muted'], accent=T['orange'])


CONFIG = dict(
    num=487, title='最大连续1的个数II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='一趟遍历：now 记当前段，last 记隔一个 0 的前一段',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        last = None
        now = 0
        res = 0
        for num in nums:
            if num == 1:
                now += 1
                if last is not None:
                    res = max(res, last + now + 1)
                else:
                    res = max(res, now)
            else:
                last = now
                now = 0
                res = max(res, last + 1)

        return res
''',
    setup=SETUP,
    call=f'Solution().findMaxConsecutiveOnes(_Nums({NUMS}))',
    expect=6,
    views=[
        dict(type='text', fn=_note, h=60),
        dict(type='array', var=lambda S: list(S['nums']) if 'nums' in S else None, label='nums（最多把一个 0 翻成 1）',
             pointers={'nums.pos': 'blue'}, pointer_labels={'nums.pos': 'num'}, color=_seg_color, cell=100, h=230),
        dict(type='custom', draw=_cases, h=290),
    ],
    watch=[('last', 'last', 'purple'), ('now', 'now', 'green'), ('res', 'res', 'orange')],
    captions={
        'last = None': '`last = None`：当前这段 1 的左边==还没有出现过 0==',
        4: '`now`：当前这一段连续 1 的长度',
        'res = 0': '`res` 记录答案',
        'for num in nums': lambda S, B, ret: (f'看 `nums[{_pos(S)}] = {S.num}`' if _pos(S) != _pos(B) or 'num' not in B else '遍历结束'),
        'if num == 1': lambda S, B, ret: ('是 1 → 当前这段变长' if S.num == 1 else '是 0 → 当前这段结束'),
        'now += 1': '`now` → {now}',
        'if last is not None': lambda S, B, ret: (f'`last = {S.last}`：左边有 0 → 情况 2、4 都可以，==情况 4 更优=='
                                                  if S.last is not None else '`last` 为空：左边没有 0 → 只能用情况 1'),
        'res = max(res, last + now + 1)': '翻转中间的 0，两段合并：`max({B.res}, {last} + {now} + 1)` = =={res}==',
        'res = max(res, now)': '`res = max({B.res}, {now})` = =={res}==',
        'last = now': '遇到 0：当前段变成「隔一个 0 的前一段」：`last = {last}`',
        15: '`now` 清零，重新数',
        'res = max(res, last + 1)': '翻转这个 0 接在 last 后面：`max({B.res}, {last} + 1)` = =={res}==',
        'return res': '最多 =={ret}== 个连续 1',
    },
    cards=dict(
        one_liner='now 记当前一段 1，last 记隔着一个 0 的前一段，last + 1 + now 就是翻转后的长度',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给定二进制数组 `nums`，==最多==可以把一个 `0` 翻转成 `1`',
                 '求最长的连续 `1` 的个数',
                 '示例：`[1,0,1,1,0]` → `4`（翻转第一个 0）',
                 f'本视频：`{NUMS}` → `6`'],
        quote='分别记当前这一段1的数量和跳过之前一个0之后的连续1的数量为now和last，二者的初始值分别为0和none。',
        quote_src='—— yiduobo 题解原文',
        idea=['答案有 4 种可能：① 一整段 1　② 左边翻一个 0　③ 右边翻一个 0　④ 翻中间的 0 合并两段',
              '遇到 1：`now += 1`；`last` 不为空就用情况 4（比 2 更优），否则用情况 1',
              '遇到 0：`last = now`，`now = 0`，新的 `last` 配这个 0 就是情况 3'],
        summary=['时间 `O(n)`，空间 `O(1)`，只遍历一次',
                 '`last` 初值是 `None` 而不是 0：区分「左边没有 0」和「左边有 0 但前一段长度为 0」',
                 '情况 4 包含了情况 2，所以不用单独算',
                 '等价写法：滑动窗口，窗口内最多一个 0',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串；视频里给输入包了一层记录下标的 list 用于画指针'],
    ),
)
