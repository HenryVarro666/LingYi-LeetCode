R = [["good", "ok", "good", "ok"], ["ok", "bad", "good", "ok", "ok"], ["good"], ["bad"]]
CONFIG = dict(
    num=3527, title='找到最常见的回答', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='set 去重 + Counter 计数',
    tags=[],
    code='''
class Solution:
    def findCommonResponse(self, responses: List[List[str]]) -> str:
        cnt = Counter(s for resp in responses for s in set(resp))
        max_cnt = max(cnt.values())
        return min(s for s, c in cnt.items() if c == max_cnt)
''',
    call='Solution().findCommonResponse(%r)' % (R,),
    expect='good',
    views=[
        dict(type='text', size=26, fn=lambda S: '每天去重后：' + '  '.join('{' + ','.join(sorted(set(r))) + '}' for r in S['responses']) if 'responses' in S else ''),
        dict(type='map', var='cnt', h=330, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', size=30, fn=lambda S: (f"最大次数 `max_cnt` = =={S['max_cnt']}==，候选：" + '、'.join(sorted(s for s, c in S['cnt'].items() if c == S['max_cnt']))) if 'max_cnt' in S else ''),
    ],
    watch=[('max_cnt', 'max_cnt', 'green')],
    captions={
        'cnt = Counter': '每天先 `set(resp)` 去重，再统计：`cnt` = {dict(cnt)}（每个回答最多算每天一次）',
        'max_cnt = max': '最大出现次数 `max_cnt` = =={max_cnt}==',
        'return min': '只在次数等于 `{max_cnt}` 的回答里取字典序最小 → =={ret}==',
    },
    cards=dict(
        one_liner='每天先去重再计数，最后在最高频里取字典序最小',
        complexity='时间 `O(L)`，空间 `O(L)`（L 为所有回答长度之和）',
        problem=['`responses[i]` 是第 `i` 天的回答，先对每天去重',
                 '返回所有天里出现次数最多的回答；次数相同取字典序最小',
                 '示例：`[[good,ok,good,ok],[ok,bad,good,ok,ok],[good],[bad]]` → `good`'],
        quote='把 responses[i] 去重后，用哈希表 cnt 统计每个字符串的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`Counter` 套一个生成器，`set(resp)` 保证同一天同一回答只数一次',
              '`max(cnt.values())` 得到最高次数',
              '`min` 在次数等于最高的回答里取字典序最小，字符串直接比较'],
        after=[dict(heading='写法二', lines=['遍历时同步维护 `max_cnt` 和 `ans`', '`c > max_cnt` 或 （`c == max_cnt` 且 `s < ans`）就更新答案'])],
        summary=['时间 `O(L)`，空间 `O(L)`',
                 '易错：必须==每天去重==，否则同一天重复的回答会多算',
                 '次数相同时取字典序最小：用 `min` 直接比较字符串',
                 '写法二一次遍历，不需要再扫一遍 cnt'],
    ),
)
