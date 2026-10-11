<script setup>
import { ref, computed, onMounted } from 'vue'
import brandLogo from './assets/xinghai-storage-logo.png'
const nav = [{ id:'home', label:'首页' },{ id:'products', label:'产品' },{ id:'support', label:'服务支持' },{ id:'contact', label:'联系' },{ id:'about', label:'关于我们' }]
const page = ref(document.getElementById('app').dataset.page || 'home')
const pageUrl = id => id === 'home' ? '/' : `/${id}/`
const category = ref('全部产品')
const selected = ref(null)
const notice = ref('')
const form = ref({ contact:'', phone:'', company:'', request_type:'企业存储采购', quantity:1, city:'', budget:'待评估', description:'' })
const submitting = ref(false)
const fieldErrors = ref({})
const products = ref([])
const productsLoading = ref(true)
const productsError = ref('')
async function loadProducts(){
  productsLoading.value=true;productsError.value=''
  try{const response=await fetch('/api/products/');if(!response.ok)throw new Error();const data=await response.json();products.value=data.products}
  catch{productsError.value='产品信息加载失败，请稍后重试。'}
  finally{productsLoading.value=false}
}
onMounted(()=>{if(['home','products'].includes(page.value))loadProducts()})

const expanded = {
 home:{tag:'INDUSTRY PERSPECTIVE',title:'同样是数据，不同业务有不同重点',lead:'围绕企业日常运营、生产研发与数字化平台，建立匹配业务节奏的数据基础。',items:[['制造与研发','研发文件、设计资料与生产系统既要便于协作，也需要清晰的版本管理和保护策略。规划时同步考虑工厂与办公环境之间的数据流转。'],['办公与协作','共享文件、业务文档和内部应用是日常运营的基础。按照部门职责、访问频率与保留期限，设计容量、权限与备份策略。'],['数字化业务平台','数据库、虚拟机和业务系统需要稳定的数据承载。识别关键业务、维护窗口和增长趋势，为后续系统扩展预留合理空间。']]},
 products:{tag:'ARCHITECTURE PLANNING',title:'从单一设备，走向完整架构',lead:'设备只是方案的一部分，完整规划需要兼顾连接方式、管理流程与生命周期成本。',items:[['计算与网络匹配','梳理服务器、虚拟化平台与交换网络，确认接口类型、链路带宽及管理网络需求，避免局部性能与整体架构脱节。'],['容量与扩展规划','区分原始容量、可用容量和业务增长预留空间。容量规划应考虑保护策略、快照、备份保留以及扩容时的维护条件。'],['保护与运维设计','为不同数据划分保护等级，明确备份位置和恢复验证方式。同步准备监控、权限、变更管理与故障处理流程。']]},
 support:{tag:'DELIVERY CHECKLIST',title:'让交付成果可以检查、可以接续',lead:'围绕准备、上线与移交建立检查清单，减少实施阶段的信息缺口。',items:[['上线前的环境准备','确认机柜空间、供电、网络端口与地址规划。提前梳理系统版本、兼容性和部署依赖，让实施安排有据可依。'],['上线中的验证记录','按照确认的方案检查设备、网络、存储资源与业务连接。保留配置记录和验收结果，便于后续维护与问题追溯。'],['上线后的管理移交','整理资产清单、配置说明、权限交接与日常巡检事项。结合实际需要安排管理培训和恢复验证计划。']]},
 contact:{tag:'PROJECT COLLABORATION',title:'提交之后，如何推进项目沟通',lead:'表单用于整理项目线索；具体联系安排与交付范围需在后续沟通中确认。',items:[['需求澄清','围绕使用场景、现有环境和交付地点确认需求。预算尚未确定时，可选择“待评估”，优先梳理项目目标。'],['方案讨论','根据容量、负载和业务连续性要求讨论产品方向，并确认设备数量、实施边界与服务需求。'],['交付确认','将配置、价格、交付周期及验收方式写入正式方案。表单提交不构成采购合同或交付承诺。']]},
 about:{tag:'WORKING PRINCIPLES',title:'把专业落实到每一次项目协作',lead:'星海存储围绕企业数据基础设施建立内容与服务方向，强调清晰、务实和可持续。',items:[['先理解，再设计','理解业务流程与数据使用方式，再讨论设备配置。将需求、条件与限制写清楚，让技术选择服务于实际目标。'],['以文档形成共识','通过需求记录、配置清单和交付文档减少信息误差。方案调整应有明确依据，重要决定应可追溯。'],['以验证支持判断','对容量、兼容性和恢复能力采用明确的验证方法。未经实际验证的指标不作为项目承诺，具体能力以正式资料为准。']]}
}
const guides = {
 home:{tag:'PROJECT ROADMAP',title:'一条清晰的数据基础设施建设路径',items:[['梳理现状','盘点业务系统、数据规模、资源利用情况与运维痛点，明确需要解决的问题。'],['明确优先级','区分关键业务与一般业务，结合项目预算确定建设顺序和阶段目标。'],['设计与落地','从产品选型、部署计划到迁移验证，形成可执行的建设方案。'],['持续评估','关注容量增长、运行状态与恢复演练结果，及时调整资源与管理策略。']]},
 products:{tag:'SELECTION GUIDE',title:'产品方向与业务需求对照',items:[['性能敏感型业务 → 全闪存储','适用于需要重点评估访问延迟与并发负载的业务。具体性能需要依据实际配置与工作负载验证。'],['综合业务承载 → 混合存储','适合同时考虑容量和预算的规划方向。确认不同数据的访问热度，讨论资源分层与管理策略。'],['持续增长的数据 → 分布式存储','当容量和访问需求持续增长时，重点评估扩展方式、网络条件与管理复杂度。'],['业务连续性 → 备份与容灾','从恢复目标出发，讨论备份周期、保留策略、异地保护与恢复演练，不以备份任务成功代替恢复验证。']]},
 support:{tag:'OPERATIONS GUIDE',title:'日常运维中值得持续关注的事项',items:[['容量趋势','定期检查容量利用率和增长速度，关注快照、备份与归档占用，提前规划扩容窗口。'],['健康与告警','查看硬件健康、链路状态与系统告警，记录异常发生时间及关联业务影响。'],['变更与版本','维护配置基线和变更记录。升级前确认兼容性、验证方案与回退条件。'],['恢复演练','结合业务优先级定期验证恢复流程，确认数据完整性和应用可用性，记录改进事项。']]},
 contact:{tag:'INQUIRY FAQ',title:'填写需求前，您可能关心这些问题',items:[['暂时没有完整配置，可以提交吗？','可以。先提供使用场景、数量估计和项目目标，在需求说明中注明尚待确认的内容。'],['预计数量应怎样填写？','按计划采购的设备或项目套数填写正整数。若数量尚不确定，可填写初步估计，并在需求说明中解释。'],['预算区间有什么用途？','预算帮助明确可讨论的方案范围，并不代表最终报价。正式价格以双方确认的配置与服务内容为准。'],['提交的信息如何使用？','需求信息存储于网站后台，用于项目沟通。请只提供必要的联系人和业务信息，避免上传账户密码或敏感数据。']]},
 about:{tag:'LONG-TERM VIEW',title:'面向业务增长，保留演进空间',items:[['架构具有可理解性','清晰说明数据在哪里、如何访问和如何保护，让企业团队能够接续管理。'],['交付具有可检查性','以确认的方案和验收项目为依据，检查实施结果并记录需要继续完善的事项。'],['管理具有连续性','通过文档、培训与维护记录减少对个人经验的依赖，形成稳定的日常管理方式。'],['合作具有明确边界','坦诚说明实施条件、责任分工与服务范围，以正式约定作为项目推进依据。']]}
}
const filtered = computed(() => category.value === '全部产品' ? products.value : products.value.filter(p => p.type === category.value))
async function save(){
  if(submitting.value) return
  submitting.value=true; notice.value=''; fieldErrors.value={}
  try {
    const ready = await fetch('/api/inquiries/', { credentials:'same-origin' })
    if(!ready.ok) throw new Error('暂时无法提交，请稍后重试。')
    const { csrf_token: token } = await ready.json()
    const response = await fetch('/api/inquiries/', { method:'POST', credentials:'same-origin', headers:{'Content-Type':'application/json','X-CSRFToken':decodeURIComponent(token || '')}, body:JSON.stringify(form.value) })
    const result = await response.json().catch(()=>({message:'服务器未能处理请求，请刷新页面后重试。'}))
    if(!response.ok){ fieldErrors.value=result.errors || {}; throw new Error(result.message || '提交失败，请稍后重试。') }
    notice.value=`需求提交成功，编号 XH-${result.id}。您可保留编号供后续沟通。`
    form.value={contact:'',phone:'',company:'',request_type:'企业存储采购',quantity:1,city:'',budget:'待评估',description:''}
  } catch(error){notice.value=error.message || '网络异常，请稍后重试。'}
  finally{submitting.value=false}
}
</script>

