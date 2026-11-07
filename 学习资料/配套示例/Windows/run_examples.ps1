param(
    [ValidateSet('python', 'rtl', 'chisel')]
    [string]$Group = 'python',
    [string]$JavaHome
)
$ErrorActionPreference = 'Stop'
$entry = Join-Path $PSScriptRoot '..\run_examples.py'
$runnerArguments = @($entry, $Group)
if ($JavaHome) { $runnerArguments += @('--java-home', $JavaHome) }
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 @runnerArguments
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python @runnerArguments
} else {
    throw 'Python was not found. Read Windows/README.md first.'
}
exit $LASTEXITCODE
