package tui

import (
	"strings"
	"testing"

	tea "github.com/charmbracelet/bubbletea"
)

func TestUpdateIncrements(t *testing.T) {
	m := NewModel()
	updated, _ := m.Update(tea.KeyMsg{Type: tea.KeyUp})
	model := updated.(Model)
	if model.Count() != 1 {
		t.Errorf("got %d, want 1", model.Count())
	}
}

func TestUpdateDecrements(t *testing.T) {
	m := NewModel()
	updated, _ := m.Update(tea.KeyMsg{Type: tea.KeyDown})
	model := updated.(Model)
	if model.Count() != -1 {
		t.Errorf("got %d, want -1", model.Count())
	}
}

func TestUpdateQuit(t *testing.T) {
	m := NewModel()
	updated, cmd := m.Update(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("q")})
	if cmd == nil {
		t.Fatal("expected quit command")
	}
	if !updated.(Model).quitting {
		t.Error("expected quitting to be true")
	}
}

func TestViewContainsTitle(t *testing.T) {
	m := NewModel()
	if !strings.Contains(m.View(), "{{project_name}}") {
		t.Errorf("view missing title: %q", m.View())
	}
}
