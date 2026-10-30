def _color(S, i, v):
    if v == 'B':
        return 'green'
    if v == 'H':
        return 'blue' if S.get('index') == i else 'orange'
    return None


CONFIG = dict(
    num=2086, title='喂食仓鼠的最小食物桶数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='从左到右 · 桶优先放右边',
    tags=['灵神题单', '难度分 1623'],
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
    call="Solution().minimumBuckets('..HH.H')",
    expect=2,
    views=[
        dict(type='text', fn=lambda S: '橙 = 还没喂的仓鼠，蓝 = 当前仓鼠，绿 B = 已放的食物桶' if 'street_list' in S else ''),
        dict(type='string', var='street_list', pointers={'index': 'blue'}, color=_color, h=300, cell=100),
    ],
    watch=[('index', 'index', 'blue'), ('res', 'res', 'green'), 'n'],
    captions={
        "== 'H'": lambda S, B, r: (f'`street_list[{S.index}]` 是仓鼠，需要看看它有没有桶' if S.street_list[S.index] == 'H'
                                  else f'`street_list[{S.index}]` 是空位，跳过'),
        "== 'B'": lambda S, B, r: ('`index - 1` 处已有桶 → ==这只仓鼠已被左边的桶喂到==，不用再放，直接看下一个'
                                  if S.index > 0 and S.street_list[S.index - 1] == 'B'
                                  else '左边没有桶，这只仓鼠还没被喂到，得为它放一个'),
        "street_list[index + 1] == '.'": lambda S, B, r: ('先试右边：`index + 1` 是空位 → 放右边的桶==还可能顺带喂到下一只==，所以优先放右边'
                                                       if S.index + 1 < len(S.street_list) and S.street_list[S.index + 1] == '.'
                                                       else '先试右边：`index + 1` 越界或是仓鼠，放不了'),
        "street_list[index + 1] = 'B'": '右边放桶：`street_list[{index + 1}] = B`',
        "street_list[index - 1] == '.'": lambda S, B, r: ('右边放不了 → 退而求其次，左边 `index - 1` 是空位，可以放'
                                                       if S.index > 0 and S.street_list[S.index - 1] == '.'
                                                       else '右边放不了，左边也没有空位'),
        "street_list[index - 1] = 'B'": '左边放桶：`street_list[{index - 1}] = B`，只能喂到这一只',
        'return -1': '左右都没有空位可放 → ==这只仓鼠喂不到，无解==，返回 -1',
        'res += 1': '放了一个桶，`res` = {res}',
        'return res': '所有仓鼠都喂到了，最少需要 `{res}` 个桶',
    },
    skip=['street_list = list', 'n = len'],
    cards=dict(
        one_liner='盯住最左边没被喂的仓鼠：桶尽量放它右边',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['字符串里 `H` 是仓鼠，`.` 是空位；桶只能放在空位上，喂饱左右相邻的仓鼠',
                 '求喂饱所有仓鼠的最少桶数，不可能则返回 `-1`',
                 '本视频：`"..HH.H"` → `2`（原题为 hamsters，原文称房子与水桶）'],
        quote='如果其右侧可以安置水桶，那么就应该将水桶安置在其右侧，因为这样一来这个水桶还有可能惠及到下一栋房子。',
        quote_src='—— yiduobo 题解原文',
        idea=['从左往右，考虑最左边还没被喂的仓鼠 `H`',
              '右边能放就放右边：桶可能顺带喂到下一只；放左边只喂一只',
              '右边不行再放左边，两边都不行就返回 `-1`'],
        summary=['时间 `O(n)`，空间 `O(n)`（把字符串转成列表来改）',
                 '易错：先判断 `index - 1` 是不是已有桶 `B`，有就 `continue`',
                 '易错：下标要判断越界，`index + 1 < n`、`index - 1 >= 0`',
                 '`HHH` 这种仓鼠挤在一起、中间没空位的情况会返回 `-1`'],
    ),
)