<template>
  <div>
    <header class="header"><div class="container header-inner"><a class="brand" href="/"><img class="brand-logo" :src="brandLogo" alt="星海存储 XINGHAI STORAGE" width="2000" height="800"></a><nav aria-label="主导航"><a v-for="item in nav" :key="item.id" :href="pageUrl(item.id)" :class="{active:page===item.id}" :aria-current="page===item.id?'page':undefined">{{item.label}}</a></nav></div></header>
    <main>
      <template v-if="page==='home'">
        <section class="hero"><div class="container hero-content"><p class="eyebrow">ENTERPRISE DATA INFRASTRUCTURE</p><h1>让数据稳健运行<br>让业务持续向前</h1><p class="hero-description">面向企业关键业务的存储与数据保护方案。<br>从架构规划到运维支持，让每一份数据都有可靠的承载。</p><div class="actions"><a href="/products/" class="button">探索存储产品 <span>↗</span></a><a href="/contact/" class="text-link">沟通您的需求 →</a></div><div class="hero-caption">企业级存储 / 数据保护 / 全生命周期服务</div></div></section>
        <div class="principles container"><div><span>01</span><strong>围绕业务设计</strong><p>从实际工作负载出发</p></div><div><span>02</span><strong>面向长期演进</strong><p>兼顾当前需求与未来增长</p></div><div><span>03</span><strong>贯穿数据生命周期</strong><p>从存储到保护与恢复</p></div></div>
        <section class="section container"><div class="section-heading"><div><p class="eyebrow">PORTFOLIO</p><h2>为不同业务，找到合适的存储</h2></div><a href="/products/" class="inline-link">查看全部产品 →</a></div><p v-if="productsLoading" role="status">正在加载产品…</p><div v-else-if="productsError" role="alert"><p>{{productsError}}</p><button class="inline-link" @click="loadProducts">重新加载</button></div><p v-else-if="!products.length">暂无已上架产品，欢迎联系我们讨论需求。</p><div class="product-grid"><a v-for="(p,i) in products" :key="p.id" href="/products/" class="product-card"><img v-if="p.image" class="product-image" :src="p.image" :alt="p.name"><div v-else class="hardware" aria-hidden="true"><div v-for="row in 3" :key="row" class="rack"><i v-for="slot in 8" :key="slot"></i><b></b></div><span>{{p.code}}</span></div><div class="card-body"><small>0{{i+1}} / {{p.type}}</small><h3>{{p.name}} <span>↗</span></h3><p>{{p.desc}}</p></div></a></div></section>
        <section class="dark-section"><div class="container split"><div><p class="eyebrow">BUSINESS SCENARIOS</p><h2>数据的价值，<br>始于业务的连续性。</h2><p>存储架构不只是容量的选择。我们围绕访问方式、业务优先级与恢复目标，梳理企业的数据需求。</p><a href="/contact/" class="text-link">讨论您的业务场景 →</a></div><div class="scenario-list"><article v-for="(s,i) in [['核心业务平台','关注数据库与业务系统的性能、可用性和维护窗口。'],['企业协作与文件管理','围绕共享访问、权限管理和数据增长规划文件服务。'],['备份归档与业务恢复','依据数据保留周期与恢复目标，建立可验证的保护流程。']]" :key="s[0]"><span>0{{i+1}}</span><div><h3>{{s[0]}}</h3><p>{{s[1]}}</p></div></article></div></div></section>
        <section class="section container split"><div><p class="eyebrow">SERVICE & SUPPORT</p><h2>交付之后，服务仍在继续。</h2><p>从需求梳理、方案设计到上线与持续运维，以清晰的流程帮助团队管理数据基础设施。</p><a class="inline-link" href="/support/">了解服务体系 →</a></div><div class="steps"><div v-for="(s,i) in ['需求评估与架构规划','部署交付与迁移协助','运维指导与恢复验证']" :key="s"><span>0{{i+1}}</span><h3>{{s}}</h3></div></div></section>
      </template>
      <template v-else-if="page==='products'">
        <section class="page-intro"><div class="container"><p class="eyebrow">PRODUCT PORTFOLIO</p><h1>企业存储产品</h1><p>从关键应用到海量数据，按照业务负载选择合适的存储方向。</p></div></section>
        <section class="section container"><div class="filters" aria-label="产品分类"><button v-for="c in ['全部产品',...new Set(products.map(p=>p.type))]" :key="c" :class="{chosen:category===c}" @click="category=c">{{c}}</button></div><p v-if="productsLoading" role="status">正在加载产品…</p><div v-else-if="productsError" role="alert"><p>{{productsError}}</p><button class="inline-link" @click="loadProducts">重新加载</button></div><p v-else-if="!products.length">暂无已上架产品，欢迎联系我们讨论需求。</p><div class="product-grid two"><article v-for="p in filtered" :key="p.id" class="product-card"><img v-if="p.image" class="product-image" :src="p.image" :alt="p.name"><div v-else class="hardware"><div v-for="row in 3" :key="row" class="rack"><i v-for="slot in 8" :key="slot"></i><b></b></div><span>{{p.code}}</span></div><div class="card-body"><small>{{p.type}}</small><h3>{{p.name}}</h3><p>{{p.desc}}</p><ul class="feature-list"><li v-for="f in p.features" :key="f">{{f}}</li></ul><button class="inline-link" @click="selected=selected===p.id?null:p.id" :aria-expanded="selected===p.id">{{selected===p.id?'收起选型说明 −':'查看选型说明 + '}}</button><div v-if="selected===p.id" class="detail"><p>{{p.selection_notes || "选型前建议明确容量增长、并发负载、可用性要求及预算。具体配置、兼容性和服务范围应以正式方案为准。"}}</p><a href="/contact/">沟通产品需求 →</a></div></div></article></div><div class="editorial"><h2>选型，先从正确的问题开始</h2><div class="three"><div><h3>业务负载</h3><p>识别访问模式、读写比例与峰值压力，避免只按容量选择设备。</p></div><div><h3>数据增长</h3><p>梳理未来数据增长、保留周期与扩展路径，规划长期使用成本。</p></div><div><h3>保护目标</h3><p>明确可接受的数据损失范围与恢复时间，设计备份与容灾策略。</p></div></div></div><p class="disclaimer">本页面为产品方向展示，非具体型号规格或性能承诺。</p></section>
      </template>
      <template v-else-if="page==='support'">
        <section class="page-intro"><div class="container"><p class="eyebrow">SERVICE & SUPPORT</p><h1>专业支持，贯穿每个阶段</h1><p>以可执行的流程，让规划、交付和日常管理更清晰。</p></div></section>
        <section class="section container"><div class="three service-cards"><article v-for="s in [['01','咨询与规划','梳理业务负载、容量与保护目标，形成架构建议、选型依据和交付边界。'],['02','部署与交付','协助环境检查、部署配置和迁移规划，结合验收清单确认上线准备。'],['03','运维与保护','提供日常管理建议、问题定位思路和恢复演练规划，帮助形成可持续的运维机制。']]" :key="s[0]"><span>{{s[0]}}</span><h3>{{s[1]}}</h3><p>{{s[2]}}</p></article></div><div class="editorial split"><div><p class="eyebrow">SUPPORT PROCESS</p><h2>问题有记录，处理有路径。</h2><p>提交问题时，请整理环境版本、故障现象、发生时间及近期变更。日志分享前应清除密码与敏感业务数据。</p><a href="/contact/" class="button">联系服务团队 ↗</a></div><ol class="process"><li v-for="s in [['提交与确认','整理问题描述，确认受影响范围与业务优先级。'],['分析与定位','结合环境信息、日志和复现条件逐步排查。'],['处理与验证','记录处理步骤，验证恢复情况及业务状态。'],['回顾与预防','总结原因与改进建议，更新运维记录。']]" :key="s[0]"><h3>{{s[0]}}</h3><p>{{s[1]}}</p></li></ol></div><h2>常见问题</h2><div class="faq"><details v-for="q in [['选型前需要准备哪些信息？','建议准备当前数据量、年增长预估、业务系统类型、访问方式、预算及恢复目标。'],['迁移过程中如何评估业务影响？','先梳理依赖关系、兼容性和迁移窗口，再制定验证与回退计划。具体流程应按实际环境确定。'],['如何验证备份是否有效？','除了检查备份任务状态，还应定期执行恢复演练并记录恢复时间、数据完整性与应用可用性。'],['服务响应时间如何约定？','响应时间、覆盖时段与交付范围应以双方确认的服务协议为准。']]" :key="q[0]"><summary>{{q[0]}}</summary><p>{{q[1]}}</p></details></div></section>
      </template>
      <template v-else-if="page==='contact'">
        <section class="page-intro"><div class="container"><p class="eyebrow">LET’S TALK</p><h1>从一次沟通开始</h1><p>告诉我们您的业务场景，让存储规划更贴近实际需求。</p></div></section>
        <section class="section container contact-grid"><div><h2>您的下一步，<br>可以更清晰。</h2><p>无论是新建平台、容量扩展，还是数据保护规划，都可以先整理当前环境与目标。</p><div class="contact-note"><h3>沟通前建议准备</h3><ul><li>现有系统与存储架构</li><li>数据规模及增长趋势</li><li>性能与业务恢复目标</li><li>项目时间计划与预算范围</li></ul></div><p class="disclaimer">品牌与页面内容为展示方案。公开联系电话、邮箱和办公地址待企业确认后补充。您可以使用右侧表单提交项目需求。</p></div><form @submit.prevent="save"><h3>提交项目需求</h3><p>请填写项目基本信息，需求将提交至星海存储管理后台。</p><div class="form-row"><label>联系人 *<input v-model="form.contact" required maxlength="60" autocomplete="name" placeholder="联系人姓名"></label><label>联系电话 *<input v-model="form.phone" type="tel" required maxlength="30" pattern="[+0-9()\s-]{6,30}" autocomplete="tel" placeholder="手机或固定电话"></label></div><label>公司/品牌 *<input v-model="form.company" required maxlength="120" autocomplete="organization" placeholder="公司或品牌名称"></label><div class="form-row"><label>需求类型 *<select v-model="form.request_type"><option v-for="x in ['企业存储采购','存储扩容升级','备份与容灾','方案咨询','其他需求']" :key="x">{{x}}</option></select></label><label>预计数量 *<input v-model.number="form.quantity" type="number" min="1" max="1000000" required><small>以设备或项目套数估算，最终数量在方案中确认。</small></label></div><div class="form-row"><label>交付城市 *<input v-model="form.city" required maxlength="80" placeholder="例如：上海市"></label><label>预算区间 *<select v-model="form.budget"><option v-for="x in ['5万元以下','5–20万元','20–50万元','50–100万元','100万元以上','待评估']" :key="x">{{x}}</option></select></label></div><label>需求说明 *<textarea v-model="form.description" required maxlength="3000" rows="6" placeholder="请描述存储容量、使用场景、交付时间及其他要求"></textarea></label><p>请勿填写密码或敏感业务数据。提交的信息用于项目需求沟通。</p><button class="button" type="submit" :disabled="submitting">{{submitting?'正在提交…':'提交项目需求'}} <span>→</span></button><p v-if="notice" class="notice" role="status">{{notice}}</p><ul v-if="Object.keys(fieldErrors).length" class="form-errors"><li v-for="(errors,key) in fieldErrors" :key="key">{{errors.map(e=>e.message).join('；')}}</li></ul></form></section>
      </template>
      <template v-else>
        <section class="page-intro"><div class="container"><p class="eyebrow">ABOUT XINGHAI</p><h1>专注数据，着眼长远</h1><p>让复杂的数据基础设施，回归清晰的业务目标。</p></div></section>
        <section class="section container split about"><div class="about-image" role="img" aria-label="现代数据中心机房"></div><div><p class="eyebrow">OUR APPROACH</p><h2>可靠，来自每一个<br>经过思考的决定。</h2><p>星海存储是本官网方案的示例品牌，围绕企业存储、数据保护与基础设施服务展开内容设计。</p><p>我们倡导从真实业务需求出发，把架构、交付与运维作为一个整体考虑。技术选择应有依据，扩展路径应清晰，数据保护应经过验证。</p><p class="disclaimer">企业历史、资质、团队与客户案例待真实资料提供后补充。</p></div></section><section class="section soft"><div class="container"><p class="eyebrow">VALUES</p><h2>以务实的方式，建立长期信任</h2><div class="three"><article v-for="s in [['业务优先','让每一项技术选择回应具体的业务需求，而不是堆砌参数。'],['透明沟通','明确方案边界、实施条件与维护成本，让决策有据可依。'],['持续改进','通过验证、记录和复盘，让基础设施随业务一起成长。']]" :key="s[0]"><h3>{{s[0]}}</h3><p>{{s[1]}}</p></article></div></div></section><section class="section container"><h2>合作从理解彼此开始</h2><p>业务邮箱：<a class="inline-link" href="mailto:1483110216@qq.com">1483110216@qq.com</a></p><p>欢迎围绕存储建设、平台升级与数据保护展开沟通，共同梳理目标与实施路径。</p><a class="inline-link" href="/contact/">联系与合作 →</a></section>
      </template>
      <section class="section soft"><div class="container"><p class="eyebrow">{{expanded[page].tag}}</p><h2>{{expanded[page].title}}</h2><p class="section-lead">{{expanded[page].lead}}</p><div class="three"><article v-for="item in expanded[page].items" :key="item[0]" class="expanded-card"><h3>{{item[0]}}</h3><p>{{item[1]}}</p></article></div></div></section>
      <section class="section container"><div class="section-heading"><div><p class="eyebrow">{{guides[page].tag}}</p><h2>{{guides[page].title}}</h2></div></div><div class="guidance-list"><article v-for="(item,i) in guides[page].items" :key="item[0]"><span>0{{i+1}}</span><div><h3>{{item[0]}}</h3><p>{{item[1]}}</p></div></article></div></section>
      <section class="cta" v-if="page!=='contact'"><div class="container"><div><p class="eyebrow">BUILD A STRONGER FOUNDATION</p><h2>为下一阶段的业务，做好数据准备。</h2></div><a href="/contact/" class="button light">沟通项目需求 ↗</a></div></section>
    </main>
    <footer><div class="container footer-top"><a class="brand" href="/"><img class="brand-logo" :src="brandLogo" alt="星海存储 XINGHAI STORAGE" width="2000" height="800"></a><p>企业存储 · 数据保护 · 专业服务</p><a href="/contact/">联系与合作 ↗</a></div><div class="container footer-bottom"><span>© {{new Date().getFullYear()}} 星海存储 · 官网展示方案</span><span>专注数据基础设施的长期价值</span></div></footer>
  </div>
</template>

