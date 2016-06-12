
all: devtools
	@echo "All done"

.PHONY: devtools
devtools: 
	go install github.com/nsf/gocode
	go install github.com/rogpeppe/godef
	go install github.com/golang/lint/golint
	go install github.com/lukehoban/go-outline
	go install sourcegraph.com/sqs/goreturns
	go install golang.org/x/tools/cmd/gorename
	go install github.com/tpng/gopkgs
	go install github.com/newhook/go-symbols
	go install golang.org/x/tools/cmd/guru
