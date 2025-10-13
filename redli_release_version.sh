VERSION=0.14.0

# Cross-compile for different platforms
GOOS=windows GOARCH=amd64 go build -o redli.exe
GOOS=darwin GOARCH=amd64 go build -o redli_darwin_amd64
GOOS=linux GOARCH=amd64 go build -o redli_linux_amd64
GOOS=windows GOARCH=arm64 go build -o redli_arm64.exe
GOOS=darwin GOARCH=arm64 go build -o redli_darwin_arm64
GOOS=linux GOARCH=arm64 go build -o redli_linux_arm64

# Package the binaries into tar.gz files
tar -czf redli_${VERSION}_darwin_amd64.tar.gz redli_darwin_amd64
tar -czf redli_${VERSION}_windows_amd64.tar.gz redli.exe
tar -czf redli_${VERSION}_linux_amd64.tar.gz redli_linux_amd64
tar -czf redli_${VERSION}_darwin_arm64.tar.gz redli_darwin_arm64
tar -czf redli_${VERSION}_windows_arm64.tar.gz redli_arm64.exe
tar -czf redli_${VERSION}_linux_arm64.tar.gz redli_linux_arm64

# Generate checksums
sha256sum redli_${VERSION}_darwin_amd64.tar.gz > redli_${VERSION}_checksums.txt
sha256sum redli_${VERSION}_windows_amd64.tar.gz >> redli_${VERSION}_checksums.txt
sha256sum redli_${VERSION}_linux_amd64.tar.gz >> redli_${VERSION}_checksums.txt
sha256sum redli_${VERSION}_darwin_arm64.tar.gz >> redli_${VERSION}_checksums.txt
sha256sum redli_${VERSION}_windows_arm64.tar.gz >> redli_${VERSION}_checksums.txt
sha256sum redli_${VERSION}_linux_arm64.tar.gz >> redli_${VERSION}_checksums.txt

# Commit and tag release
git commit -m "Add release files for version ${VERSION}"
git tag -a v${VERSION} -m "Version ${VERSION} release"
git push origin v${VERSION} --force
