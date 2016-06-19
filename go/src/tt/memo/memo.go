package memo

import (
	"bytes"
	"fmt"
	"reflect"
)

// Func is a formal function that can provide values.
type Func struct {
}

// Index is an index onto a Pile.
type Index struct {
}

// Pile is a list of tuples that provide storage.
type Pile struct {
}

func Bind(dst interface{}, ver int, src interface{}) {
	dstFn := reflect.ValueOf(dst).Elem()
	srcFn := reflect.ValueOf(src)
	if dstFn.Type() != srcFn.Type() {
		panic("src and dst function types not identical")
	}
	proxy := reflect.MakeFunc(dstFn.Type(), func(in []reflect.Value) []reflect.Value {
		return lookupOrCall(srcFn, in)
	})
	dstFn.Set(proxy)
}

var seen = map[string]string{}

func lookupOrCall(fn reflect.Value, in []reflect.Value) []reflect.Value {
	// TODO(bruce): use FuncType of fn to find the right history table for this function.
	fmt.Println("FuncType is ", string(funcType(fn)))
	key := in[0].Interface().(string)
	if val, ok := seen[key]; ok {
		return []reflect.Value{reflect.ValueOf(val)}
	}
	val := fn.Call(in)[0].Interface().(string)
	seen[key] = val
	return []reflect.Value{reflect.ValueOf(val)}
}

// FuncType represents the type of a function (params and returns) as a single atomic key.
type FuncType []byte

func funcType(fn reflect.Value) FuncType {
	fnType := fn.Type()
	var t bytes.Buffer
	for i, n := 0, fnType.NumIn(); i < n; i++ {
		if i > 0 {
			t.WriteString(",")
		}
		t.WriteString(fnType.In(i).Name())
	}
	t.WriteString(":")
	for i, n := 0, fnType.NumOut(); i < n; i++ {
		if i > 0 {
			t.WriteString(",")
		}
		t.WriteString(fnType.Out(i).Name())
	}
	return FuncType(t.Bytes())
}
