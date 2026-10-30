CONFIG = dict(
    num=2833, title='距离原点最远的点', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='遍历统计位置', tags=['难度分 1294'],
    code='''
class Solution(object):
    def furthestDistanceFromOrigin(self, moves):

        cnt = 0
        now = 0
        for char in moves:
            if char == '_':
                cnt += 1
            elif char == 'L':
                now -= 1
            else:
                now += 1
        
        if now >= 0:
            now += cnt
        else:
            now -= cnt
        
        return abs(now)
''',
    call="Solution().furthestDistanceFromOrigin('_R__LL_')",
    expect=5,
    views=[
        dict(type='string', var='moves', h=200, label='moves',
             color=lambda S, i, v: 'yellow' if v == '_' else ('blue' if v == 'R' else 'pink')),
        dict(type='text', h=130, size=34, fn=lambda S: (
            f"当前位置 now = =={S['now']}==，空位 `_` 共 =={S['cnt']}== 个" if 'now' in S else '')),
    ],
    watch=[('char', 'char'), ('cnt', 'cnt', 'yellow'), ('now', 'now', 'blue')],
    captions={
        'for char': '读下一个字符 `char = {char!r}`',
        "char == '_'": '`char = {char!r}`：是下划线吗？ → {char == "_"}',
        'cnt += 1': '下划线方向可以自己选，先记账：`cnt = {cnt}`',
        'now -= 1': '`L` 不能改，位置左移：`now = {now}`',
        'now += 1': '`R` 不能改，位置右移：`now = {now}`',
        'if now >= 0': '`now = {now}`：在正半轴或原点就继续向右走，否则向左走',
        'now += cnt': '`now` 在右侧 → 把 `{cnt}` 个下划线都向右走：`now = {now}`',
        'now -= cnt': '`now` 在左侧 → 把 `{cnt}` 个下划线都向左走：`now = {now}`',
        'return': '位置可正可负，题目要的是距离：`abs({now})` = =={ret}==',
    },
    cards=dict(
        one_liner='L 和 R 改不了，下划线全部顺着当前方向走',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`moves` 里 `L`/`R` 固定方向，`_` 可左可右',
                 '求走完后离原点最远的距离',
                 '示例：`_R__LL_` → `5`'],
        quote='序列中的下划线可以人工控制，但是L和R是无法变更的，于是可以先一趟遍历，使用变量cnt统计下划线出现的次数，同时根据L和R计算当前的下标位置now。',
        quote_src='—— yiduobo 题解',
        idea=['一趟遍历：`_` 只计数，`L`/`R` 直接改位置 `now`',
              '遍历完再看 `now`：在正半轴就向右加 `cnt`，否则向左减 `cnt`',
              '最后 `abs(now)` 就是最远距离'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`now == 0` 时向左向右都一样，代码里归到向右',
                 '与“L/R 计数相减”等价，只是用位置 `now` 来表达',
                 '原文已是 Python 3 可运行写法，未改动'],
    ),
)
