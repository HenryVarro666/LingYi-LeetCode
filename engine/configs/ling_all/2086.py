CONFIG = dict(
    num=2086, title='喂食仓鼠的最小食物桶数', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='从左到右贪心 · 优先放右侧（Go 原文转写）',
    tags=['贪心与思维', '从最左开始贪心', '难度分 1623'],
    code='''
class Solution:
    def minimumBuckets(self, street: str) -> int:
        ans = 0
        bucketPos = -2  # 上一个水桶的放置位置
        for i, ch in enumerate(street):
            if ch == 'H':  # 遍历每个房屋
                if bucketPos == i - 1:  # 左侧已有水桶，不做任何处理
                    pass
                elif i + 1 < len(street) and street[i + 1] == '.':  # 贪心：先考虑在右侧放水桶
                    bucketPos = i + 1
                    ans += 1
                elif i > 0 and street[i - 1] == '.':  # 再考虑在左侧放水桶
                    ans += 1
                else:  # 左右均无空位，无解
                    return -1
        return ans
''',
    call='Solution().minimumBuckets(".HH.H.H.")',
    expect=3,
    views=[
        dict(type='string', var='street', pointers={'i': 'blue', 'bucketPos': 'green'}, label='street（蓝 = 当前，绿 = 上个桶）', h=220,
             color=lambda S, i, v: 'orange' if v == 'H' and 'i' in S and i == S['i'] else None),
        dict(type='text', h=70, fn=lambda S: f"已放桶 ==`{S['ans']}`== 个" if 'ans' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('bucketPos', 'bucketPos', 'green'), ('ans', 'ans', 'orange')],
    captions={
        'ch ==': lambda S, B, r: (f'第 {S.i} 位是仓鼠 H，需要左或右有桶' if S.ch == 'H' else f'第 {S.i} 位是空地，跳过'),
        'bucketPos == i - 1': lambda S, B, r: (f'上个桶在 `{S.bucketPos}` = 仓鼠左边 → 已被喂饱，不用处理' if S.bucketPos == S.i - 1 else f'上个桶在 `{S.bucketPos}`，不在仓鼠 `{S.i}` 旁边 → 需要新放一个'),
        'street[i + 1] ==': lambda S, B, r: (f'右边 `{S.i + 1}` 是空地 → 优先放右边，它还可能顺便喂下一只仓鼠' if S.i + 1 < len(S.street) and S.street[S.i + 1] == '.' else f'右边 `{S.i + 1}` 不能放（越界或是仓鼠）→ 试左边'),
        'bucketPos = i + 1': '记下桶的位置 `bucketPos = {bucketPos}`',
        'street[i - 1] ==': lambda S, B, r: (f'左边 `{S.i - 1}` 是空地 → 放左边（这个桶只能喂这一只）' if S.i > 0 and S.street[S.i - 1] == '.' else f'左边也没有空地 → 无解'),
        'ans += 1': '桶数 `ans` → =={ans}==',
        'return -1': '左右都没空位 → 这只仓鼠无解，返回 `-1`',
        'return ans': '最少需要 `{ret}` 个桶',
    },
    cards=dict(
        one_liner='先放右边，让一个桶有机会喂两只',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`H` 是仓鼠，`.` 是空地；桶只能放空地',
                 '仓鼠左边或右边有桶就能被喂食，求最少桶数，无解返回 `-1`',
                 '示例：`H..H` → `2`；本视频：`.HH.H.H.` → `3`'],
        quote='贪心：先考虑在右侧放水桶；再考虑在左侧放水桶；左右均无空位，无解。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['从左到右处理每只仓鼠，若左边已有桶就跳过',
              '否则优先放右侧：右侧的桶还能喂到下一只仓鼠，左侧的桶只对当前有用',
              '只记录「上个桶的位置」，不需要修改字符串'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n)`，空间 `O(1)`',
                 '易错点：先判断左侧是否已有桶；`HHH` 这类左右都无空位要返回 `-1`',
                 '放左侧时不用更新 `bucketPos`：该桶不会再喂后面的仓鼠'],
    ),
)
