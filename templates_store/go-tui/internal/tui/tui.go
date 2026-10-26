// Package tui implements the {{project_name}} terminal interface.
package tui

import (
	"strings"

	tea "github.com/charmbracelet/bubbletea"
)

// Model holds the application state.
type Model struct {
	width    int
	height   int
	count    int
	quitting bool
}

// NewModel returns the initial model.
func NewModel() Model {
	return Model{}
}

// Init is called once when the program starts.
func (m Model) Init() tea.Cmd {
	return nil
}

// Update handles incoming messages.
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q", "esc":
			m.quitting = true
			return m, tea.Quit
		case "up", "+":
			m.count++
		case "down", "-":
			m.count--
		}
	}
	return m, nil
}

// View renders the interface.
func (m Model) View() string {
	if m.quitting {
		return "bye!\n"
	}

	var b strings.Builder
	b.WriteString("{{project_name}}\n\n")
	b.WriteString("Count: " + itoa(m.count) + "\n\n")
	b.WriteString("↑/↓ or +/- to change, q to quit\n")

	if m.width > 0 {
		b.WriteString(strings.Repeat("─", max(m.width-1, 1)) + "\n")
	}
	return b.String()
}

// Count exposes the counter for tests.
func (m Model) Count() int { return m.count }

func itoa(n int) string {
	if n == 0 {
		return "0"
	}
	neg := n < 0
	if neg {
		n = -n
	}
	var buf [20]byte
	i := len(buf)
	for n > 0 {
		i--
		buf[i] = byte('0' + n%10)
		n /= 10
	}
	if neg {
		i--
		buf[i] = '-'
	}
	return string(buf[i:])
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
