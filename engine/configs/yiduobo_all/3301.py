CONFIG = dict(
    num=3301, title='高度互不相同的最大塔高和', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='降序 + 变量 now 记上一座',
    tags=['贪心', '排序', '难度分 1448'],
    code='''
class Solution(object):
    def maximumTotalSum(self, maximumHeight):

        maximumHeight.sort(reverse=True)
        now = maximumHeight[0]
        s = now

        for h in maximumHeight[1:]:
            if now > h:
                now = h
            else:
                now -= 1
                if now == 0:
                    return -1
            
            s += now
        
        return s
''',
    call='Solution().maximumTotalSum([2,3,4,3,5])',
    expect=15,
    views=[
        dict(type='bars', var='maximumHeight', h=380, label='上限（降序）'),
        dict(type='text', fn=lambda S: (f"上一座高度 `now` = =={S['now']}==，已累计 `s` = =={S['s']}==" if 'now' in S else ''), size=28),
    ],
    watch=[('now', 'now', 'blue'), ('h', 'h', 'pink'), ('s', 's', 'green')],
    captions={
        'sort(reverse': '从大到小排序：`{maximumHeight}`，方便处理同高的情况',
        'now = maximumHeight[0]': '最高的塔顶格设置：`now` = `{now}`，它就是上一座塔的高度',
        's = now': '累计和 `s` = `{s}`',
        'for h in': '下一座塔上限 `h` = `{h}`',
        'if now > h': '上限 `{h}` 比上一座 `{now}` 矮吗？→ {"是，可以顶格" if now > h else "不是，会撞高度"}',
        'now = h': '顶格安排：`now` 降到 `{h}`',
        'now -= 1': '上限 `{h}` ≥ 上一座，只能比上一座矮 1：`now` = =={now}==',
        'now == 0': '`now` = `{now}`：{"没法设置高度 → 返回 -1" if now == 0 else "还是正整数，可以放"}',
        's += now': '这座塔高 `{now}` 加入总和：`s` = {B.s} + {now} = =={s}==',
        'return s': '总高度 =={ret}==',
    },
    cards=dict(
        one_liner='排序后用 now 记上一座高度，撞高就减 1',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`maximumHeight[i]` 是第 `i` 座塔的高度上限',
                 '高度必须是正整数且互不相同，求最大总高度，无解返回 `-1`',
                 '示例：`[2,3,4,3]` → `10`'],
        quote='最理想的情况自然是所有塔都能达到其高度上限。但是还有一个条件是不能出现相同高度的塔，那么当两座塔高度相同时，就不得不降低其中一座塔的高度。',
        quote_src='—— yiduobo 题解',
        idea=['先按上限降序排序，同高的塔就挨在一起',
              '不必统计同高塔的数量，只用变量 `now` 表示上一座的高度',
              '`h < now` 就顶格并更新 `now`；否则 `now` 减 1，减到 0 就无解'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '`now == 0` 时无解，要立刻返回 `-1`',
                 '`now > h` 才顶格，`h >= now` 要减 1',
                 '第一座塔不进循环，要先把 `s = now` 算上'],
    ),
)
