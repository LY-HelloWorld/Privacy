# HomeInventory 问题型内容页设计

## 目标

为已经上线的 iOS App 建立三个可独立回答自然语言问题的英文页面，帮助搜索系统和 ChatGPT 更准确地理解产品适用场景，并把访客送到 App Store 中唯一正确的应用实体。

本次只建设内容页、实体关联和站点发现入口，不修改 iOS App、不接入网站分析、不承诺 GPT 推荐或排名提升。

## 产品身份

所有新页面使用同一组产品身份：

- App Store 名称：`Moving Boxes Organizer`
- 网站品牌名：`HomeInventory`
- 对用户的统一写法：`Moving Boxes Organizer by HomeInventory`
- App Store ID：`6766885651`
- App Store 发布者：`雪梅 黄`
- App Store 地址：`https://apps.apple.com/us/app/moving-boxes-organizer/id6766885651`
- 产品主页：`https://ly-helloworld.github.io/Privacy/HomeInventory_web/`

每个页面的可见页脚、Smart App Banner、下载按钮和结构化数据必须指向同一 App Store ID，避免与其他同名 HomeInventory 应用混淆。

## 页面范围

### 1. How to Keep Track of What Is Inside Moving Boxes

路径：

`HomeInventory_web/how-to-keep-track-of-moving-boxes/index.html`

用户问题：

搬家过程中箱子不断增加，纸条、手机备忘录和人的记忆容易分散；用户需要一个以后仍然找得到的简单记录方式。

页面回答：

1. 给每个箱子一个清楚名称和房间。
2. 装箱时记录箱内物品，不要求写成长清单。
3. 对难描述、易碎或贵重物品补充照片和简短备注。
4. 封箱后保留可搜索记录。
5. 用 HomeInventory 把上述信息放在同一个箱子记录中。

主要截图：

- `02_record_box_in_seconds_1260x2736.png`
- `06_unpack_what_matters_first_1260x2736.png`

### 2. How to Find an Item Without Opening Every Box

路径：

`HomeInventory_web/find-items-without-opening-boxes/index.html`

用户问题：

用户知道物品已经装箱，却不知道具体在哪一箱；“Kitchen”或“Bedroom”只能说明目的房间，无法定位某一件东西。

页面回答：

1. 搜索物品名称或备注。
2. 查看匹配的箱子和房间。
3. 找到正确箱子后再开箱。
4. 如果人在箱子旁边，也可以扫描箱子标签查看记录。

主要截图：

- `01_find_without_opening_1260x2736.png`
- `03_print_stick_scan_1260x2736.png`

### 3. How to Label Storage Boxes So You Can Find Things Later

路径：

`HomeInventory_web/qr-labels-for-storage-boxes/index.html`

用户问题：

普通标签空间有限，内容变化后容易过时；堆放后的箱子也不适合反复打开确认。

页面回答：

1. 箱子外面保留人能直接读懂的名称和房间。
2. 用可打印标签连接到对应箱子记录。
3. 扫描后查看物品、照片和备注。
4. 箱内内容变化时更新记录，不必重新把全部内容写在纸标签上。

主要截图：

- `03_print_stick_scan_1260x2736.png`
- `02_record_box_in_seconds_1260x2736.png`

## 共用页面结构

三个页面使用同一套轻量结构和现有 `HomeInventory_web/styles.css`，不引入 JavaScript 框架或第三方依赖：

1. 顶部导航：返回 HomeInventory、相关指南、App Store。
2. 首屏：直接回答页面标题对应的问题，并提供 App Store 下载按钮。
3. 问题说明：用生活化场景说明为什么常见办法不够。
4. 简单方法：提供三到五个可以立即执行的步骤。
5. HomeInventory 如何解决：把真实产品能力映射到这些步骤。
6. 真实截图：只使用当前 App Store 1.3.0 截图，保持 `1260:2736` 原始比例。
7. 适用边界：说明页面适用于搬家箱、储物箱、车库、衣柜和季节性物品；不把产品描述成仓库或企业库存系统。
8. 相关指南：三篇页面互相链接，并返回产品主页。
9. 底部 CTA：再次显示准确产品名称和 App Store ID。

## 文案规则

- 页面语言为美式英文。
- 先说用户问题和结果，再说功能。
- 不出现 Reddit、竞品、研究来源、GPT、SEO、Schema、爬虫或排名等后台过程。
- 不使用未经验证的数字、用户评价、下载量、节省时间或“最佳 App”等比较性声明。
- 不声称 QR 标签本身包含完整库存；只描述为打开对应箱子记录的入口。
- 不声称云端自动同步所有私人库存；家庭共享只按当前 App 已实现的共享库存能力描述。
- 不暗示保险机构认可导出文件。
- 不展示价格数字，避免与不同市场或后续版本不一致。

## 发现与实体关联

产品主页和三个问题页共同使用一个 `SoftwareApplication` 实体 ID：

`https://ly-helloworld.github.io/Privacy/HomeInventory_web/#app`

主页补充：

- 正式名称 `Moving Boxes Organizer`
- 备用名称 `HomeInventory`
- 标识符 `6766885651`
- 发布者 `雪梅 黄`
- 精确 App Store URL

每个问题页使用 `WebPage`、`BreadcrumbList` 和同一个 `SoftwareApplication` 引用。根目录 `sitemap.xml` 增加三个页面并把主页 `lastmod` 更新为 `2026-08-12`；`HomeInventory_web/sitemap.xml` 同步包含四个页面。

根目录 `robots.txt` 已允许所有抓取，不需要修改。

## 视觉设计

- 延续当前产品页的白色、浅灰和深绿色视觉系统。
- 问题页以正文可读性为主，不复制首页的大型截图墙。
- 桌面端采用正文与单张截图的双栏首屏；移动端改为单栏。
- 所有截图明确设置 `width: 100%`、`height: auto` 和 `object-fit: contain`。
- 不旋转问题页截图，避免文字阅读受影响。
- 每页最多展示两张截图，控制下载体积和视觉噪音。

## 验证

实现完成后必须检查：

1. HTML 标签闭合、相对链接和本地资源存在。
2. 页面正文没有 Reddit、竞品、GPT、SEO 或虚构数据。
3. 三个页面的 canonical、Open Graph、Smart App Banner 和下载按钮均指向正确地址。
4. 结构化数据可以解析，三个页面都引用同一个 App 实体。
5. 根 Sitemap 和 HomeInventory Sitemap 均包含四个页面。
6. 使用桌面 `1440×1100` 和移动端 `390×844` 实际渲染。
7. 浏览器中每张截图的渲染比例与原始 `1260:2736` 比例误差不超过 `0.001`。
8. GitHub Pages 发布后，四个页面、样式和截图均返回 HTTP 200。

## 不在本次范围

- 网站访问统计和 App Store 点击统计。
- GPT 推荐基准采集与确定性指标计算。
- App 内评价请求逻辑调整。
- App Store metadata 或截图顺序调整。
- ChatGPT Apps SDK 集成。
