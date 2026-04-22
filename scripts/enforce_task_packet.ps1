[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [string]$PacketPath,

  [Parameter(Mandatory = $true)]
  [string]$ResultPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Normalize-RelPath {
  param([string]$PathValue)
  $p = $PathValue.Trim()
  $p = $p -replace '\\', '/'
  $p = $p.TrimStart('.')
  $p = $p.TrimStart('/')
  return $p.ToLowerInvariant()
}

function Get-SectionLines {
  param(
    [string[]]$Lines,
    [string]$Header
  )
  $start = -1
  for ($i = 0; $i -lt $Lines.Count; $i++) {
    if ($Lines[$i].Trim() -eq $Header) {
      $start = $i + 1
      break
    }
  }
  if ($start -lt 0) { return @() }

  $end = $Lines.Count
  for ($j = $start; $j -lt $Lines.Count; $j++) {
    if ($Lines[$j] -match '^## ') {
      $end = $j
      break
    }
  }
  if ($end -le $start) { return @() }
  return $Lines[$start..($end - 1)]
}

function Get-LinkedPagePacketFromTaskPacket {
  param([string]$PacketText)
  $m = [regex]::Match($PacketText, '\((?:/)?docs/spec-v2/pages/([^)]+\.md)\)')
  if (-not $m.Success) {
    throw "Could not find linked page packet in task packet."
  }
  return $m.Groups[1].Value
}

function Get-AllowedWriteFilesFromPagePacket {
  param([string[]]$PageLines)
  $section = Get-SectionLines -Lines $PageLines -Header '## Allowed Write Files'
  $files = @()
  foreach ($line in $section) {
    $m = [regex]::Match($line, '^\s*-\s*`([^`]+)`')
    if ($m.Success) {
      $files += (Normalize-RelPath -PathValue $m.Groups[1].Value)
    }
  }
  return $files | Select-Object -Unique
}

function Get-AllowedTestFilesFromPagePacket {
  param([string]$PageText)
  $matches = [regex]::Matches($PageText, '/frontend/tests/e2e/([^)]+\.spec\.ts)\)')
  $files = @()
  foreach ($m in $matches) {
    $files += (Normalize-RelPath -PathValue ("frontend/tests/e2e/" + $m.Groups[1].Value))
  }
  return $files | Select-Object -Unique
}

function Is-BroadTestCommand {
  param([string]$Command)
  $c = $Command.ToLowerInvariant()
  if ($c -match '^\s*npm\s+exec\s+playwright\s+test\s*$') { return $true }
  if ($c -match '^\s*playwright\s+test\s*$') { return $true }
  if ($c -match '^\s*npm\s+run\s+test(:e2e)?\s*$') { return $true }
  if ($c -match '^\s*pytest(\.exe)?\s*$') { return $true }
  return $false
}

if (-not (Test-Path -LiteralPath $PacketPath)) {
  throw "Packet not found: $PacketPath"
}
if (-not (Test-Path -LiteralPath $ResultPath)) {
  throw "Result file not found: $ResultPath"
}

$packetText = Get-Content -LiteralPath $PacketPath -Raw -Encoding utf8
$packetLines = $packetText -split "`r?`n"
$linkedPageFile = Get-LinkedPagePacketFromTaskPacket -PacketText $packetText
$pagePath = Join-Path (Split-Path -Parent (Split-Path -Parent $PacketPath)) ("spec-v2/pages/" + $linkedPageFile)
if (-not (Test-Path -LiteralPath $pagePath)) {
  throw "Linked page packet not found: $pagePath"
}

$pageText = Get-Content -LiteralPath $pagePath -Raw -Encoding utf8
$pageLines = $pageText -split "`r?`n"
$allowedWriteFiles = @(Get-AllowedWriteFilesFromPagePacket -PageLines $pageLines)
$allowedTestFiles = @(Get-AllowedTestFilesFromPagePacket -PageText $pageText)

if ($allowedWriteFiles.Count -eq 0) {
  throw "No allowed write files found in page packet: $pagePath"
}

$resultJson = Get-Content -LiteralPath $ResultPath -Raw -Encoding utf8
$result = $resultJson | ConvertFrom-Json

$requiredProps = @('task_id', 'files_read', 'files_changed', 'dimensions_completed', 'tests_run', 'contract_gaps_found', 'notes')
foreach ($prop in $requiredProps) {
  if (-not ($result.PSObject.Properties.Name -contains $prop)) {
    throw "Result missing required property: $prop"
  }
}

$violations = New-Object System.Collections.Generic.List[string]

foreach ($changed in @($result.files_changed)) {
  $normalized = Normalize-RelPath -PathValue ([string]$changed)
  if (-not ($allowedWriteFiles -contains $normalized)) {
    $violations.Add("Changed file outside allowed scope: $changed")
  }
}

foreach ($entry in @($result.tests_run)) {
  $item = [string]$entry
  if (Is-BroadTestCommand -Command $item) {
    $violations.Add("Broad test command is forbidden: $item")
    continue
  }
  if ($item -match '\.spec\.ts') {
    $normalizedTest = Normalize-RelPath -PathValue $item
    if (-not ($allowedTestFiles -contains $normalizedTest)) {
      $violations.Add("Test file outside packet scope: $item")
    }
  }
}

if ($violations.Count -gt 0) {
  Write-Host "Task packet enforcement failed." -ForegroundColor Red
  foreach ($v in $violations) {
    Write-Host ("- " + $v) -ForegroundColor Red
  }
  exit 1
}

Write-Host "Task packet enforcement passed." -ForegroundColor Green
Write-Host ("Packet: " + $PacketPath)
Write-Host ("Page: " + $pagePath)
Write-Host ("Allowed write files: " + $allowedWriteFiles.Count)
Write-Host ("Allowed tests: " + $allowedTestFiles.Count)
exit 0
