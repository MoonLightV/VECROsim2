package app

import (
	"github.com/jaegertracing/jaeger/model/json"
)

// JaegerTracesResponse represents a Jaeger Trace Search response
type JaegerTracesResponse struct {
	Data   []json.Trace `json:"data"`
	Total  int          `json:"total"`
	Limit  int          `json:"limit"`
	Offset int          `json:"offset"`
	Errors interface{}  `json:"errors"`
}

// Trace represents Trace
type Trace struct {
	TraceID string
	Spans   map[string]*Span
}

// Span represents a span
type Span struct {
	json.Span
}
