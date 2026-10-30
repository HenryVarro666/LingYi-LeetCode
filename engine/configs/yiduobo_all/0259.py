def _cnt(S):
    c = S.get('cnt')
    if c is None:
        return {}
    return {v - 100: n for v, n in enumerate(c) if n}


def _pre(S):
    s = S.get('s')
    c = S.get('cnt')
    if not s or len(s) < 201 or c is None:
        return {}
    return {f'<={v - 100}': s[v] for v in range(201) if c[v]}


def _txt(S):
    if 'res' not in S:
        return '先把数值加 100 变成非负下标，`target` 加 300'
    return f'已统计的三元组数 `res` = =={S["res"]}==（下标 = 数值 + 100）'


CONFIG = dict(
    num=259, title='较小的三数之和', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='计数 + 前缀和 · 三类三元组',
    tags=[],
    code='''
class Solution(object):
    def threeSumSmaller(self, nums, target):

        cnt = [0] * 201
        for num in nums:
            cnt[num + 100] += 1

        target += 300

        s = [cnt[0]]
        for v in range(1, 201):
            s.append(s[-1] + cnt[v])

        res = 0
        for x in range(0, min(200, target) + 1):
            if cnt[x] >= 3 and x * 3 < target:
                res += cnt[x] * (cnt[x] - 1) * (cnt[x] - 2) // 6

            if cnt[x] >= 2 and x * 2 < target:
                r = target - x * 2
                tmp = s[r - 1]
                if r - 1 >= x:
                    tmp -= cnt[x]
                res += (cnt[x] * (cnt[x] - 1) // 2) * tmp

            if cnt[x] > 0:
                for y in range(x + 1, min(200, target - x) + 1):
                    if cnt[y] > 0:
                        r = target - x - y
                        if r > y:
                            res += cnt[x] * cnt[y] * (s[r - 1] - s[y])

        return res
''',
    call='Solution().threeSumSmaller([1,1,1,0,0,-1,2], 4)',
    expect=32,
    max_events=60000,
    skip=['for num in nums', 'for v in range', 's.append', 'for x in range', 'if cnt[x] >= 3', 'if cnt[x] >= 2',
          'if cnt[x] > 0', 'for y in range', 'if cnt[y] > 0'],
    views=[
        dict(type='text', h=70, size=30, fn=_txt),
        dict(type='map', var=_cnt, label='cnt：数值 → 出现次数（只列出现过的）', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
        dict(type='map', var=_pre, label='前缀和 s：小于等于该数值的个数', fmt=lambda k, v: f'{k}: {v}', h=170, font=32),
    ],
    watch=['x', 'y', 'r', ('res', 'res', 'green')],
    captions={
        'cnt = [0]': '数值范围 -100..100，用长 201 的数组 `cnt` 计数',
        'cnt[num + 100] += 1': '数值加 100 变成下标，`cnt` 统计出现次数',
        'target += 300': '三个数各加了 100，所以 `target` 加 300 → `{target}`',
        's = [cnt[0]]': '`s` 是 `cnt` 的前缀和（循环已跑完）：`s[v]` = 下标不超过 v 的数的个数',
        'res = 0': '`res` 累计合法三元组个数；下面按三种情况枚举 `x`',
        'res += cnt[x] * (cnt[x] - 1) * (cnt[x] - 2)': '情况 1：三个数都是 `{x-100}`，从 `{cnt[x]}` 个里选 3 个：C({cnt[x]},3) → `res` = =={res}==',
        'r = target - x * 2': '情况 2：两个 `{x-100}`，第三个数下标必须 `< r = {r}`',
        'tmp = s[r - 1]': '下标 `< {r}` 的数共 `{tmp}` 个',
        'if r - 1 >= x': lambda S, B, ret: ('`r - 1 >= x`：这些数里包含 x 本身，要扣掉' if S.r - 1 >= S.x
                                           else '`r - 1 < x`：x 不在其中，不用扣'),
        'tmp -= cnt[x]': '第三个数不能等于 x（那是情况 1）：扣掉 `{cnt[x]}` 个 → `tmp = {tmp}`',
        'res += (cnt[x] * (cnt[x] - 1) // 2) * tmp': '情况 2：C({cnt[x]},2) × `{tmp}` → `res` = =={res}==',
        'r = target - x - y': '情况 3：三个互不相同，规定 x<y<v；v 的下标必须 `< r = {r}`',
        'if r > y': lambda S, B, ret: (f'`r = {S.r} > y = {S.y}`：v 在 `y+1 .. r-1`，有候选' if S.r > S.y
                                       else f'`r = {S.r} <= y = {S.y}`：没有比 y 大又小于 r 的数'),
        'res += cnt[x] * cnt[y] * (s[r - 1] - s[y])': '用前缀和求区间：`cnt[x]·cnt[y]·(s[r-1] − s[y])` = `{cnt[x]}·{cnt[y]}·({s[r-1]} − {s[y]})` → `res` = =={res}==',
        'return res': '一共 `{res}` 个三元组',
    },
    cards=dict(
        one_liner='值域很小：计数 + 前缀和，三种三元组分别数',
        complexity='时间 `O(V²)`（V = 值域大小 201），空间 `O(V)`',
        problem=['给整数数组 `nums` 和 `target`，数有多少个下标三元组 `i<j<k` 满足 `nums[i]+nums[j]+nums[k] < target`',
                 '示例：`[-2,0,1,3]`，`target=2` → `2`',
                 '本视频：`[1,1,1,0,0,-1,2]`，`target=4` → `32`'],
        quote='可以将三元组分成三类：1、三个相同的数。2、两个相同的数和另一个不同的数。3、最后一种情况就是三个不同的数。',
        quote_src='—— yiduobo 题解原文',
        idea=['直接枚举 x、y 再查前缀和会重复算，所以按「相同的个数」分类',
              '三同：C(cnt,3)；两同：C(cnt,2) × 小于 r 且不等于 x 的个数',
              '三不同：规定 x<y<v，用 `s[r-1] − s[y]` 数 v 的个数'],
        summary=['时间 `O(V²)`，与数组长度无关，空间 `O(V)`',
                 '先把数值加 100、`target` 加 300，才能当下标用',
                 '情况 2 里第三个数不能等于 x，所以要减 `cnt[x]`',
                 '原文为 Python 2 写法，其中的整数除法 `/` 已改为 `//`',
                 '本视频略去了循环里不满足条件的空转步骤，只演示命中的分支'],
    ),
)
