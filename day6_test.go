package aoc2022

import (
	"testing"
)

func Test_marker(t *testing.T) {
	if marker(input, 4) != markerFast(input, 4) {
		t.Fail()
	}

	if marker(input, 14) != markerFast(input, 14) {
		t.Fail()
	}

}

func BenchmarkTestMarker(b *testing.B) {
	for i := 0; i < b.N; i++ {
		marker(input, 14)
	}

}
func BenchmarkTestMarkerFast(b *testing.B) {
	for i := 0; i < b.N; i++ {
		markerFast(input, 14)
	}
}
