// Package cli implements the command-line interface for {{project_name}}.
package cli

import (
	"errors"
	"fmt"
	"strings"
)

// Version is the tool version, overridable at build time.
var Version = "0.1.0"

// ErrHelp signals that help was requested.
var ErrHelp = errors.New("help requested")

// usage returns the help text.
func usage() string {
	return `{{project_slug}} — a command-line tool

Usage:
  {{project_slug}} <command> [arguments]

Commands:
  greet <name>   Greet someone
  version        Print version

Run "{{project_slug}} <command>" for usage details.`
}

// Run dispatches args to the matching subcommand.
func Run(args []string) error {
	if len(args) == 0 {
		fmt.Println(usage())
		return nil
	}

	switch args[0] {
	case "greet":
		return greet(args[1:])
	case "version":
		fmt.Printf("{{project_slug}} %s\n", Version)
		return nil
	case "help", "-h", "--help":
		fmt.Println(usage())
		return nil
	default:
		return fmt.Errorf("unknown command %q", args[0])
	}
}

// greet prints a greeting for the given name.
func greet(args []string) error {
	if len(args) != 1 {
		return errors.New("greet requires exactly one argument")
	}
	name := strings.TrimSpace(args[0])
	if name == "" {
		return errors.New("greet requires a non-empty name")
	}
	fmt.Printf("Hello, %s!\n", name)
	return nil
}
