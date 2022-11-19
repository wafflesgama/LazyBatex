$filePath= './lazy-batex.zip'
if(Test-Path -LiteralPath $filePath){
    Remove-Item $filePath
}
Compress-Archive -LiteralPath '../LazyBatex' -DestinationPath $filePath