_P = 'sum(cnt) - (_line == 9) if _line != 10 else None'


def _txt(S):
    if 't' not in S:
        return '要找左边模 60 等于 `(60 − t % 60) % 60` 的数'
    t = S['t']
    need = (60 - t % 60) % 60
    return f"`t = {t}`，`t % 60 = {t % 60}` → 需要左边余数为 `(60 − {t % 60}) % 60` = =={need}=="


CONFIG = dict(
    num=1010, title='总持续时间可被 60 整除的歌曲', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='枚举右，维护左 · 余数计数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def numPairsDivisibleBy60(self, time: List[int]) -> int:
        ans = 0
        cnt = [0] * 60
        for t in time:
            # 先查询 cnt，再更新 cnt，因为题目要求 i<j
            # 如果先更新，再查询，就把 i=j 的情况也考虑进去了
            ans += cnt[(60 - t % 60) % 60]
            cnt[t % 60] += 1
        return ans
''',
    call='Solution().numPairsDivisibleBy60([30,20,150,100,40,60,120])',
    expect=4,
    views=[
        dict(type='array', var='time', label='time（t = 当前歌曲）', pointers={_P: 'blue'}, pointer_labels={_P: 't'}, h=210,
             dim=lambda S, i, v: 'cnt' in S and S.get('_line') != 10 and i > sum(S['cnt']) - (S.get('_line') == 9)),
        dict(type='map', var=lambda S: {r: c for r, c in enumerate(S['cnt']) if c} if 'cnt' in S else {},
             label='cnt 中非零的项：余数 → 左边出现次数', fmt=lambda k, v: f'余{k}: {v}', h=170, font=34),
        dict(type='text', fn=_txt, h=90, size=30),
    ],
    watch=[('t', 't', 'blue'), ('t % 60', 't % 60'), ('ans', 'ans', 'green')],
    captions={
        'ans = 0': '`ans` 统计满足条件的下标对',
        'cnt = [0] * 60': '`cnt[r]`：左边模 60 余 `r` 的歌曲数，只有 60 种余数',
        'for t in time': lambda S, B, r: (f'枚举右边的歌 `t = {S.t}`，把它当作 `time[j]`' if sum(S.cnt) < len(S.time) else '遍历结束'),
        'ans += cnt': lambda S, B, r: ((f'余数 0 要配余数 0：`(60 − 0) % 60 = 0`，左边有 `{S.cnt[0]}` 首 → `ans = {S.ans}`' if S.t % 60 == 0
                                  else f'余数 `{S.t % 60}` 要配 `60 − {S.t % 60}` = =={60 - S.t % 60}==：左边有 `{S.cnt[60 - S.t % 60]}` 首 → `ans = {S.ans}`')),
        'cnt[t % 60] += 1': '再把 `t` 计入：`cnt[{t % 60}]` → `{cnt[t % 60]}`，供右边的歌配对',
        'return ans': '一共 `{ans}` 对',
    },
    cards=dict(
        one_liner='枚举右边的歌，查左边有多少余数能和它凑成 60',
        complexity='时间 `O(n + 60)`，空间 `O(60)`',
        problem=['`time[i]` 是第 i 首歌的秒数，求 `i < j` 且 `(time[i] + time[j]) % 60 == 0` 的对数',
                 '示例：`[30,20,150,100,40]` → `3`',
                 '本视频：`[30,20,150,100,40,60,120]` → `4`'],
        quote='对于 time[i]，需要知道左边有多少个模 60 是 60 − time[i] mod 60 的数。这两种情况可以合并为：累加左边 ==(60 − time[i] mod 60) mod 60== 的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['借鉴两数之和：枚举右边的 `t`，把它看成常量，问题变成「左边有几个」',
              '`t % 60 = 0` 时要配余 0：外面再 `% 60` 就把两种情况合并了',
              '==先查询再更新==，保证只数 `i < j`'],
        summary=['时间 `O(n + 60)`，空间 `O(60)`',
                 '易错：余数为 0 时 `60 − 0 = 60` 会越界，要再 `% 60`',
                 '易错：先更新再查询会把 `i = j` 也算进去',
                 '一句话：两个变量的题，==枚举一个、维护另一个=='],
    ),
)
