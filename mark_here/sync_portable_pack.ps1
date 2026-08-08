# Sync portable MARK HERE knowledge pack into THIS folder.
# Run from anywhere; kit root = folder that contains this script.
# After sync, copy the whole mark_here/ folder anywhere.

[CmdletBinding()]
param(
  [string]$ArmyRoot = "",
  [string]$TruthRoot = "",
  [switch]$FullTrading,
  [switch]$Quiet
)

$ErrorActionPreference = "Continue"
$Kit = $PSScriptRoot
$PortablePath = Join-Path $Kit "PORTABLE.json"
$ManifestPath = Join-Path $Kit "PORTABLE_MANIFEST.json"
$Know = Join-Path $Kit "knowledge"

function Write-Info([string]$m) {
  if (-not $Quiet) { Write-Host "  $m" }
}

function Ensure-Dir([string]$p) {
  if (-not (Test-Path -LiteralPath $p)) {
    New-Item -ItemType Directory -Path $p -Force | Out-Null
  }
}

function Get-FileSha16([string]$path) {
  if (-not (Test-Path -LiteralPath $path)) { return $null }
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $fs = [System.IO.File]::OpenRead($path)
    try {
      $hash = $sha.ComputeHash($fs)
      return ([BitConverter]::ToString($hash[0..7])).Replace("-", "")
    } finally { $fs.Dispose() }
  } finally { $sha.Dispose() }
}

function Copy-FileSafe([string]$src, [string]$dst) {
  $parent = Split-Path -Parent $dst
  Ensure-Dir $parent
  Copy-Item -LiteralPath $src -Destination $dst -Force
}

function Copy-TreeFiltered {
  param(
    [string]$srcDir,
    [string]$dstDir,
    [int]$MaxMb = 0,
    [int]$TailLines = 0
  )
  if (-not (Test-Path -LiteralPath $srcDir)) { return 0 }
  $count = 0
  $maxBytes = if ($MaxMb -gt 0) { [long]$MaxMb * 1MB } else { [long]::MaxValue }
  Get-ChildItem -LiteralPath $srcDir -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
    $rel = $_.FullName.Substring($srcDir.Length).TrimStart('\', '/')
    $dst = Join-Path $dstDir $rel
    if ($_.Length -le $maxBytes) {
      Copy-FileSafe $_.FullName $dst
      $script:count++
      $count++
    } elseif ($TailLines -gt 0) {
      Ensure-Dir (Split-Path -Parent $dst)
      $noteName = "_TRUNCATED__" + $_.Name + ".txt"
      $note = Join-Path (Split-Path -Parent $dst) $noteName
      $mbRound = [math]::Round($_.Length / 1MB, 2)
      @(
        "PORTABLE TAIL ONLY - full file was larger than $MaxMb MB",
        "source: $($_.FullName)",
        "bytes: $($_.Length) (~$mbRound MB)",
        "tail_lines: $TailLines",
        "---"
      ) | Set-Content -LiteralPath $note -Encoding UTF8
      Get-Content -LiteralPath $_.FullName -Tail $TailLines -ErrorAction SilentlyContinue |
        Set-Content -LiteralPath $dst -Encoding UTF8
      $count++
    } else {
      Ensure-Dir (Split-Path -Parent $dst)
      $noteName = "_SKIPPED__" + $_.Name + ".txt"
      $note = Join-Path (Split-Path -Parent $dst) $noteName
      $mbRound = [math]::Round($_.Length / 1MB, 2)
      "Skipped oversized file ($mbRound MB): $($_.FullName). Re-run sync with -FullTrading to include." |
        Set-Content -LiteralPath $note -Encoding UTF8
    }
  }
  return $count
}

function Resolve-ArmyRoot([string]$hint) {
  $candidates = New-Object System.Collections.Generic.List[string]
  if ($hint) { [void]$candidates.Add($hint) }
  if ($env:MARKOS_ARMY_ROOT) { [void]$candidates.Add($env:MARKOS_ARMY_ROOT) }
  $parent = Split-Path -Parent $Kit
  [void]$candidates.Add((Join-Path $parent "ARMY\01_SYSTEM"))
  [void]$candidates.Add((Join-Path (Split-Path -Parent $parent) "ARMY\01_SYSTEM"))
  [void]$candidates.Add("C:\Users\user\OneDrive\Desktop\ARMY\01_SYSTEM")
  [void]$candidates.Add("C:\Users\user\Desktop\ARMY\01_SYSTEM")
  foreach ($c in $candidates) {
    if ($c -and (Test-Path -LiteralPath (Join-Path $c "config\agents"))) {
      return (Resolve-Path -LiteralPath $c).Path
    }
  }
  return $null
}

