#!/usr/bin/env node
const fs = require('fs');

function main() {
  const [, , inPath, outPath] = process.argv;
  const data = JSON.parse(fs.readFileSync(inPath, 'utf8'));
  const fileNodes = data.fileNodes || [];
  const importEdges = data.importEdges || [];
  const allEdges = data.allEdges || [];

  const idToNode = {};
  fileNodes.forEach(n => { idToNode[n.id] = n; });
  const pathOf = n => n.filePath || n.id.split(':').slice(1).join(':');

  // Common prefix of directories
  const paths = fileNodes.map(pathOf);
  function commonPrefix(arr) {
    if (!arr.length) return '';
    const segs = arr.map(p => p.split('/').slice(0, -1));
    let prefix = [];
    const first = segs[0] || [];
    for (let i = 0; i < first.length; i++) {
      const s = first[i];
      if (segs.every(g => g[i] === s)) prefix.push(s); else break;
    }
    return prefix.length ? prefix.join('/') + '/' : '';
  }
  const prefix = commonPrefix(paths);

  // A. Directory grouping
  const directoryGroups = {};
  const fileToGroup = {};
  fileNodes.forEach(n => {
    let p = pathOf(n);
    let rel = prefix && p.startsWith(prefix) ? p.slice(prefix.length) : p;
    const parts = rel.split('/');
    let group = parts.length > 1 ? parts[0] : (prefix ? prefix.replace(/\/$/, '') || 'root' : 'root');
    if (!directoryGroups[group]) directoryGroups[group] = [];
    directoryGroups[group].push(n.id);
    fileToGroup[n.id] = group;
  });

  // B. Node type grouping
  const nodeTypeGroups = {};
  fileNodes.forEach(n => {
    (nodeTypeGroups[n.type] = nodeTypeGroups[n.type] || []).push(n.id);
  });

  // C. Fan in/out
  const fanIn = {}, fanOut = {};
  fileNodes.forEach(n => { fanIn[n.id] = 0; fanOut[n.id] = 0; });
  importEdges.forEach(e => {
    if (fanOut[e.source] !== undefined) fanOut[e.source]++;
    if (fanIn[e.target] !== undefined) fanIn[e.target]++;
  });

  // D. Cross-category edges
  const crossMap = {};
  allEdges.forEach(e => {
    const s = idToNode[e.source], t = idToNode[e.target];
    if (!s || !t) return;
    if (s.type === t.type) return;
    const key = s.type + '|' + t.type + '|' + e.type;
    crossMap[key] = (crossMap[key] || 0) + 1;
  });
  const crossCategoryEdges = Object.entries(crossMap).map(([k, count]) => {
    const [fromType, toType, edgeType] = k.split('|');
    return { fromType, toType, edgeType, count };
  });

  // E. Inter-group imports
  const interMap = {};
  importEdges.forEach(e => {
    const a = fileToGroup[e.source], b = fileToGroup[e.target];
    if (a === undefined || b === undefined || a === b) return;
    const key = a + '|' + b;
    interMap[key] = (interMap[key] || 0) + 1;
  });
  const interGroupImports = Object.entries(interMap).map(([k, count]) => {
    const [from, to] = k.split('|');
    return { from, to, count };
  });

  // F. Intra-group density
  const intraGroupDensity = {};
  Object.keys(directoryGroups).forEach(g => {
    let internal = 0, total = 0;
    importEdges.forEach(e => {
      const a = fileToGroup[e.source], b = fileToGroup[e.target];
      if (a === g || b === g) {
        total++;
        if (a === g && b === g) internal++;
      }
    });
    intraGroupDensity[g] = { internalEdges: internal, totalEdges: total, density: total ? +(internal / total).toFixed(2) : 0 };
  });

  // G. Pattern matching
  const dirPatterns = [
    [/^(routes|api|controllers|endpoints|handlers|serializers|routers|blueprints|controller)$/, 'api'],
    [/^(services|core|lib|domain|logic|signals|composables|mailers|jobs|channels)$/, 'service'],
    [/^(models|db|data|persistence|repository|entities|migrations|entity|sql|database)$/, 'data'],
    [/^(components|views|pages|ui|layouts|screens)$/, 'ui'],
    [/^(middleware|plugins|interceptors|guards)$/, 'middleware'],
    [/^(utils|helpers|common|shared|tools|pkg|templatetags)$/, 'utility'],
    [/^(config|constants|env|settings|management|commands)$/, 'config'],
    [/^(__tests__|test|tests|spec|specs)$/, 'test'],
    [/^(types|interfaces|schemas|contracts|dtos|dto|request|response)$/, 'types'],
    [/^hooks$/, 'hooks'],
    [/^(store|state|reducers|actions|slices)$/, 'state'],
    [/^(assets|static|public)$/, 'assets'],
    [/^(cmd|bin|internal)$/, 'entry'],
    [/^(docs|documentation|wiki)$/, 'documentation'],
    [/^(deploy|deployment|infra|infrastructure|k8s|kubernetes|helm|charts|terraform|tf|docker)$/, 'infrastructure'],
    [/^(\.github|\.gitlab|\.circleci)$/, 'ci-cd'],
    [/^(providers)$/, 'service'],
    [/^(llm)$/, 'service'],
    [/^(api)$/, 'service'],
  ];
  const patternMatches = {};
  Object.keys(directoryGroups).forEach(g => {
    for (const [re, label] of dirPatterns) {
      if (re.test(g)) { patternMatches[g] = label; break; }
    }
  });

  // H. Deployment topology
  const infraFiles = [];
  let hasDockerfile = false, hasCompose = false, hasK8s = false, hasTerraform = false, hasCI = false;
  fileNodes.forEach(n => {
    const p = pathOf(n);
    if (/Dockerfile/.test(p)) { hasDockerfile = true; infraFiles.push(p); }
    if (/docker-compose/.test(p)) { hasCompose = true; infraFiles.push(p); }
    if (/\.tf$|\.tfvars$/.test(p)) { hasTerraform = true; infraFiles.push(p); }
    if (/\.github\/workflows\//.test(p) || /gitlab-ci|Jenkinsfile/.test(p)) { hasCI = true; infraFiles.push(p); }
    if (/k8s|kubernetes|helm/.test(p)) { hasK8s = true; infraFiles.push(p); }
  });

  // I. Data pipeline
  const dataPipeline = { schemaFiles: [], migrationFiles: [], dataModelFiles: [], apiHandlerFiles: [] };
  fileNodes.forEach(n => {
    const p = pathOf(n);
    if (/\.sql$|schema\.(graphql|sql)/.test(p)) dataPipeline.schemaFiles.push(p);
    if (/migrations?\//.test(p)) dataPipeline.migrationFiles.push(p);
    if (/models?\//.test(p)) dataPipeline.dataModelFiles.push(p);
  });

  // J. Doc coverage
  const groupsWithDocs = {};
  fileNodes.forEach(n => {
    if (n.type === 'document') groupsWithDocs[fileToGroup[n.id]] = true;
  });
  const totalGroups = Object.keys(directoryGroups).length;
  const undoc = Object.keys(directoryGroups).filter(g => !groupsWithDocs[g]);
  const docCoverage = {
    groupsWithDocs: Object.keys(groupsWithDocs).length,
    totalGroups,
    coverageRatio: totalGroups ? +(Object.keys(groupsWithDocs).length / totalGroups).toFixed(2) : 0,
    undocumentedGroups: undoc,
  };

  // K. Dependency direction
  const dirPair = {};
  interGroupImports.forEach(({ from, to, count }) => {
    const key = [from, to].sort().join('|');
    dirPair[key] = dirPair[key] || {};
    dirPair[key][from + '->' + to] = count;
  });
  const dependencyDirection = [];
  Object.keys(dirPair).forEach(key => {
    const [a, b] = key.split('|');
    const ab = dirPair[key][a + '->' + b] || 0;
    const ba = dirPair[key][b + '->' + a] || 0;
    if (ab >= ba && ab > 0) dependencyDirection.push({ dependent: a, dependsOn: b });
    else if (ba > 0) dependencyDirection.push({ dependent: b, dependsOn: a });
  });

  const filesPerGroup = {};
  Object.entries(directoryGroups).forEach(([g, arr]) => filesPerGroup[g] = arr.length);
  const nodeTypeCounts = {};
  Object.entries(nodeTypeGroups).forEach(([t, arr]) => nodeTypeCounts[t] = arr.length);

  const result = {
    scriptCompleted: true,
    commonPrefix: prefix,
    directoryGroups, nodeTypeGroups, crossCategoryEdges, interGroupImports,
    intraGroupDensity, patternMatches,
    deploymentTopology: { hasDockerfile, hasCompose, hasK8s, hasTerraform, hasCI, infraFiles: [...new Set(infraFiles)] },
    dataPipeline, docCoverage, dependencyDirection,
    fileStats: { totalFileNodes: fileNodes.length, filesPerGroup, nodeTypeCounts },
    fileFanIn: fanIn, fileFanOut: fanOut,
  };
  fs.writeFileSync(outPath, JSON.stringify(result, null, 2));
  console.log('OK', fileNodes.length, 'nodes,', Object.keys(directoryGroups).length, 'groups');
}
try { main(); } catch (e) { console.error(e.stack || e); process.exit(1); }
