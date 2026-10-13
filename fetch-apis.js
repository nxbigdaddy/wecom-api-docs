const https = require('https');
const fs = require('fs');
const path = require('path');

// API列表 - 从企业微信API接口大全.md提取
const apis = [
  // 一、开发指南 - 开发前必读
  { path: '90664', name: '开发前必读', dir: '01-开发指南/开发前必读' },
  { path: '90665', name: '基本概念介绍', dir: '01-开发指南/开发前必读' },
  { path: '91039', name: '获取access_token', dir: '01-开发指南/开发前必读' },
  { path: '90930', name: '回调配置', dir: '01-开发指南/开发前必读' },
  { path: '92520', name: '获取企业微信接口IP段', dir: '01-开发指南/开发前必读' },
  { path: '92521', name: '获取企业微信回调IP段', dir: '01-开发指南/开发前必读' },
  // 二、基础 - 账号ID
  { path: '98728', name: '账号ID概述', dir: '02-基础/账号ID' },
  { path: '95884', name: '自建应用与第三方应用的对接', dir: '02-基础/账号ID' },
  { path: '98729', name: 'tmp_external_userid的转换', dir: '02-基础/账号ID' },
  // 三、通讯录管理 - 概述
  { path: '90193', name: '通讯录管理概述', dir: '03-通讯录管理/概述' },
  // 成员管理
  { path: '100067', name: '成员扩展属性', dir: '03-通讯录管理/成员管理' },
  { path: '90195', name: '创建成员', dir: '03-通讯录管理/成员管理' },
  { path: '90196', name: '读取成员', dir: '03-通讯录管理/成员管理' },
  { path: '90197', name: '更新成员', dir: '03-通讯录管理/成员管理' },
  { path: '90198', name: '删除成员', dir: '03-通讯录管理/成员管理' },
  { path: '90199', name: '批量删除成员', dir: '03-通讯录管理/成员管理' },
  { path: '90200', name: '获取部门成员', dir: '03-通讯录管理/成员管理' },
  { path: '90201', name: '获取部门成员详情', dir: '03-通讯录管理/成员管理' },
  { path: '90202', name: 'userid与openid互换', dir: '03-通讯录管理/成员管理' },
  { path: '90203', name: '登录二次验证', dir: '03-通讯录管理/成员管理' },
  { path: '90975', name: '邀请成员', dir: '03-通讯录管理/成员管理' },
  { path: '91714', name: '获取加入企业二维码', dir: '03-通讯录管理/成员管理' },
  { path: '95402', name: '手机号获取userid', dir: '03-通讯录管理/成员管理' },
  { path: '95895', name: '邮箱获取userid', dir: '03-通讯录管理/成员管理' },
  { path: '96067', name: '获取成员ID列表', dir: '03-通讯录管理/成员管理' },
  // 部门管理
  { path: '90205', name: '创建部门', dir: '03-通讯录管理/部门管理' },
  { path: '90206', name: '更新部门', dir: '03-通讯录管理/部门管理' },
  { path: '90207', name: '删除部门', dir: '03-通讯录管理/部门管理' },
  { path: '90208', name: '获取部门列表', dir: '03-通讯录管理/部门管理' },
  { path: '95350', name: '获取子部门ID列表', dir: '03-通讯录管理/部门管理' },
  { path: '95351', name: '获取单个部门详情', dir: '03-通讯录管理/部门管理' },
  // 标签管理
  { path: '90210', name: '创建标签', dir: '03-通讯录管理/标签管理' },
  { path: '90211', name: '更新标签名字', dir: '03-通讯录管理/标签管理' },
  { path: '90212', name: '删除标签', dir: '03-通讯录管理/标签管理' },
  { path: '90213', name: '获取标签成员', dir: '03-通讯录管理/标签管理' },
  { path: '90214', name: '增加标签成员', dir: '03-通讯录管理/标签管理' },
  { path: '90215', name: '删除标签成员', dir: '03-通讯录管理/标签管理' },
  { path: '90216', name: '获取标签列表', dir: '03-通讯录管理/标签管理' },
  // 异步导入接口
  { path: '90979', name: '异步导入接口概述', dir: '03-通讯录管理/异步导入接口' },
  { path: '90980', name: '增量更新成员', dir: '03-通讯录管理/异步导入接口' },
  { path: '90981', name: '全量覆盖成员', dir: '03-通讯录管理/异步导入接口' },
  { path: '90982', name: '全量覆盖部门', dir: '03-通讯录管理/异步导入接口' },
  { path: '90983', name: '获取异步任务结果', dir: '03-通讯录管理/异步导入接口' },
  // 异步导出接口
  { path: '94850', name: '异步导出接口概述', dir: '03-通讯录管理/异步导出接口' },
  { path: '94849', name: '导出成员', dir: '03-通讯录管理/异步导出接口' },
  { path: '94851', name: '导出成员详情', dir: '03-通讯录管理/异步导出接口' },
  { path: '94852', name: '导出部门', dir: '03-通讯录管理/异步导出接口' },
  { path: '94853', name: '导出标签成员', dir: '03-通讯录管理/异步导出接口' },
  { path: '94854', name: '获取导出结果', dir: '03-通讯录管理/异步导出接口' },
  { path: '94946', name: '导出任务完成通知', dir: '03-通讯录管理/异步导出接口' },
  // 通讯录回调通知
  { path: '90967', name: '通讯录回调通知概述', dir: '03-通讯录管理/通讯录回调通知' },
  { path: '90970', name: '成员变更通知', dir: '03-通讯录管理/通讯录回调通知' },
  { path: '90971', name: '部门变更通知', dir: '03-通讯录管理/通讯录回调通知' },
  { path: '90972', name: '标签变更通知', dir: '03-通讯录管理/通讯录回调通知' },
  { path: '90973', name: '异步任务完成通知', dir: '03-通讯录管理/通讯录回调通知' },
  { path: '96079', name: '通讯录同步接口调整', dir: '03-通讯录管理/通讯录回调通知' },
];

