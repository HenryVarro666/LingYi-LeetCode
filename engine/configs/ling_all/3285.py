CONFIG = dict(
    num=3285, title='找到稳定山的下标', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='枚举左邻居 · 列表推导式',
    code='''
class Solution:
    def stableMountains(self, height: List[int], threshold: int) -> List[int]:
        return [i for i, h in enumerate(height[:-1], 1) if h > threshold]
''',
    call='Solution().stableMountains([10,1,10,1,10,2,2], 3)',
    expect=[1, 3, 5],
    views=[
        dict(type='array', var='height', label='height（第 i 座山的左邻居是 height[i-1]）', pointers={'i': 'blue'},
             color=lambda S, i, v: ('green' if v > S['threshold'] else 'pink') if 'threshold' in S and 'i' in S and i == S['i'] - 1 else None,
             h=300),
        dict(type='text', size=28, h=90,
             fn=lambda S: '配对 `(i, h)`：' + ' '.join(f"`({i+1},{h})`" for i, h in enumerate(S['height'][:-1]))),
        dict(type='text', size=30, h=90,
             fn=lambda S: '`h > ' + str(S['threshold']) + '` 的 i：==' + str([i+1 for i, h in enumerate(S['height'][:-1]) if h > S['threshold']]) + '=='),
    ],
    watch=['threshold'],
    captions={
        'return [i for': '`enumerate(height[:-1], 1)`：把 `height[0..n-2]` 配上下标 `1..n-1`，`h` 就是第 `i` 座山的==左邻居==；`h > {threshold}` 的 `i` 收进答案，最终得到 =={ret}==',
    },
    cards=dict(
        after=[dict(heading='逐个配对看一遍', lines=['`enumerate(height[:-1], 1)` 产生：', '`(1, height[0])`、`(2, height[1])`、…、`(n-1, height[n-2])`', '每一对里 `h` 是 `i` 的左邻居，`h > threshold` 就保留 `i`', '结果顺序天然从小到大，题目允许任意顺序'])],
        one_liner='枚举左邻居，高于阈值就把右边那座山记下来',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['第 `i` 座山稳定：它左边相邻的山高度 `> threshold`（严格大于）',
                 '下标 0 的山没有左邻居，永远不稳定',
                 '示例：`[10,1,10,1,10], threshold=3` → `[1,3]`'],
        quote='遍历下标 0 到 n-2，如果发现 height[i]>threshold，就说明 i+1 是稳定的，加入答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['换个角度：不看山自己，看它==左边那座==',
              '`height[:-1]` 去掉最后一座（它没有右邻居），下标从 1 开始配对',
              '一行列表推导式完成筛选'],
        summary=['时间 `O(n)`，空间 `O(1)`（Python 忽略切片空间）',
                 '易错点：条件是严格大于，等于阈值不算',
                 '易错点：别把左邻居的下标 `i-1` 当成答案，答案是 `i`'],
    ),
)
