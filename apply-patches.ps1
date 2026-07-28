param(
    [string]$ImHexDir = (Get-Location).Path
)

$PatchesDir = Join-Path $PSScriptRoot "patches"

$Order = @(
    "01-builtin-library-plugin.patch"
    "02-fileprovider-public-open.patch"
    "03-fileprovider-graceful-settings.patch"
    "04-provider-graceful-settings.patch"
    "05-appleclang-build-helpers.patch"
    "0007-fix-Replace-RequestOpenFile-event-based-approach-wit.patch"
    "0008-fix-Improve-disassembly-and-diff-error-handling.patch"
    "0009-fix-Implement-TaskManager-based-diff-analysis-ALL-v0.patch"
    "0010-feat-Add-batch-open_directory-endpoint-v1.0.0-Phase-.patch"
    "0011-Add-batch-search-endpoint-for-v1.0.0-Phase-2.patch"
    "0012-Add-batch-hash-endpoint-for-v1.0.0-Phase-2.patch"
    "0013-Fix-glob-pattern-matching-in-batch-open_directory.patch"
    "0014-Fix-glob-pattern-escaping-bug-in-batch-open_director.patch"
    "06-mcp-api-compatibility.patch"
    "0001-feat-Implement-queue-based-file-opening-to-fix-netwo.patch"
)

Write-Host "Applying patches to $ImHexDir ..." -ForegroundColor Cyan

$ok = 0; $fail = 0
foreach ($p in $Order) {
    $path = Join-Path $PatchesDir $p
    if (-not (Test-Path $path)) {
        Write-Host "  $p - NOT FOUND" -ForegroundColor Yellow
        $fail++
        continue
    }
    $output = & git -C $ImHexDir apply $path 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $p OK" -ForegroundColor Green
        $ok++
    } else {
        Write-Host "  $p FAILED" -ForegroundColor Red
        $fail++
    }
}

Write-Host "---" -ForegroundColor Cyan
Write-Host "$ok applied, $fail failed" -ForegroundColor $(if ($fail -eq 0) { "Green" } else { "Red" })
