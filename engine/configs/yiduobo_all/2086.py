CONFIG = dict(
    num=2086, title='喂食仓鼠的最小食物桶数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='从左到右 · 桶优先放右侧 · 直接改列表',
    tags=['贪心与思维', '从最左开始贪心', '难度分 1623'],
    code='''
class Solution(object):
    def minimumBuckets(self, street):

        street_list = list(street)
        res = 0
        n = len(street_list)
        for index in range(n):
            if street_list[index] == 'H':
                if index - 1 >= 0 and street_list[index - 1] == 'B':
                    continue

                if index + 1 < n and street_list[index + 1] == '.':
                    street_list[index + 1] = 'B'
                elif index - 1 >= 0 and street_list[index - 1] == '.':
                    street_list[index - 1] = 'B'
                else:
                    return -1
                
                res += 1
        
        return res
''',
    call='Solution().minimumBuckets("H..H.HH.")',
    expect=3,
    views=[
        dict(type='array', var='street_list', pointers={'index': 'blue'}, label='street_list（B = 已放的桶）', h=230,
             color=lambda S, i, v: 'green' if v == 'B' else ('orange' if v == 'H' else None)),
        dict(type='text', h=70, fn=lambda S: f"已放桶 ==`{S['res']}`== 个" if 'res' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green')],
    captions={
        'street_list = list': '把字符串转成列表，方便直接把 `.` 改成 `B`（桶）',
        "== 'H'": lambda S, B, r: (f'第 {S.index} 位是仓鼠 H，检查它旁边有没有桶' if S.street_list[S.index] == 'H' else f'第 {S.index} 位不是仓鼠，跳过'),
        "== 'B'": lambda S, B, r: ('左边已经是桶 `B` → 这只仓鼠已被喂饱，直接看下一只' if S.street_list[S.index - 1] == 'B' else '左边不是桶 → 需要新放一个'),
        "[index + 1] == '.'": lambda S, B, r: ('右边是空地 → 放右边：这个桶说不定还能喂下一只' if S.index + 1 < S.n and S.street_list[S.index + 1] == '.' else '右边放不了（越界或是仓鼠）→ 试左边'),
        "[index + 1] = 'B'": '右边 `{index + 1}` 放桶',
        "[index - 1] == '.'": lambda S, B, r: ('左边是空地 → 放左边（只能喂这一只）' if S.index - 1 >= 0 and S.street_list[S.index - 1] == '.' else '左右都放不了 → 这只仓鼠无解'),
        "[index - 1] = 'B'": '左边 `{index - 1}` 放桶',
        'return -1': '返回 `-1`：没有地方给它放桶',
        'res += 1': '放了一个桶：`res` → =={res}==',
        'return res': '最少需要 `{ret}` 个桶',
    },
    cards=dict(
        one_liner='先看左边有没有桶，没有就优先往右放',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`H` 是仓鼠，`.` 是空地，桶只能放空地',
                 '仓鼠左边或右边有桶就能被喂食，求最少桶数，无解 `-1`',
                 '示例：`H..H` → `2`；本视频：`H..H.HH.` → `3`'],
        quote='如果其右侧可以安置水桶，那么就应该将水桶安置在其右侧，因为这样一来这个水桶还有可能惠及到下一栋房子。',
        quote_src='—— yiduobo 题解原文',
        idea=['从最左边没有桶的房子开始：左右各放一个桶都能满足它',
              '放右边的桶可能还能喂下一只，放左边只能喂自己 → 优先右边',
              '把桶直接写进列表（`B`），后面的房子看左边就知道有没有桶'],
        summary=['时间 `O(n)`，空间 `O(n)`（拷贝成列表）',
                 '易错点：先判断左边是不是 `B`，再考虑放桶；左右都没空位必须返回 `-1`',
                 '原文为 Python 2 风格，除 `class Solution(object)` 外无需改动，代码一字未改',
                 '对比灵神：灵神只记一个 `bucketPos`，yiduobo 直接在列表里放 B'],
    ),
)
