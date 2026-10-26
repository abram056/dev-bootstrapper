//! {{project_name}} — a terminal UI built with ratatui.

use std::io;
use std::time::Duration;

use crossterm::event::{self, Event, KeyCode};
use crossterm::terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen};
use crossterm::execute;
use ratatui::prelude::{Alignment, CrosstermBackend, Frame, Terminal};
use ratatui::widgets::{Block, Borders, Paragraph};

#[derive(Default)]
struct App {
    counter: u32,
    should_quit: bool,
}

impl App {
    fn on_key(&mut self, code: KeyCode) {
        match code {
            KeyCode::Char('q') => self.should_quit = true,
            KeyCode::Up => self.counter += 1,
            KeyCode::Down => self.counter = self.counter.saturating_sub(1),
            _ => {}
        }
    }
}

fn draw(frame: &mut Frame, app: &App) {
    let paragraph = Paragraph::new(format!(
        "{{project_name}}\n\nCount: {}\n\n↑/↓ to change, q to quit",
        app.counter
    ))
    .block(Block::default().borders(Borders::ALL).title("{{project_name}}"))
    .alignment(Alignment::Center);

    frame.render_widget(paragraph, frame.size());
}

fn main() -> io::Result<()> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    let mut app = App::default();

    loop {
        terminal.draw(|frame| draw(frame, &app))?;

        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                app.on_key(key.code);
            }
        }

        if app.should_quit {
            break;
        }
    }

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
    terminal.show_cursor()?;
    Ok(())
}
