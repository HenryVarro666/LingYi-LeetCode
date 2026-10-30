CONFIG = dict(
    num=1996, title='游戏中弱角色的数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='攻击降序 · 同攻防御升序',
    code='''
class Solution:
    def numberOfWeakCharacters(self, properties: List[List[int]]) -> int:
        properties.sort(key=lambda p: (-p[0], p[1]))
        ans = max_def = 0
        for _, d in properties:
            if d < max_def: ans += 1
            else: max_def = d
        return ans
''',
    call='Solution().numberOfWeakCharacters([[1,5],[10,4],[4,3],[4,6],[4,2],[7,7]])',
    expect=4,
    views=[
        dict(type='array', var='properties', label='properties（攻击, 防御）', fmt=lambda v: f'{v[0]},{v[1]}', cell=140, h=170,
             color=lambda S, i, v: None),
        dict(type='text', fn=lambda S: (f"当前防御 `d = {S['d']}`，前面防御最大值 `max_def = {S['max_def']}`" if 'd' in S else '先按 (−攻击, 防御) 排序'), h=60),
    ],
    watch=[('d', 'd', 'blue'), ('max_def', 'max_def', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'properties.sort': '攻击从大到小；攻击相同时防御==从小到大==：排序后 `{properties}`',
        'ans = max_def = 0': '`ans` 弱角色数，`max_def` 已遍历角色的最大防御，都从 0 开始',
        'for _, d in properties': '依次看角色，防御 `d = {d}`，前面的角色攻击都不小于它',
        'if d < max_def': '`d = {d}` 与 `max_def = {max_def}`：{"前面有防御更高的角色，它攻击必然更高 → 弱角色" if d < max_def else "前面没有防御更高的 → 不是弱角色"}',
        'ans += 1': '是弱角色：`ans` → {ans}',
        'max_def = d': '不是弱角色，`max_def` 更新为 `{max_def}`（同攻击时防御升序，不会把同攻击的角色误判成弱）',
        'return ans': '弱角色一共 `{ans}` 个',
    },
    cards=dict(
        one_liner='攻击降序排好，只需看前面最大的防御',
        complexity='时间 `O(n log n)`，空间 `O(1)`（不计排序栈）',
        problem=['每个角色有攻击和防御；若另一角色的攻击、防御都==严格==更高，该角色就是弱角色',
                 '求弱角色的数量',
                 '示例：`[[1,5],[10,4],[4,3]]` → `1`；本视频用 6 个角色 → `4`'],
        quote='将角色按照攻击从大到小排序，攻击相同的按照防御从小到大排序。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，能压制当前角色的只可能在它前面',
              '前面若有防御更高的 q：攻击相同时 q 排在后面，所以 q 的攻击必然更高，当前角色是弱角色',
              '只用维护前面的最大防御 `max_def`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错点：==攻击相同时防御要升序==，否则同攻击的角色会被误判为弱角色',
                 '不弱的角色才更新 `max_def`；弱角色的防御本来就小于它'],
    ),
)
