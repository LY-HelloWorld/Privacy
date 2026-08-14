# WorkProofCam Product Hunt 与 Press Kit 设计

## 目标

为已经上线的 **WorkProofCam: Photo Report** 准备可公开引用的双语 Press Kit 页面和 Product Hunt 发布素材，并在官网部署后通过 Product Hunt 创建正式产品发布。

本次工作只修改统一静态网站仓库中的 WorkProofCam 专属目录，不修改 iOS 工程、不处理 AlternativeTo，也不开展博客或媒体邮件外联。

## 已确认标识

- App 名称：`WorkProofCam: Photo Report`
- 品牌名称：`WorkProofCam`
- App Store ID：`6775852372`
- App Store URL：`https://apps.apple.com/us/app/workproofcam-photo-report/id6775852372`
- 官网入口：`https://ly-helloworld.github.io/Privacy/workproofcam-web/`
- 公开开发者署名：`Xuemei Huang, Independent iOS Developer`
- 联系邮箱：`luoyi9932@gmail.com`
- 当前版本：`1.1.4`

## 范围边界

所有新增页面和素材必须位于：

```text
workproofcam-web/
```

计划新增：

```text
workproofcam-web/press/index.html
workproofcam-web/press/pt-br/index.html
workproofcam-web/press/assets/app-icon-1024.png
workproofcam-web/press/assets/screens/
workproofcam-web/press/assets/product-hunt/
```

允许为可发现性更新 WorkProofCam 自己的首页导航和现有 sitemap 中对应的 WorkProofCam URL；不得修改其他 App 的页面、资源、文案或实体数据。

## 选择的故事与视觉方向

### 主故事

以“避免施工举证纠纷”为主故事：社区用户反复遇到既有损坏归责、施工前后证据散落、照片缺少时间和位置上下文、离场后仍需整理 PDF 等问题。WorkProofCam 将这些公开用户痛点转化为一个聚焦的 iPhone 工作流。

该故事来源必须表述为公开社区痛点和市场调研，不得写成开发者亲身经历、客户案例或已经验证的用户成功故事。

### 视觉方向

采用已确认的“证据工作流”方向，Product Hunt 五张图按以下顺序组织：

1. 纠纷痛点：在争议发生前保留清晰工作证据。
2. 现场上下文：时间、GPS、地址和照片备注。
3. 工作过程：Before、After 与 General 照片组织。
4. 交付结果：在 iPhone 上生成并分享结构化 PDF。
5. 轻量与隐私：本地优先、无需账号、不是完整施工管理平台。

视觉沿用现有 WorkProofCam 深蓝现场主题、橙色强调色和真实 App 截图，不生成虚构 App 界面，不展示法律认证、防篡改或 C2PA 能力。

## 英文 Press Kit 页面

`workproofcam-web/press/index.html` 是 Product Hunt、媒体和目录引用的英文官方资料页，包含：

- App 名称、图标、当前版本和一句话定位。
- 主故事及其公开社区调研来源说明。
- 已上线功能：带时间和位置上下文的照片、地址、备注、Before/After/General 组织、单张水印照片分享与保存、PDF 导出、本地存储、无需账号。
- 适用人群：承包商、技术人员、巡检人员、清洁、维修维护和小型现场服务团队。
- 明确限制：不是云协作或完整施工管理平台；设备位置可能受权限和信号影响；报告不保证满足法律、保险、合同或工作场所证据要求。
- 1024×1024 图标、真实截图、Product Hunt 图集和示例报告链接。
- App Store、官网、支持、隐私、条款和联系邮箱。
- 开发者署名 `Xuemei Huang, Independent iOS Developer`。
- 可直接复制的 short description、long description 和 factual feature list。

页面入口和核心实体位置需要写有解释设计目的的 HTML 注释，并使用与官网一致的 `SoftwareApplication` 实体标识连接 App Store ID。

## 巴西葡语 Press Kit 页面

`workproofcam-web/press/pt-br/index.html` 提供与英文页事实一致的巴西葡语资料，不做逐字翻译，使用巴西现场服务用户自然表达：