const BASE_URL = 'https://developer.work.weixin.qq.com/document/path/';
const OUTPUT_DIR = path.join(__dirname, 'apis');
const CONCURRENCY = 5; // 并发数

function fetchApi(pathId) {
  return new Promise((resolve, reject) => {
    const url = `${BASE_URL}${pathId}`;
    https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      }
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function extractContent(html, apiName) {
  // 提取标题
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  const title = titleMatch ? titleMatch[1].replace(/\s*-\s*.*$/, '').trim() : apiName;
  
  // 提取主要内容区域
  const contentMatch = html.match(/<article[^>]*>([\s\S]*?)<\/article>/i);
  if (!contentMatch) {
    return `# ${title}\n\n> 内容提取失败，请访问 ${BASE_URL} 查看原文档`;
  }
  
  let content = contentMatch[1];
  
  // 移除script标签
  content = content.replace(/<script[\s\S]*?<\/script>/gi, '');
  // 移除style标签
  content = content.replace(/<style[\s\S]*?<\/style>/gi, '');
  // 移除注释
  content = content.replace(/<!--[\s\S]*?-->/g, '');
  
  // 转换HTML到Markdown
  // 标题
  content = content.replace(/<h1[^>]*>([\s\S]*?)<\/h1>/gi, '\n# $1\n');
  content = content.replace(/<h2[^>]*>([\s\S]*?)<\/h2>/gi, '\n## $1\n');
  content = content.replace(/<h3[^>]*>([\s\S]*?)<\/h3>/gi, '\n### $1\n');
  content = content.replace(/<h4[^>]*>([\s\S]*?)<\/h4>/gi, '\n#### $1\n');
  content = content.replace(/<h5[^>]*>([\s\S]*?)<\/h5>/gi, '\n##### $1\n');
  content = content.replace(/<h6[^>]*>([\s\S]*?)<\/h6>/gi, '\n###### $1\n');
  
  // 粗体和斜体
  content = content.replace(/<strong[^>]*>([\s\S]*?)<\/strong>/gi, '**$1**');
  content = content.replace(/<b[^>]*>([\s\S]*?)<\/b>/gi, '**$1**');
  content = content.replace(/<em[^>]*>([\s\S]*?)<\/em>/gi, '*$1*');
  content = content.replace(/<i[^>]*>([\s\S]*?)<\/i>/gi, '*$1*');
  
  // 代码块
  content = content.replace(/<pre[^>]*><code[^>]*>([\s\S]*?)<\/code><\/pre>/gi, '\n```\n$1\n```\n');
  content = content.replace(/<code[^>]*>([\s\S]*?)<\/code>/gi, '`$1`');
  
  // 链接
  content = content.replace(/<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)');
  
  // 图片
  content = content.replace(/<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*\/?>/gi, '![$2]($1)');
  content = content.replace(/<img[^>]*alt="([^"]*)"[^>]*src="([^"]*)"[^>]*\/?>/gi, '![$1]($2)');
  content = content.replace(/<img[^>]*src="([^"]*)"[^>]*\/?>/gi, '![]($1)');
  
  // 列表
  content = content.replace(/<li[^>]*>([\s\S]*?)<\/li>/gi, '- $1\n');
  content = content.replace(/<ul[^>]*>([\s\S]*?)<\/ul>/gi, '\n$1\n');
  content = content.replace(/<ol[^>]*>([\s\S]*?)<\/ol>/gi, '\n$1\n');
  
  // 段落
  content = content.replace(/<p[^>]*>([\s\S]*?)<\/p>/gi, '\n$1\n');
  
  // 换行
  content = content.replace(/<br\s*\/?>/gi, '\n');
  
  // 表格
  content = content.replace(/<table[^>]*>([\s\S]*?)<\/table>/gi, '\n$1\n');
  content = content.replace(/<thead[^>]*>([\s\S]*?)<\/thead>/gi, '$1\n');
  content = content.replace(/<tbody[^>]*>([\s\S]*?)<\/tbody>/gi, '$1\n');
  content = content.replace(/<tr[^>]*>([\s\S]*?)<\/tr>/gi, '| $1 |\n');
  content = content.replace(/<th[^>]*>([\s\S]*?)<\/th>/gi, '$1 |');
  content = content.replace(/<td[^>]*>([\s\S]*?)<\/td>/gi, '$1 |');
  
  // 移除剩余HTML标签
  content = content.replace(/<[^>]+>/g, '');
  
  // 解码HTML实体
  content = content.replace(/&nbsp;/g, ' ');
  content = content.replace(/&lt;/g, '<');
  content = content.replace(/&gt;/g, '>');
  content = content.replace(/&amp;/g, '&');
  content = content.replace(/&quot;/g, '"');
  content = content.replace(/&#39;/g, "'");
  
  // 清理多余空行
  content = content.replace(/\n{3,}/g, '\n\n');
  content = content.trim();
  
  return `# ${title}\n\n${content}`;
}

function sanitizeFilename(name) {
  return name.replace(/[\\/:*?"<>|]/g, '_').replace(/\s+/g, '_');
}

async function processBatch(batch) {
  const promises = batch.map(async (api) => {
    try {
      const html = await fetchApi(api.path);
      const content = extractContent(html, api.name);
      
      const outputDir = path.join(OUTPUT_DIR, api.dir);
      fs.mkdirSync(outputDir, { recursive: true });
      
      const filename = `${sanitizeFilename(api.name)}.md`;
      const filepath = path.join(outputDir, filename);
      
      fs.writeFileSync(filepath, content, 'utf8');
      console.log(`✓ ${api.dir}/${filename}`);
      
      // 延迟避免请求过快
      await new Promise(resolve => setTimeout(resolve, 300));
    } catch (err) {
      console.error(`✗ ${api.name}: ${err.message}`);
    }
  });
  
  await Promise.all(promises);
}

async function main() {
  console.log(`开始抓取 ${apis.length} 个API接口...\n`);
  
  for (let i = 0; i < apis.length; i += CONCURRENCY) {
    const batch = apis.slice(i, i + CONCURRENCY);
    console.log(`\n--- 批次 ${Math.floor(i / CONCURRENCY) + 1} ---`);
    await processBatch(batch);
  }
  
  console.log('\n=== 抓取完成! ===');
}

main().catch(console.error);
