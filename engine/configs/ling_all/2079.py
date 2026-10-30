CONFIG = dict(
    num=2079, title='给植物浇水', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='模拟 · 回河边加走 2i 步',
    code='''
class Solution:
    def wateringPlants(self, plants: List[int], capacity: int) -> int:
        ans = len(plants)
        water = capacity
        for i, need in enumerate(plants):
            if water < need:
                ans += i * 2
                water = capacity
            water -= need
        return ans
''',
    call='Solution().wateringPlants([2,2,3,3], 5)',
    expect=14,
    views=[
        dict(type='text', fn=lambda S: f"水罐剩余 `{S['water']}` ／ 容量 `{S['capacity']}`" if 'water' in S else '', size=34),
        dict(type='array', var='plants', pointers={'i': 'blue'}, h=300, label='plants（第 i 株需要的水量）',
             dim=lambda S, i, v: 'i' in S and i < S['i'],
             color=lambda S, i, v: 'blue' if 'i' in S and i == S['i'] else None),
    ],
    watch=[('i', 'i', 'blue'), 'need', ('water', 'water', 'cyan'), ('ans', 'ans', 'green')],
    captions={
        'ans = len': '每株植物至少要走 1 步：`ans = n = {ans}`',
        4: '出发时水罐是满的：`water = {water}`',
        'if water < need': '`water = {water}`，第 `{i}` 株要 `{need}`：{"水不够 → 在位置 i-1 回河边" if water < need else "水够，直接浇"}',
        'ans += i * 2': '去河边再回到 `x={i-1}`，额外走 `2i = {i*2}` 步：`ans` → {ans}',
        8: '在河边重新灌满：`water = {water}`',
        'water -= need': '浇水：`water` → {water}',
        'return ans': '总步数 `{ans}`',
    },
    cards=dict(
        one_liner='先假设每株走 1 步，缺水时再补 2i 步',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['植物在 `x = 0..n-1`，河在 `x = -1`，水罐容量 `capacity`',
                 '浇完一株后水不够下一株，就要回河边灌满再走回来',
                 '示例：`plants=[2,2,3,3], capacity=5` → `14`'],
        quote='如果 water < plants[i]，那么我们在上一个位置 x=i-1 就可以返回 x=-1 重新灌满水，再返回到 x=i-1，需要额外走 2i 步。',
        quote_src='—— 灵茶山艾府题解',
        idea=['由于要浇完所有植物，至少走 `n` 步，所以 `ans` 先设为 `n`',
              '遍历到第 `i` 株，水不够就==额外走 `2i` 步==并把水罐灌满',
              '不用模拟每一步，直接加公式'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '回河边发生在 `i-1`，来回一共 `2i` 步，不是 `2(i+1)`',
                 '`ans` 初值是 `n`（走到各株的基础步数）',
                 '思考题：有 `position` 数组时，改为按位置差累加'],
    ),
)