- `relatório de obra com fotos`
- `fotos com data, hora e GPS`
- `antes e depois`
- `prova de serviço realizado`
- `relatório PDF`
- `dados no iPhone, sem conta`

页面保留 `WorkProofCam` 品牌、同一个 App Store ID、开发者署名和官方联系信息。所有功能与限制必须与英文页面一致，不引入额外承诺。

## Product Hunt 发布内容

Product Hunt 使用英文发布，不单独创建葡语 Product Hunt 产品条目。

### 核心字段

- Name：`WorkProofCam`
- 推荐 Tagline：`Turn job-site photos into clear work proof`
- Primary URL：WorkProofCam 官网入口 `https://ly-helloworld.github.io/Privacy/workproofcam-web/`
- Download URL：正确的美国 App Store URL
- Pricing：免费下载安装，提供一次性 Pro 解锁
- Topics：只选择与 iPhone、productivity、photography 和 field work 最匹配的少量主题，以 Product Hunt 当前可选项为准

### 发布材料

- 1024×1024 App 图标。
- 五张采用“证据工作流”的 Product Hunt 图集。
- 260 字以内描述。
- 完整产品说明。
- 开发者首评，说明产品来自公开社区痛点调研，并明确其轻量、本地优先定位。
- 官网作为 Product Hunt 主链接；Press Kit、App Store、隐私和支持作为补充链接或发布正文中的公开资料入口。

不得写入虚假下载量、评分、排名、客户数量、媒体评价或推荐结果。不得把照片水印、EXIF、GPS 或 PDF 描述成密码学防篡改或具有保证性的法律证据。

## 发布流程

1. 在 `Privacy` 仓库实现并本地验证双语 Press Kit 页面与 Product Hunt 资源。
2. 仅暂存本设计范围文件，提交到当前 `main`。
3. 推送统一 `Privacy` 仓库，并等待 GitHub Pages 部署成功。
4. 验证英文和葡语 Press Kit 公开 URL、资源、示例报告和 App Store 链接。
5. 使用已登录浏览器进入 Product Hunt，创建或填写 WorkProofCam 发布草稿。
6. 上传图标和五张图集，填写已确认文案与链接。
7. 在最终点击发布或安排发布日期前，向用户展示关键字段并请求一次操作确认。
8. 用户确认后执行最终发布，并回传公开 Product Hunt URL。

## 验证

### 网站

- 所有新增文件都位于 `workproofcam-web/`。
- HTML 可解析，标题、canonical、Open Graph 和 Twitter 元数据完整。
- JSON-LD 可解析，App Store ID、版本、开发者和 URL 一致。
- 英文与葡语页面互相提供正确的语言入口。
- 所有相对链接和图片资源存在。
- 1024 图标为可读取 PNG 且尺寸正确。
- 五张 Product Hunt 图尺寸一致、文字可读、不拉伸真实截图。
- 桌面和移动宽度无水平溢出，键盘可访问。
- sitemap 只增加 WorkProofCam Press Kit URL，不改变其他 App 条目。

### Product Hunt

- Name、Tagline、Description、Maker comment 与网站事实一致。
- Primary URL、Download URL 和 App Store ID 正确。
- 图标和五张图按确认顺序上传。
- 定价不被描述为订阅。
- 最终发布前完成用户确认。

## 非目标

- 修改或发布 iOS App
- 修改 App Store Connect 元数据
- AlternativeTo、SaaSHub、Capterra 或其他目录提交
- 媒体名单、博客外联、邮件发送或兑换码准备
- 正式新闻稿、虚构采访、用户评价或创始人亲身故事
- 付费推广、购买外链或评分
- 保证 ChatGPT 推荐、Google 排名或下载增长

## 成功标准

- 双语 Press Kit 作为公开、准确、可引用的 WorkProofCam 产品资料页上线。
- 所有公开资源严格隔离在 WorkProofCam 专属目录。
- Product Hunt 发布页使用一致的品牌、App Store ID、真实功能、限制和开发者身份。
- Product Hunt 最终发布成功并获得可公开访问的产品 URL。
- 未修改其他 App 页面，未提交 WorkProofCam iOS 工程中的现有本地变更。
