CONFIG = dict(
    num=1196, title='最多可以买到的苹果数量', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='排序 · 先拿最轻的',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def maxNumberOfApples(self, weight):

        cnt = 0
        res = 0
        for w in sorted(weight):
            if cnt + w > 5000:
                break

            cnt += w
            res += 1
        
        return res
''',
    call='Solution().maxNumberOfApples([900,950,800,1000,700,800])',
    expect=5,
    views=[
        dict(type='array', var='weight', label='weight（原顺序）', h=170),
        dict(type='bars', var='sorted(weight)', label='排序后，依次放进篮子', h=330,
             color=lambda S, i, v: 'green' if i < S.get('res', 0) else None, vmax=1000),
        dict(type='text', fn=lambda S: (f"篮子已装 `{S['cnt']}` / 5000，装了 `{S['res']}` 个" if 'cnt' in S and 'res' in S else ''), size=30, h=70),
    ],
    watch=[('cnt', 'cnt', 'blue'), ('res', 'res', 'green'), 'w'],
    captions={
        'cnt = 0': '`cnt` 是篮子当前的总重量',
        'res = 0': '`res` 是已经装进去的苹果个数',
        'for w in sorted': '先排序，==从最轻的苹果开始拿==：这一个重 `{w}`',
        'if cnt + w > 5000': lambda S, B, r: (f'`{S.cnt} + {S.w} = {S.cnt + S.w} > 5000` → 装不下，更重的更装不下 → ==停止==' if S.cnt + S.w > 5000
                                              else f'`{S.cnt} + {S.w} = {S.cnt + S.w} <= 5000` → 还装得下'),
        'break': '后面的苹果只会更重，直接结束',
        'cnt += w': '装进去：总重 `cnt` → =={cnt}==',
        'res += 1': '个数 `res` → =={res}==',
        'return res': '最多装 `{res}` 个',
    },
    cards=dict(
        one_liner='要的是个数不是重量，所以先拿最轻的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['篮子最多承重 `5000`，每个苹果重 `weight[i]`',
                 '求篮子里最多能装多少个苹果',
                 '示例：`[900,950,800,1000,700,800]` → `5`'],
        quote='题目只是要求买到的苹果数量最多，并不是要求重量最大，因此在这里就应该优先选择重量较小的苹果。',
        quote_src='—— yiduobo 题解原文',
        idea=['同样装 k 个，选最轻的 k 个总重最小，最容易装得下',
              '把重量从小到大排序，一个个往篮子里放',
              '放不下就停：后面的只会更重'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '判断条件是 `cnt + w > 5000` 才停，恰好等于 5000 还能装',
                 '原文本身可直接在 Python 3 运行，没有改动',
                 '题面库里没有，题意按 LeetCode 1196 与原文整理'],
    ),
)
