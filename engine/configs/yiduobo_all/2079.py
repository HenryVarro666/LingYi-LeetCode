CONFIG = dict(
    num=2079, title='给植物浇水', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 累计已用水量',
    code='''
class Solution(object):
    def wateringPlants(self, plants, capacity):

        now = 0
        res = 0
        for index in range(len(plants)):
            if now + plants[index] > capacity:
                res += index + index
                now = 0
            
            now += plants[index]
        
        res += len(plants)
        return res
''',
    call='Solution().wateringPlants([1,1,1,4,2,3], 4)',
    expect=30,
    views=[
        dict(type='text', fn=lambda S: f"已用水量 `{S['now']}` ／ 容量 `{S['capacity']}`" if 'now' in S else '', size=34),
        dict(type='array', var='plants', pointers={'index': 'blue'}, h=300, label='plants',
             dim=lambda S, i, v: 'index' in S and i < S['index'],
             color=lambda S, i, v: 'blue' if 'index' in S and i == S['index'] else None),
    ],
    watch=[('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        4: '`now`：当前这一轮已经用掉的水',
        'res = 0': '`res` 累计步数',
        'if now + plants': '已用 `{now}` + 本株 `{plants[index]}` = `{now + plants[index]}`，容量 `{capacity}`：{"不够 → 这一轮结束，回河边" if now + plants[index] > capacity else "够，继续浇"}',
        'res += index + index': '这一轮走到 `plants[{index-1}]` 再回河边，共 `{index} + {index}` 步：`res` → {res}',
        9: '回河边装满，已用水量清零',
        'now += plants': '浇水：`now` → {now}',
        'res += len': '最后一轮不会被记录，补上 `n = {len(plants)}`：`res` → {res}',
        'return res': '总步数 `{res}`',
    },
    cards=dict(
        one_liner='每轮的路程 = 回河边的往返，最后一轮补上 n',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['植物排成一行，河在 `x=-1`，水不够下一株就要回河边灌满',
                 '求浇完全部植物走的总步数',
                 '本视频：`plants=[1,1,1,4,2,3], capacity=4` → `30`'],
        quote='如果当前剩余的水量不能满足该植物，那么这一轮浇水的路径就是从河边走到plants[index - 1]，然后再返回河边打水，一共走了index + index的路程。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `now` 记录这一轮已经用掉多少水',
              '`now + plants[index] > capacity` 说明装不下，上一轮结束',
              '最后一轮没有回河边，遍历后再统一加上 `n`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '最后一轮不会被记录，别忘了 `res += len(plants)`',
                 '原文用「已用水量」，灵神用「剩余水量」，思路等价',
                 '回河边的路程是 `index + index`，对应位置 `index-1` 往返'],
    ),
)