function Resolve-TruthRoot([string]$hint) {
  $candidates = New-Object System.Collections.Generic.List[string]
  if ($hint) { [void]$candidates.Add($hint) }
  if ($env:MARKOS_THE_TRUTH_ROOT) { [void]$candidates.Add($env:MARKOS_THE_TRUTH_ROOT) }
  $parent = Split-Path -Parent $Kit
  if (Test-Path -LiteralPath (Join-Path $parent "GOAL.md")) { [void]$candidates.Add($parent) }
  [void]$candidates.Add("C:\Users\user\Fable5_Foundation\MOMENTUM_ONE\the-truth")
  foreach ($c in $candidates) {
    if ($c -and (Test-Path -LiteralPath (Join-Path $c "GOAL.md"))) {
      return (Resolve-Path -LiteralPath $c).Path
    }
  }
  return $null
}

Write-Host ""
Write-Host "  ========================================"
Write-Host "   MARK HERE - sync portable knowledge pack"
Write-Host "  ========================================"
Write-Host ""

$cfg = $null
if (Test-Path -LiteralPath $PortablePath) {
  try {
    $cfg = Get-Content -LiteralPath $PortablePath -Raw -Encoding UTF8 | ConvertFrom-Json
  } catch {
    Write-Info "PORTABLE.json parse failed: $_"
  }
}

$Army = Resolve-ArmyRoot $ArmyRoot
$Truth = Resolve-TruthRoot $TruthRoot

Write-Info "kit:    $Kit"
if ($Army) { Write-Info "army:   $Army" } else { Write-Info "army:   (not found)" }
if ($Truth) { Write-Info "truth:  $Truth" } else { Write-Info "truth:  (not found)" }

Ensure-Dir $Know
Ensure-Dir (Join-Path $Know "soul")
Ensure-Dir (Join-Path $Know "doctrine\llm_basic_thinking")
Ensure-Dir (Join-Path $Know "kag\configs")
Ensure-Dir (Join-Path $Know "kag\army")
Ensure-Dir (Join-Path $Know "kag\skills")
Ensure-Dir (Join-Path $Know "kag\shared")
Ensure-Dir (Join-Path $Know "kag\wiki")
Ensure-Dir (Join-Path $Know "kag\trading")
Ensure-Dir (Join-Path $Know "lab")

$stats = [ordered]@{
  synced_utc       = (Get-Date).ToUniversalTime().ToString("o")
  army_root        = $Army
  truth_root       = $Truth
  full_trading     = [bool]$FullTrading
  counts           = [ordered]@{}
  soul_fingerprint = @()
  warnings         = @()
}

