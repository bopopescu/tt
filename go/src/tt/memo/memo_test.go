package memo_test

import (
	"strings"
	"testing"
	"tt/memo"
)

var uppercase func(string) string

func init() {
	memo.Bind(&uppercase, 1, func(s string) string {
		return strings.ToUpper(s)
	})
}

func TestBasics(t *testing.T) {
	var tests = []string{
		"",
		"   ",
		"AppleCart",
		"apple",
		"APPLECARTING",
		"---",
	}

	for _, test := range tests {
		got := uppercase(test)
		want := strings.ToUpper(test)
		if want != got {
			t.Errorf("mismatch; wanted %q, got %q", want, got)
			continue
		}
	}
}
