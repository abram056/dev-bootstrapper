package cli

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"
)

// captureOutput redirects stdout while fn runs and returns what was written.
func captureOutput(t *testing.T, fn func() error) (string, error) {
	t.Helper()
	old := os.Stdout
	r, w, err := os.Pipe()
	if err != nil {
		t.Fatalf("pipe: %v", err)
	}
	os.Stdout = w

	done := make(chan string)
	go func() {
		var buf bytes.Buffer
		io.Copy(&buf, r) //nolint:errcheck
		done <- buf.String()
	}()

	fnErr := fn()

	w.Close()
	os.Stdout = old
	out := <-done
	return out, fnErr
}

func TestGreet(t *testing.T) {
	out, err := captureOutput(t, func() error { return greet([]string{"World"}) })
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !strings.Contains(out, "Hello, World!") {
		t.Errorf("got %q, want greeting", out)
	}
}

func TestGreetNoArgs(t *testing.T) {
	if err := greet(nil); err == nil {
		t.Error("expected error for missing name")
	}
}

func TestVersion(t *testing.T) {
	out, err := captureOutput(t, func() error { return Run([]string{"version"}) })
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !strings.Contains(out, "{{project_slug}}") {
		t.Errorf("got %q, want version output", out)
	}
}

func TestUnknownCommand(t *testing.T) {
	if err := Run([]string{"nope"}); err == nil {
		t.Error("expected error for unknown command")
	}
}