# --- 1) Soul + KAG configs from ARMY ---
if ($Army) {
  $agents = Join-Path $Army "config\agents"
  $soulNames = @(
    "MARK_PERSONALITY.md",
    "FABLE_METHOD.md",
    "ARMY_MORAL_DOCTRINE.md",
    "OPERATING_PRINCIPLES.md",
    "mark_personality.json",
    "army_moral.json",
    "fable_method.json",
    "second_brain.json",
    "fable5_mark_here_kag.json",
    "dual_folder_kag_peer.json",
    "super_mentor_l2l_kag.json",
    "physics_super_agent_kag.json"
  )
  if ($cfg -and $cfg.sync -and $cfg.sync.soul_files) {
    $soulNames = @($cfg.sync.soul_files)
  }

  $nSoul = 0
  $fpList = New-Object System.Collections.Generic.List[object]
  foreach ($name in $soulNames) {
    $src = Join-Path $agents $name
    if (-not (Test-Path -LiteralPath $src)) { continue }

    $isKag = $name -match "kag|second_brain|fable5|dual_folder|super_mentor|physics_super"
    if ($isKag) {
      Copy-FileSafe $src (Join-Path $Know "kag\configs\$name")
    } else {
      Copy-FileSafe $src (Join-Path $Know "soul\$name")
    }
    $nSoul++

    if ($name -match "MARK_PERSONALITY|FABLE_METHOD|ARMY_MORAL|mark_personality\.json|army_moral\.json") {
      $fpList.Add([ordered]@{
        file   = $name
        path   = $src
        hash16 = (Get-FileSha16 $src)
        bytes  = (Get-Item -LiteralPath $src).Length
      })
    }
  }
  $stats.counts["soul_and_kag_configs"] = $nSoul
  $stats["soul_fingerprint"] = @($fpList.ToArray())

  # 2) Doctrine from ARMY
  $armyDoc = Join-Path $Army "data\knowledge\skills\trading\llm_basic_thinking"
  if (Test-Path -LiteralPath $armyDoc) {
    $stats.counts["doctrine"] = Copy-TreeFiltered -srcDir $armyDoc -dstDir (Join-Path $Know "doctrine\llm_basic_thinking")
  }

  # 3) KAG knowledge dirs
  $kRoot = Join-Path $Army "data\knowledge"
  $dirMap = [ordered]@{
    "army"                = "kag\army"
    "skills"              = "kag\skills"
    "shared"              = "kag\shared"
    "wiki"                = "kag\wiki"
    "learning"            = "kag\learning"
    "personal_principles" = "kag\personal_principles"
    "project_memory"      = "kag\project_memory"
    "lessons_learned"     = "kag\lessons_learned"
  }
  foreach ($d in $dirMap.Keys) {
    $src = Join-Path $kRoot $d
    $dst = Join-Path $Know $dirMap[$d]
    $stats.counts["knowledge_$d"] = Copy-TreeFiltered -srcDir $src -dstDir $dst
  }

  # trading with size cap unless -FullTrading
  $tradeSrc = Join-Path $kRoot "trading"
  $tradeDst = Join-Path $Know "kag\trading"
  $maxMb = 8
  $tail = 2000
  if ($cfg -and $cfg.sync -and $cfg.sync.trading_max_file_mb) {
    $maxMb = [int]$cfg.sync.trading_max_file_mb
  }
  if ($cfg -and $cfg.sync -and $cfg.sync.trading_tail_lines_if_oversize) {
    $tail = [int]$cfg.sync.trading_tail_lines_if_oversize
  }
  if ($FullTrading) {
    $stats.counts["knowledge_trading"] = Copy-TreeFiltered -srcDir $tradeSrc -dstDir $tradeDst -MaxMb 0
  } else {
    $stats.counts["knowledge_trading"] = Copy-TreeFiltered -srcDir $tradeSrc -dstDir $tradeDst -MaxMb $maxMb -TailLines $tail
  }

  if ($fpList.Count -gt 0) {
    $fpList | ConvertTo-Json -Depth 5 |
      Set-Content -LiteralPath (Join-Path $Kit "SOUL_FINGERPRINT.json") -Encoding UTF8
  }
} else {
  $stats.warnings += "ARMY 01_SYSTEM not found - kept existing knowledge pack if present"
}

