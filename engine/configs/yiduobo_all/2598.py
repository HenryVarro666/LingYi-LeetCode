CONFIG = dict(
    num=2598, title='执行操作后的最大 MEX', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按余数分 value 类 · 一轮一轮填',
    tags=['灵神题单', '数学算法', '难度分 1846'],
    code='''
class Solution(object):
    def findSmallestInteger(self, nums, value):

        cnt = {}
        for v in nums:
            if v >= 0:
                r = v % value
            else:
                r = (-v) % value
                if r > 0:
                    r = value - r
            
            cnt[r] = cnt.get(r, 0) + 1
        
        mi_freq = None
        mi_r = None
        for r in range(value):
            if mi_freq is None or cnt.get(r, 0) < mi_freq:
                mi_freq = cnt.get(r, 0)
                mi_r = r

        return mi_freq * value + mi_r
''',
    call='Solution().findSmallestInteger([1,-6,-4,3,5,2,7,9], 3)',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（value = 3）', h=170),
        dict(type='map', var='cnt', label='cnt：余数 → 个数', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"目前个数最少的是余数 =={S['mi_r']}==，只有 =={S['mi_freq']}== 个" if S.get('mi_r') is not None
                           else '每个数先归到 0..value−1 的某一类')),
    ],
    watch=['v', 'r', ('mi_freq', 'mi_freq', 'orange'), ('mi_r', 'mi_r', 'pink')],
    captions={
        'cnt = {}': '`cnt[r]`：余数为 `r` 的数有几个',
        'if v >= 0': lambda S, B, ret: (f'`{S.v} >= 0`，直接取模' if S.v >= 0 else f'`{S.v}` 是负数，要单独处理余数'),
        'r = v % value': '`{v} % {value}` = `{r}`',
        'r = (-v) % value': '负数：先对 `-v = {-v}` 取模，得 `{r}`',
        'if r > 0': lambda S, B, ret: (f'`r = {S.r} > 0` → 要换成 `value - r`，才是 `{S.v}` 真正的余数' if S.r > 0
                                       else '`r = 0`，整除，余数就是 0'),
        'r = value - r': '`r = {value} - 旧 r` = `{r}`',
        'cnt[r] = cnt.get': '余数 `{r}` 的个数 → `{cnt[r]}`',
        'mi_freq = None': '`mi_freq` 记最少的个数，`mi_r` 记对应的余数',
        'mi_r = None': '`mi_r = None`：还没有候选',
        'for r in range(value)': lambda S, B, ret: ('所有余数都检查完了' if 'r' in B and B.r == S.r and 'mi_r' in B and B.get('mi_r') == S.mi_r and S.r == S.value - 1 and 'v' in S and B.r == S.r and S._line == B._line else f'检查余数 `{S.r}`'),
        'if mi_freq is None': lambda S, B, ret: (f'`mi_freq` 还没有值，先记下余数 {S.r}（{S.cnt.get(S.r, 0)} 个）' if S.mi_freq is None
            else (f'余数 {S.r} 有 {S.cnt.get(S.r, 0)} 个 `< {S.mi_freq}` → 更少，更新' if S.cnt.get(S.r, 0) < S.mi_freq
                  else f'余数 {S.r} 有 {S.cnt.get(S.r, 0)} 个，不少于 {S.mi_freq} → 不更新（并列保留较小余数）')),
        'mi_freq = cnt.get': '`mi_freq` → {mi_freq}',
        'mi_r = r': '`mi_r` → {mi_r}',
        'return': '一共能完整填 `{mi_freq}` 轮，第 {mi_freq+1} 轮在 `{mi_r}` 处断：`{mi_freq} × {value} + {mi_r}` = =={ret}==',
    },
    cards=dict(
        one_liner='把数按余数分成 value 类，一轮一轮地填 0,1,2…',
        complexity='时间 `O(n+value)`，空间 `O(value)`',
        problem=['每次可对任一元素加或减 `value`',
                 '求任意次操作后数组能达到的最大 MEX',
                 '本视频：`nums=[1,-6,-4,3,5,2,7,9], value=3` → `7`'],
        quote='接下来，需要使用这些数从0开始填充这个数组。如果以value个数为一轮，那么就意味着这value类数都需要出一份力。',
        quote_src='—— yiduobo 题解原文',
        idea=['操作不改变对 value 的余数，先分成 value 类',
              '第一轮填 0..value−1，第二轮填 value..2value−1，每轮每类出一个',
              '某类先用完，那一轮就缺数：答案 `mi_freq * value + mi_r`'],
        summary=['时间 `O(n+value)`，空间 `O(value)`',
                 '负数余数：`(-v) % value` 后用 `value - r` 换算，余数为 0 时不换',
                 '并列时用严格小于，保留较小的余数',
                 '原文无需改动 Python 3'],
    ),
)
