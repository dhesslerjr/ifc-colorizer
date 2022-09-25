pip install --platform manylinux2014_x86_64 --target=./ --implementation cp --python 3.9 --only-binary=:all: --upgrade requests

$ZipFileResult="./ifc-colorizer.zip"
$DirToExclude=@(".git", "venv")

Get-ChildItem "./" -Directory  | 
           where { $_.Name -notin $DirToExclude} | 
              Compress-Archive -DestinationPath $ZipFileResult -Update
			  
Compress-Archive -Path "./*.py" -DestinationPath $ZipFileResult -Update
Compress-Archive -Path "./requirements.txt" -DestinationPath $ZipFileResult -Update