# --- 4) Lab pack from the-truth ---
if ($Truth) {
  $labDst = Join-Path $Know "lab"
  $nLab = 0
  $rootFiles = @(
    "SOUL_MATCH.md",
    "GOAL.md",
    "AGENTS.md",
    "KEEP_AFTER_SOUL.md",
    "POLICY_EQUALS_MARK_ON_CHART.md",
    "FURTHEST_WEAVE__POLICY_EQUALS_MARK_ON_CHART.md",
    "HANDOFF_2026-08-05.md",
    "00_MAP_OF_THE_HOUSE.md",
    "00_START_HERE.md",
    "DO_THIS.md"
  )
  # Always keep price-data map + configs/data.yaml in the pack (paths, not multi-GB CSVs)
  $priceSrc = Join-Path $Truth "mark_here\knowledge\00_PRICE_DATA.md"
  if (-not (Test-Path -LiteralPath $priceSrc)) {
    $priceSrc = Join-Path $Kit "knowledge\00_PRICE_DATA.md"
  }
  if (Test-Path -LiteralPath $priceSrc) {
    Copy-FileSafe $priceSrc (Join-Path $Know "00_PRICE_DATA.md")
    Copy-FileSafe $priceSrc (Join-Path $labDst "00_PRICE_DATA.md")
    Copy-FileSafe $priceSrc (Join-Path $Kit "PRICE_DATA.md")
  }
  $dataYaml = Join-Path $Truth "configs\data.yaml"
  if (Test-Path -LiteralPath $dataYaml) {
    Copy-FileSafe $dataYaml (Join-Path $labDst "configs\data.yaml")
  }

  # Flea-jar doctrine + Performance is possible (full copies travel with Mark)
  $fleaSrc = Join-Path $Truth "references\doctrine\flea-jar"
  $lidSrc = Join-Path $Truth "references\doctrine\00_LID_OFF_THE_JAR.md"
  $perfSrc = Join-Path $Truth "references\performance"
  if (Test-Path -LiteralPath $fleaSrc) {
    $fleaDst = Join-Path $Know "doctrine\flea-jar"
    Ensure-Dir $fleaDst
    $stats.counts["doctrine_flea_jar"] = Copy-TreeFiltered -srcDir $fleaSrc -dstDir $fleaDst
    $labFlea = Join-Path $labDst "references\doctrine\flea-jar"
    [void](Copy-TreeFiltered -srcDir $fleaSrc -dstDir $labFlea)
  }
  if (Test-Path -LiteralPath $lidSrc) {
    Copy-FileSafe $lidSrc (Join-Path $Know "doctrine\00_LID_OFF_THE_JAR.md")
    Copy-FileSafe $lidSrc (Join-Path $Know "00_LID_OFF_THE_JAR.md")
    Copy-FileSafe $lidSrc (Join-Path $Kit "00_LID_OFF_THE_JAR.md")
    Ensure-Dir (Join-Path $labDst "references\doctrine")
    Copy-FileSafe $lidSrc (Join-Path $labDst "references\doctrine\00_LID_OFF_THE_JAR.md")
  }
  if (Test-Path -LiteralPath $perfSrc) {
    $perfDst = Join-Path $Know "performance"
    Ensure-Dir $perfDst
    $stats.counts["performance_is_possible"] = Copy-TreeFiltered -srcDir $perfSrc -dstDir $perfDst
    [void](Copy-TreeFiltered -srcDir $perfSrc -dstDir (Join-Path $labDst "references\performance"))
  }
  if ($cfg -and $cfg.sync -and $cfg.sync.lab_root_files) {
    $rootFiles = @($cfg.sync.lab_root_files)
  }
  foreach ($f in $rootFiles) {
    $src = Join-Path $Truth $f
    if (Test-Path -LiteralPath $src) {
      Copy-FileSafe $src (Join-Path $labDst $f)
      $nLab++
    }
  }

  $truthDoc = Join-Path $Truth "references\doctrine\llm_basic_thinking"
  if (Test-Path -LiteralPath $truthDoc) {
    $stats.counts["doctrine_truth"] = Copy-TreeFiltered -srcDir $truthDoc -dstDir (Join-Path $Know "doctrine\llm_basic_thinking")
  }

  $extraGlobs = @(
    "lineages\adaptive_rl_brain_7_31_26\*MARK*.md",
    "lineages\adaptive_rl_brain_7_31_26\*SOUL*.md",
    "lineages\adaptive_rl_brain_7_31_26\MARK_*.md",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\*MARK*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\*FABLE5*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\*LEARNING*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\BEST__*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\*SPINE*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\*HITL*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\*KAG*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\WHAT_WORKS*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\fable_50d_match\GROW_UP*",
    "lineages\adaptive_rl_brain_7_31_26\checkpoints\mark_chart_hitl\*"
  )
  foreach ($g in $extraGlobs) {
    $full = Join-Path $Truth $g
    Get-ChildItem -Path $full -File -ErrorAction SilentlyContinue | ForEach-Object {
      $rel = $_.FullName.Substring($Truth.Length).TrimStart('\', '/')
      Copy-FileSafe $_.FullName (Join-Path $labDst $rel)
      $nLab++
    }
  }
  $stats.counts["lab_files"] = $nLab
} else {
  $stats.warnings += "the-truth not found - kept existing knowledge/lab if present"
}

# --- 5) Human index ---
$indexPath = Join-Path $Know "00_INDEX.md"
$soulLines = @("- (empty)")
if (Test-Path -LiteralPath (Join-Path $Know "soul")) {
  $soulFiles = Get-ChildItem -LiteralPath (Join-Path $Know "soul") -File -ErrorAction SilentlyContinue
  if ($soulFiles) {
    $soulLines = $soulFiles | ForEach-Object { "- knowledge/soul/$($_.Name)" }
  }
}
$kagLines = @("- (empty)")
if (Test-Path -LiteralPath (Join-Path $Know "kag\configs")) {
  $kagFiles = Get-ChildItem -LiteralPath (Join-Path $Know "kag\configs") -File -ErrorAction SilentlyContinue
  if ($kagFiles) {
    $kagLines = $kagFiles | ForEach-Object { "- knowledge/kag/configs/$($_.Name)" }
  }
}

$allPack = Get-ChildItem -LiteralPath $Know -Recurse -File -ErrorAction SilentlyContinue
$fileCount = if ($allPack) { $allPack.Count } else { 0 }
$byteSum = if ($allPack) { ($allPack | Measure-Object -Property Length -Sum).Sum } else { 0 }
$mb = if ($byteSum) { [math]::Round($byteSum / 1MB, 2) } else { 0 }

$warnText = "- none"
if ($stats.warnings -and $stats.warnings.Count -gt 0) {
  $warnText = ($stats.warnings | ForEach-Object { "- $_" }) -join "`n"
}

$armyLine = if ($Army) { $Army } else { "not found this run" }
$truthLine = if ($Truth) { $Truth } else { "not found this run" }
$soulBlock = $soulLines -join "`n"
$kagBlock = $kagLines -join "`n"

$index = @"
# MARK HERE - portable knowledge index

**Synced (UTC):** $($stats.synced_utc)
**Pack files:** $fileCount (~$mb MB)
**Army source:** $armyLine
**Lab source:** $truthLine

This folder travels with mark_here/. Copy the whole kit anywhere.

## One Mark rule

Same soul as ARMY MarkOS. This is a **mirror pack**, not a second personality.

## Where things live (relative to mark_here/)

| Pack | Path | What |
|------|------|------|
| Soul | knowledge/soul/ | Personality, Fable method, moral doctrine |
| Doctrine / pt5 | knowledge/doctrine/llm_basic_thinking/ | Basic knowledge every LLM must know |
| KAG configs | knowledge/kag/configs/ | fable5_mark_here_kag + dual folder peer |
| Army vault | knowledge/kag/army/ | MEMORY, KAG indexes, dialogue buses |
| Skills | knowledge/kag/skills/ | Trading skills vault |
| Trading slice | knowledge/kag/trading/ | Trading bus (large logs tailed unless -FullTrading) |
| Lab | knowledge/lab/ | GOAL, SOUL_MATCH, handoffs, 50d / Mark briefs |

## Soul files present

$soulBlock

## KAG configs present

$kagBlock

## Live chat vs offline

| Mode | How |
|------|-----|
| Live MarkOS chat | Needs ARMY 01_SYSTEM service on this machine -> Mark_Here_launch.cmd |
| Offline knowledge | Read this pack + open_offline_knowledge.ps1 |

## Refresh before big copy

From this folder:

    .\sync_portable_pack.ps1
    .\sync_portable_pack.ps1 -FullTrading

## Env overrides

| Var | Meaning |
|-----|---------|
| MARKOS_ARMY_ROOT | Path to ARMY 01_SYSTEM |
| MARKOS_THE_TRUTH_ROOT | Path to the-truth lab |

## Warnings this run

$warnText
"@

$index | Set-Content -LiteralPath $indexPath -Encoding UTF8

# --- 6) Manifest ---
$stats.counts["total_pack_files"] = $fileCount
$stats.counts["total_pack_mb"] = $mb
($stats | ConvertTo-Json -Depth 8) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

Write-Host ""
Write-Host "  Pack ready: $fileCount files (~$mb MB)"
Write-Host "  Index:      knowledge\00_INDEX.md"
Write-Host "  Manifest:   PORTABLE_MANIFEST.json"
if ($stats.warnings -and $stats.warnings.Count -gt 0) {
  Write-Host "  Warnings:"
  foreach ($w in $stats.warnings) { Write-Host "   - $w" }
}
Write-Host ""
Write-Host "  Copy the ENTIRE mark_here folder anywhere."
Write-Host "  Live chat still needs ARMY on that machine; knowledge pack does not."
Write-Host ""
