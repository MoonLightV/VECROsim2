package app

import (
	"github.com/jaegertracing/jaeger/model/json"
)

// GenerateTraceWithSpansMap builds traces list with span map
func GenerateTraceWithSpansMap(info *JaegerTracesResponse) []*Trace {
	var traces []*Trace

	var resultItem *Trace
	for _, trace := range info.Data {
		resultItem = &Trace{
			TraceID: string(trace.TraceID),
			Spans:   map[string]*Span{},
		}

		for _, span := range trace.Spans {
			resultItem.Spans[spanKey(&span, &trace)] = &Span{span}
		}

		traces = append(traces, resultItem)
	}

	return traces
}

func spanKey(span *json.Span, trace *json.Trace) string {
	name := span.OperationName
	process := trace.Processes[span.ProcessID]
	if process.ServiceName != "" {
		name = process.ServiceName + " " + name
	}
	return name
}
